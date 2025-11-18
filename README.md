# Local LLM Conversation for Home Assistant

A custom Home Assistant integration that connects to external LLM servers with OpenAI-compatible APIs. Use any LLM server on your network or the internet - Ollama, llama.cpp, LM Studio, vLLM, and more.

## Features

- 🌐 **Connect to ANY LLM Server** - Works with any OpenAI-compatible API
- 🏠 **LAN or Remote** - Connect to servers on your local network or internet
- 💬 **Full Conversation Agent** - Complete Home Assistant conversation integration
- 🎨 **Easy Configuration** - Set up through the Home Assistant UI
- 🔒 **Privacy Focused** - Keep conversations on your own infrastructure

## Supported LLM Servers

This integration works with any server that provides an OpenAI-compatible API:

- **[Ollama](https://ollama.com/)** - Easy local LLM server
- **[llama.cpp](https://github.com/ggerganov/llama.cpp)** - Lightweight C++ implementation
- **[LM Studio](https://lmstudio.ai/)** - Desktop LLM server with GUI
- **[vLLM](https://github.com/vllm-project/vllm)** - High-performance serving
- **[LocalAI](https://localai.io/)** - Self-hosted OpenAI alternative
- **[text-generation-webui](https://github.com/oobabooga/text-generation-webui)** - Feature-rich web interface
- **OpenAI** (or compatible cloud services)
- Any other OpenAI-compatible API

## Installation

### Via HACS (Recommended)

1. Open **HACS** in Home Assistant
2. Click on **Integrations**
3. Click the three dots (⋮) in the top right
4. Select **Custom repositories**
5. Add repository URL: `https://github.com/tylergraf/local_llm`
6. Category: **Integration**
7. Click **Add**
8. Find "Local LLM Conversation" and click **Download**
9. Restart Home Assistant

### Manual Installation

1. Download this repository
2. Copy the `custom_components/local_llm` folder to your Home Assistant `config/custom_components/` directory
3. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "Local LLM"
4. Enter your LLM server details:
   - **Base URL**: Your server endpoint (e.g., `http://192.168.1.100:11434/v1`)
   - **API Key**: If required (leave blank for most local servers)
   - **Model**: Model name (optional, uses server default if blank)

### Example Configurations

#### Ollama on LAN
```
Base URL: http://192.168.1.50:11434/v1
API Key: (leave blank)
Model: llama3.2:3b
```

#### LM Studio on Same Machine
```
Base URL: http://localhost:1234/v1
API Key: (leave blank)
Model: (leave blank - uses loaded model)
```

#### Home Assistant in Docker → Host LLM Server
```
Base URL: http://host.docker.internal:11434/v1
API Key: (leave blank)
Model: llama3.2:3b
```

#### Remote Server
```
Base URL: https://my-llm-server.example.com/v1
API Key: your-api-key-if-required
Model: llama3.2:3b
```

## Usage

Once configured, you can use the LLM in:

### Voice Assistants
Set it as your conversation agent in Assist settings.

### Automations
```yaml
service: conversation.process
data:
  text: "What's the weather like today?"
  agent_id: conversation.local_llm
```

### Scripts & Services
Use the `local_llm.generate` service for custom text generation tasks.

## Setting Up Your LLM Server

Don't have an LLM server yet? Here are quick start guides:

### Option 1: Ollama (Easiest)

**On Mac/Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:3b
ollama serve
```

**On Windows:**
Download from [ollama.com](https://ollama.com/)

### Option 2: LM Studio

1. Download [LM Studio](https://lmstudio.ai/)
2. Download a model (e.g., llama-3.2-3b)
3. Load the model
4. Click "Local Server" and start the server

### Option 3: llama.cpp Server

```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make
./server -m models/your-model.gguf --host 0.0.0.0 --port 8080
```

## Troubleshooting

### Integration doesn't appear in the list
- Clear browser cache (Ctrl+Shift+R / Cmd+Shift+R)
- Verify files are in `custom_components/local_llm/`
- Check Home Assistant logs for errors
- Restart Home Assistant completely

### Can't connect to server
- Verify the LLM server is running
- Check the URL format includes `/v1` at the end (for Ollama/compatible servers)
- If HA is in Docker, use `host.docker.internal` instead of `localhost`
- Check firewall settings allow the connection
- Test the URL in a browser or with curl:
  ```bash
  curl http://your-server:11434/v1/models
  ```

### Slow responses
- Use a smaller/faster model
- Ensure your server has enough RAM
- Check CPU/GPU utilization on the LLM server
- Consider upgrading server hardware

### Docker Users - HA Can't Reach LAN Server

If Home Assistant is running in Docker and can't reach your LAN LLM server:

**Option A**: Use host networking
```yaml
# docker-compose.yml
services:
  homeassistant:
    network_mode: host
```

**Option B**: Use the host's IP address
Instead of `localhost`, use your machine's actual IP (e.g., `192.168.1.50`)

## Advanced Configuration

### Custom System Prompts

You can customize the system prompt through the integration's configuration options to tailor responses for your smart home.

### Multiple LLM Servers

You can add multiple instances of this integration to connect to different LLM servers for different purposes (e.g., fast local model for quick queries, powerful remote model for complex questions).

## Requirements

- Home Assistant 2025.9.0 or newer
- An LLM server with OpenAI-compatible API
- Network connectivity to the LLM server

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

This project is licensed under the MIT License.

## Support

- **Issues**: [GitHub Issues](https://github.com/tylergraf/local_llm/issues)
- **Discussions**: [Home Assistant Community](https://community.home-assistant.io/)

## Credits

Built for the Home Assistant community to enable private, local AI conversations.
