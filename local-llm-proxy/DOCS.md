# Local LLM Proxy

This add-on provides a lightweight proxy gateway to external LLM servers on your network.

## Quick Start

1. Configure your external LLM server URL
2. Start the add-on
3. Use `http://localhost:8080/v1` in the Local LLM integration

## Configuration

### llm_server_url

The URL of your external LLM server.

**Examples:**
- `http://192.168.1.100:11434` - Ollama on your network
- `http://10.0.0.50:1234` - LM Studio
- `http://my-server.local:8080` - llama.cpp server

### api_key

Optional API key for authentication. Leave empty for local servers like Ollama.

### timeout

Request timeout in seconds (30-300). Default is 120 seconds.

Increase this if you're using:
- Slower models
- Long conversations
- Complex prompts

## How to Use

After the add-on is running, it exposes a proxy API at port 8080.

Configure the Local LLM integration to use:
```
http://localhost:8080/v1
```

All requests will be forwarded to your configured LLM server.

## Architecture

```
┌─────────────────┐
│ Home Assistant  │
│   Integration   │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Proxy Add-on   │  (This add-on)
│   Port: 8080    │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Your LLM       │
│  Server (LAN)   │  Ollama/llama.cpp/etc
└─────────────────┘
```

## Benefits

- **Easy Updates**: Change LLM server without reconfiguring integration
- **Centralized Config**: One place to manage connection settings
- **Error Handling**: Better error messages and timeout management
- **Flexibility**: Switch between different LLM servers easily
