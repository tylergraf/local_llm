# Local LLM Server

## What This Add-on Does

This add-on runs Ollama, a local LLM server, directly within Home Assistant. Ollama provides an OpenAI-compatible API that allows you to use powerful language models completely offline and privately.

## Quick Start

1. Install the add-on
2. Set your desired model in Configuration (e.g., `llama3.2:1b`)
3. Start the add-on
4. Wait for the model to download (check logs)
5. Configure Home Assistant conversation agent to use `http://localhost:11434/v1`

## Configuration

### default_model

The Ollama model identifier to download and use by default.

**Examples:**
- `llama3.2:1b` - Best for devices with limited RAM (~2GB required)
- `llama3.2:3b` - Good balance of speed and quality (~4GB RAM)
- `mistral:7b` - Higher quality responses (~8GB RAM)
- `phi3:mini` - Microsoft's efficient model (~2GB RAM)

### keep_alive

How long to keep the model loaded in memory after the last request.

**Values:**
- `5m` - Keep for 5 minutes (default)
- `0` - Unload immediately
- `-1` - Keep loaded indefinitely
- `1h` - Keep for 1 hour

## API Endpoint

Once running, the API is available at:
```
http://localhost:11434/v1
```

This is OpenAI API-compatible, so you can use it with any integration that supports OpenAI.

## Model Management

### Pulling Models

The default model is automatically pulled on first start. To pull additional models:

1. Install the SSH add-on or Terminal add-on
2. Access the add-on container:
```bash
docker exec -it addon_local_slug_local-llm ollama pull <model-name>
```

### Listing Models

```bash
docker exec -it addon_local_slug_local-llm ollama list
```

## Resources

- [Ollama Model Library](https://ollama.com/library)
- [Ollama Documentation](https://github.com/ollama/ollama)
- [Home Assistant Conversation](https://www.home-assistant.io/integrations/conversation/)
