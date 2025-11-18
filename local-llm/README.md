# Local LLM Server Add-on

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg

## About

This add-on runs a local LLM (Large Language Model) server using Ollama. It provides an OpenAI-compatible API that can be used with Home Assistant's conversation agent integration.

## Features

- 🚀 Easy installation - No manual setup required
- 🔒 Private & Local - Your conversations stay on your device
- 💬 OpenAI-compatible API - Works with Home Assistant conversation agent
- 🎯 Multiple models - Support for various LLM models
- ⚡ Fast inference - Optimized for local performance

## Installation

1. Add this repository to your Home Assistant add-on store:
   - Go to **Settings** → **Add-ons** → **Add-on Store**
   - Click the three dots (⋮) in the top right
   - Select **Repositories**
   - Add: `https://github.com/tylergraf/local_llm`

2. Find "Local LLM Server" in the add-on store
3. Click **Install**
4. Configure the add-on (see Configuration section)
5. Click **Start**

## Configuration

### Options

- **default_model** (required): The Ollama model to use
  - Examples: `llama3.2:1b`, `llama3.2:3b`, `mistral`, `phi3`
  - Smaller models (1b-3b) are faster but less capable
  - Larger models require more RAM and are slower

- **keep_alive** (optional): How long to keep models in memory
  - Default: `5m` (5 minutes)
  - Set to `0` to unload immediately after use
  - Set to `-1` to keep loaded indefinitely

### Example Configuration

```json
{
  "default_model": "llama3.2:1b",
  "keep_alive": "5m"
}
```

## Using with Home Assistant

After starting the add-on, configure Home Assistant's conversation agent:

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "OpenAI Conversation"
4. Configure:
   - **API Key**: `sk-dummy` (required but not used)
   - In Advanced Settings:
     - **Base URL**: `http://localhost:11434/v1`
     - **Model**: Use the same model as configured in the add-on

Alternatively, if you have the Local LLM custom integration installed, use:
- **Base URL**: `http://localhost:11434/v1`

## Available Models

Visit [Ollama Library](https://ollama.com/library) for a full list of available models.

Popular models for Home Assistant:
- `llama3.2:1b` - Smallest, fastest (2GB RAM)
- `llama3.2:3b` - Good balance (2-4GB RAM)
- `phi3:mini` - Microsoft's efficient model (2GB RAM)
- `mistral:7b` - More capable (8GB RAM)

## Hardware Requirements

- **Minimum**: 4GB RAM for 1B-3B models
- **Recommended**: 8GB+ RAM for 7B models
- **Storage**: 2-10GB per model

## Troubleshooting

### Add-on won't start
- Check logs for errors
- Ensure you have enough free RAM
- Try a smaller model

### Model download is slow
- Large models can take time to download (several GB)
- Check the add-on logs for progress

### Conversation agent not responding
- Verify the add-on is running
- Check base URL is `http://localhost:11434/v1`
- Look at Home Assistant logs for errors

## Support

For issues and questions:
- [GitHub Issues](https://github.com/tylergraf/local_llm/issues)
- [Home Assistant Community](https://community.home-assistant.io/)
