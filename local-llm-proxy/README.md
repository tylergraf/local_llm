# Local LLM Proxy Add-on

A lightweight proxy add-on that acts as a gateway between Home Assistant and your external LLM server.

## Why Use This?

- **Easy Configuration**: Configure your LLM server through Home Assistant UI
- **Centralized Management**: One place to manage your LLM connection
- **Network Gateway**: Handles all communication with external LLM servers
- **No Heavy Dependencies**: Lightweight Python proxy, minimal resource usage

## How It Works

```
Home Assistant → Local LLM Proxy Add-on → Your LLM Server (Ollama, etc.)
```

The add-on runs a simple proxy server that:
1. Receives requests from Home Assistant integrations
2. Forwards them to your configured LLM server
3. Returns responses back to Home Assistant

## Installation

1. Add this repository to Home Assistant:
   - Go to **Settings** → **Add-ons** → **Add-on Store**
   - Click ⋮ → **Repositories**
   - Add: `https://github.com/tylergraf/local_llm`

2. Install "Local LLM Proxy"

3. Configure the add-on (see Configuration)

4. Start the add-on

5. Install the Local LLM integration and point it to:
   - `http://localhost:8080/v1` (if using Ollama-compatible API)

## Configuration

### Options

**llm_server_url** (required)
- URL of your external LLM server
- Examples:
  - `http://192.168.1.100:11434` (Ollama on LAN)
  - `http://my-server.local:8080` (llama.cpp)
  - `http://10.0.0.50:1234` (LM Studio)

**api_key** (optional)
- API key if your LLM server requires authentication
- Leave empty for most local servers (Ollama, llama.cpp, etc.)

**timeout** (optional)
- Request timeout in seconds (default: 120)
- Range: 30-300 seconds
- Increase for slower models or complex prompts

### Example Configuration

```json
{
  "llm_server_url": "http://192.168.1.50:11434",
  "api_key": "",
  "timeout": 120
}
```

## Using with the Integration

After starting the add-on:

1. Install the Local LLM custom integration (via HACS or manual)
2. Add the integration in Home Assistant
3. Configure it to connect to the proxy:
   - **Base URL**: `http://localhost:8080/v1`
   - **API Key**: (leave blank)
   - **Model**: Your model name

The integration will talk to the add-on, which forwards to your LAN server.

## Troubleshooting

### Proxy won't start
- Check add-on logs for errors
- Verify the LLM server URL is correct
- Ensure the LLM server is reachable from Home Assistant

### Can't connect to LLM server
- Test connectivity: `ping 192.168.1.100` (your server IP)
- Check firewall settings on LLM server
- Verify the port is correct (11434 for Ollama, 1234 for LM Studio, etc.)

### Timeout errors
- Increase the timeout setting
- Check if your LLM server is overloaded
- Try a smaller/faster model

### Health Check
Visit `http://homeassistant.local:8080/health` to verify the proxy is running.

## Resource Usage

This add-on is very lightweight:
- **Memory**: ~30-50 MB
- **CPU**: Minimal (just forwards requests)
- **Storage**: <10 MB

## Support

- [GitHub Issues](https://github.com/tylergraf/local_llm/issues)
- [Home Assistant Community](https://community.home-assistant.io/)
