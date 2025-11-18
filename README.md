# Local LLM for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)

This repository provides two ways to run local LLMs with Home Assistant:

1. **Add-on** (Recommended) - Run Ollama LLM server directly in Home Assistant
2. **Custom Integration** - Connect to an external LLM server

## 🚀 Quick Start

### Option 1: Using the Add-on (Easiest)

1. **Add this repository to Home Assistant:**
   - Go to **Settings** → **Add-ons** → **Add-on Store**
   - Click the three dots (⋮) in the top right
   - Select **Repositories**
   - Add: `https://github.com/tylergraf/local_llm`

2. **Install the Local LLM Server add-on**
   - Find "Local LLM Server" in the store
   - Click **Install**
   - Configure your preferred model (e.g., `llama3.2:1b`)
   - Click **Start**

3. **Configure Home Assistant conversation agent**
   - Use base URL: `http://localhost:11434/v1`

### Option 2: Using the Custom Integration

If you're running an LLM server elsewhere (external Ollama, llama.cpp, etc.):

1. **Install via HACS:**
   - Go to **HACS** → **Integrations**
   - Click the three dots (⋮) → **Custom repositories**
   - Add: `https://github.com/tylergraf/local_llm`
   - Category: **Integration**

2. **Add the integration:**
   - Go to **Settings** → **Devices & Services**
   - Search for "Local LLM"
   - Enter your LLM server URL (e.g., `http://your-server:11434/v1`)

## 📦 What's Included

### Add-on: Local LLM Server
- Runs Ollama LLM server in Home Assistant
- OpenAI-compatible API
- Automatic model management
- Works offline
- Supports multiple architectures (amd64, aarch64)

### Custom Integration: Local LLM Conversation
- Connects to any OpenAI-compatible LLM API
- Full Home Assistant conversation agent support
- Configurable via UI
- Works with Ollama, llama.cpp, LM Studio, etc.

## 🧠 Supported Models

Any model available in [Ollama's library](https://ollama.com/library):

- `llama3.2:1b` - Fastest, smallest (~2GB RAM)
- `llama3.2:3b` - Good balance (~4GB RAM)
- `phi3:mini` - Efficient (~2GB RAM)
- `mistral:7b` - High quality (~8GB RAM)
- Many more...

## 💡 Use Cases

- **Voice Assistant**: "Hey Google, what's the weather like?"
- **Smart Home Control**: Natural language automation
- **Offline Operation**: No internet required
- **Privacy**: All processing happens locally
- **Custom Prompts**: Tailor responses to your needs

## 📋 Requirements

### For Add-on
- Home Assistant OS or Supervised
- 4GB+ RAM (8GB+ recommended for larger models)
- 5GB+ free storage (per model)
- amd64 or aarch64 architecture

### For Custom Integration
- Home Assistant (any installation type)
- External LLM server with OpenAI-compatible API

## 🔧 Configuration

### Add-on Configuration

```json
{
  "default_model": "llama3.2:1b",
  "keep_alive": "5m"
}
```

### Integration Configuration

Configure through the Home Assistant UI:
- **Base URL**: Your LLM server endpoint
- **API Key**: If required (optional for Ollama)
- **Model**: Model name if different from server default

## 📖 Documentation

- [Add-on Documentation](local-llm/README.md)
- [Installation Guide](INSTALL.md)
- [Troubleshooting](#troubleshooting)

## 🐛 Troubleshooting

### Add-on won't start
- Check you have enough RAM (4GB minimum)
- Try a smaller model like `llama3.2:1b`
- Check add-on logs for specific errors

### Integration can't connect
- Verify your LLM server is running
- Check the URL is correct (include `/v1` for Ollama)
- For Docker: use `host.docker.internal` instead of `localhost`

### Slow responses
- Use a smaller/faster model
- Increase `keep_alive` to keep model in memory
- Ensure sufficient RAM available

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 📄 License

This project is licensed under the MIT License.

## ⭐ Support

If you find this useful, please consider starring the repository!

## 🔗 Links

- [Home Assistant](https://www.home-assistant.io/)
- [Ollama](https://ollama.com/)
- [HACS](https://hacs.xyz/)

[releases-shield]: https://img.shields.io/github/release/tylergraf/local_llm.svg
[releases]: https://github.com/tylergraf/local_llm/releases
[license-shield]: https://img.shields.io/github/license/tylergraf/local_llm.svg
