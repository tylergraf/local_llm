"""Base entity for Local LLM."""

from __future__ import annotations

import base64
from collections.abc import AsyncGenerator, Callable, Iterable
import json
from mimetypes import guess_file_type
from pathlib import Path
import re
from typing import TYPE_CHECKING, Any, Literal, cast

import openai
from openai._streaming import AsyncStream
from openai.types.chat import (
    ChatCompletionChunk,
    ChatCompletionMessageParam,
    ChatCompletionToolParam,
)
from openai.types.chat.chat_completion_chunk import ChoiceDeltaToolCall
import voluptuous as vol
from voluptuous_openapi import convert

from homeassistant.components import conversation
from homeassistant.config_entries import ConfigSubentry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import device_registry as dr, issue_registry as ir, llm
from homeassistant.helpers.entity import Entity
from homeassistant.util import slugify

from .const import (
    CONF_CHAT_MODEL,
    CONF_CODE_INTERPRETER,
    CONF_IMAGE_MODEL,
    CONF_MAX_TOKENS,
    CONF_REASONING_EFFORT,
    CONF_TEMPERATURE,
    CONF_TOP_P,
    CONF_VERBOSITY,
    CONF_WEB_SEARCH,
    CONF_WEB_SEARCH_CITY,
    CONF_WEB_SEARCH_CONTEXT_SIZE,
    CONF_WEB_SEARCH_COUNTRY,
    CONF_WEB_SEARCH_INLINE_CITATIONS,
    CONF_WEB_SEARCH_REGION,
    CONF_WEB_SEARCH_TIMEZONE,
    CONF_WEB_SEARCH_USER_LOCATION,
    DOMAIN,
    LOGGER,
    RECOMMENDED_CHAT_MODEL,
    RECOMMENDED_IMAGE_MODEL,
    RECOMMENDED_MAX_TOKENS,
    RECOMMENDED_REASONING_EFFORT,
    RECOMMENDED_TEMPERATURE,
    RECOMMENDED_TOP_P,
    RECOMMENDED_VERBOSITY,
    RECOMMENDED_WEB_SEARCH_CONTEXT_SIZE,
    RECOMMENDED_WEB_SEARCH_INLINE_CITATIONS,
)

if TYPE_CHECKING:
    from . import LocalLLMConfigEntry


# Max number of back and forth with the LLM to generate a response
MAX_TOOL_ITERATIONS = 10


def _adjust_schema(schema: dict[str, Any]) -> None:
    """Adjust the schema to be compatible with OpenAI API."""
    if schema["type"] == "object":
        schema.setdefault("strict", True)
        schema.setdefault("additionalProperties", False)
        if "properties" not in schema:
            return

        if "required" not in schema:
            schema["required"] = []

        # Ensure all properties are required
        for prop, prop_info in schema["properties"].items():
            _adjust_schema(prop_info)
            if prop not in schema["required"]:
                prop_info["type"] = [prop_info["type"], "null"]
                schema["required"].append(prop)

    elif schema["type"] == "array":
        if "items" not in schema:
            return

        _adjust_schema(schema["items"])


def _format_structured_output(
    schema: vol.Schema, llm_api: llm.APIInstance | None
) -> dict[str, Any]:
    """Format the schema to be compatible with OpenAI API."""
    result: dict[str, Any] = convert(
        schema,
        custom_serializer=(
            llm_api.custom_serializer if llm_api else llm.selector_serializer
        ),
    )

    _adjust_schema(result)

    return result


def _format_tool(
    tool: llm.Tool, custom_serializer: Callable[[Any], Any] | None
) -> ChatCompletionToolParam:
    """Format tool specification."""
    return ChatCompletionToolParam(
        type="function",
        function={
            "name": tool.name,
            "parameters": convert(tool.parameters, custom_serializer=custom_serializer),
            "description": tool.description,
            # "strict": False,  # Not always supported by all backends
        },
    )


def _convert_content_to_param(
    chat_content: Iterable[conversation.Content],
) -> list[ChatCompletionMessageParam]:
    """Convert any native chat message for this agent to the native format."""
    messages: list[ChatCompletionMessageParam] = []

    for content in chat_content:
        if isinstance(content, conversation.ToolResultContent):
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": content.tool_call_id,
                    "content": json.dumps(content.tool_result),
                }
            )
            continue

        if content.content:
            role: Literal["user", "assistant", "system", "developer"] = content.role
            if role == "developer":
                role = "system"  # 'developer' role is not standard in all chat completions
            messages.append({"role": role, "content": content.content})

        if isinstance(content, conversation.AssistantContent):
            if content.tool_calls:
                tool_calls = []
                for tool_call in content.tool_calls:
                    tool_calls.append(
                        {
                            "id": tool_call.id,
                            "type": "function",
                            "function": {
                                "name": tool_call.tool_name,
                                "arguments": json.dumps(tool_call.tool_args),
                            },
                        }
                    )
                messages.append(
                    {
                        "role": "assistant",
                        "tool_calls": tool_calls,
                    }
                )

    return messages


async def _transform_stream(
    chat_log: conversation.ChatLog,
    stream: AsyncStream[ChatCompletionChunk],
    remove_citations: bool = False,
) -> AsyncGenerator[
    conversation.AssistantContentDeltaDict | conversation.ToolResultContentDeltaDict
]:
    """Transform an OpenAI delta stream into HA format."""
    # remove_citations logic is simplified or removed as it was specific to how
    # the previous model/API handled it. If needed, it can be re-added.
    # For now, we assume standard text output.

    current_tool_calls: dict[int, ChoiceDeltaToolCall] = {}

    async for chunk in stream:
        if not chunk.choices:
            continue

        delta = chunk.choices[0].delta

        if delta.content:
            yield {"content": delta.content}

        if delta.tool_calls:
            for tool_call in delta.tool_calls:
                index = tool_call.index
                if index not in current_tool_calls:
                    current_tool_calls[index] = tool_call
                else:
                    # Accumulate arguments
                    if tool_call.function and tool_call.function.arguments:
                        current_tool_calls[index].function.arguments += (
                            tool_call.function.arguments
                        )

        if chunk.choices[0].finish_reason == "tool_calls":
            # Yield all accumulated tool calls
            tool_input_list = []
            for index in sorted(current_tool_calls.keys()):
                tool_call = current_tool_calls[index]
                if tool_call.function:
                    tool_input_list.append(
                        llm.ToolInput(
                            id=tool_call.id,
                            tool_name=tool_call.function.name,
                            tool_args=json.loads(tool_call.function.arguments),
                        )
                    )
            if tool_input_list:
                yield {"tool_calls": tool_input_list}
            current_tool_calls = {}

        if chunk.usage:
             chat_log.async_trace(
                {
                    "stats": {
                        "input_tokens": chunk.usage.prompt_tokens,
                        "output_tokens": chunk.usage.completion_tokens,
                    }
                }
            )


class LocalLLMBaseLLMEntity(Entity):
    """Local LLM conversation agent."""

    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, entry: LocalLLMConfigEntry, subentry: ConfigSubentry) -> None:
        """Initialize the entity."""
        self.entry = entry
        self.subentry = subentry
        self._attr_unique_id = subentry.subentry_id
        self._attr_device_info = dr.DeviceInfo(
            identifiers={(DOMAIN, subentry.subentry_id)},
            name=subentry.title,
            manufacturer="Local LLM",
            model=subentry.data.get(CONF_CHAT_MODEL, RECOMMENDED_CHAT_MODEL),
            entry_type=dr.DeviceEntryType.SERVICE,
        )

    async def _async_handle_chat_log(
        self,
        chat_log: conversation.ChatLog,
        structure_name: str | None = None,
        structure: vol.Schema | None = None,
        force_image: bool = False,
    ) -> None:
        """Generate an answer for the chat log."""
        options = self.subentry.data

        messages = _convert_content_to_param(chat_log.content)

        model_args = {
            "model": options.get(CONF_CHAT_MODEL, RECOMMENDED_CHAT_MODEL),
            "messages": messages,
            "max_tokens": options.get(CONF_MAX_TOKENS, RECOMMENDED_MAX_TOKENS),
            "top_p": options.get(CONF_TOP_P, RECOMMENDED_TOP_P),
            "temperature": options.get(CONF_TEMPERATURE, RECOMMENDED_TEMPERATURE),
            "user": chat_log.conversation_id,
            # "store": False, # Not always supported
            "stream": True,
        }

        # Reasoning models support
        if model_args["model"].startswith(("o", "gpt-5")):
             # Adjust for reasoning models if necessary, but standard chat completions
             # usually handles this via model params or separate reasoning_effort param
             # if supported by the library/backend.
             pass

        # ... (rest of the logic for tools and images)

        tools: list[ChatCompletionToolParam] = []
        if chat_log.llm_api:
            tools = [
                _format_tool(tool, chat_log.llm_api.custom_serializer)
                for tool in chat_log.llm_api.tools
            ]

        remove_citations = False
        # Web search and other specific tools logic might need adjustment
        # but for now we keep it minimal or comment out unsupported parts
        # if they rely on specific Response API features.
        
        if tools:
            model_args["tools"] = tools

        last_content = chat_log.content[-1]

        # Handle attachments by adding them to the last user message
        if last_content.role == "user" and last_content.attachments:
            files = await async_prepare_files_for_prompt(
                self.hass,
                [(a.path, a.mime_type) for a in last_content.attachments],
            )
            last_message = messages[-1]
            assert (
                last_message["role"] == "user"
                and isinstance(last_message["content"], str)
            )
            # Convert content to list of parts
            last_message["content"] = [
                {"type": "text", "text": last_message["content"]},
                *files,
            ]

        if structure and structure_name:
             model_args["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": slugify(structure_name),
                    "schema": _format_structured_output(structure, chat_log.llm_api),
                    "strict": True,
                },
            }

        client = self.entry.runtime_data

        # To prevent infinite loops, we limit the number of iterations
        for _iteration in range(MAX_TOOL_ITERATIONS):
            try:
                stream = await client.chat.completions.create(**model_args)

                messages.extend(
                    _convert_content_to_param(
                        [
                            content
                            async for content in chat_log.async_add_delta_content_stream(
                                self.entity_id,
                                _transform_stream(chat_log, stream, remove_citations),
                            )
                        ]
                    )
                )
            except openai.RateLimitError as err:
                LOGGER.error("Rate limited by Local LLM: %s", err)
                raise HomeAssistantError("Rate limited by Local LLM") from err
            except openai.OpenAIError as err:
                if (
                    isinstance(err, openai.APIError)
                    and err.type == "insufficient_quota"
                ):
                    LOGGER.error("Insufficient quota for Local LLM: %s", err)
                    raise HomeAssistantError("Insufficient quota for Local LLM") from err

                LOGGER.error("Error talking to Local LLM: %s", err)
                raise HomeAssistantError("Error talking to Local LLM") from err

            if not chat_log.unresponded_tool_results:
                break


async def async_prepare_files_for_prompt(
    hass: HomeAssistant, files: list[tuple[Path, str | None]]
) -> list[dict[str, Any]]:
    """Append files to a prompt.

    Caller needs to ensure that the files are allowed.
    """

    def append_files_to_content() -> list[dict[str, Any]]:
        content: list[dict[str, Any]] = []

        for file_path, mime_type in files:
            if not file_path.exists():
                raise HomeAssistantError(f"`{file_path}` does not exist")

            if mime_type is None:
                mime_type = guess_file_type(file_path)[0]

            if not mime_type or not mime_type.startswith(("image/", "application/pdf")):
                raise HomeAssistantError(
                    "Only images and PDF are supported by the Local LLM API,"
                    f"`{file_path}` is not an image file or PDF"
                )

            base64_file = base64.b64encode(file_path.read_bytes()).decode("utf-8")

            if mime_type.startswith("image/"):
                content.append(
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_file}",
                            "detail": "auto",
                        },
                    }
                )
            elif mime_type.startswith("application/pdf"):
                # Note: Standard OpenAI Chat Completions does not support PDF directly.
                # This is kept for compatibility if the backend supports it or if we want to
                # pass it as a custom content part.
                # For now, we'll try to pass it as an image_url with pdf mime type if the backend supports it,
                # or just a custom dict.
                content.append(
                    {
                        "type": "image_url", # Some backends might treat this as file input
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_file}",
                        }
                    }
                )

        return content

    return await hass.async_add_executor_job(append_files_to_content)
