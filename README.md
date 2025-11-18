# Local LLM for Home Assistant

Connect your Home Assistant to external LLM servers on your network (or internet) using a lightweight proxy add-on and custom integration.

## 🎯 Architecture

```
Home Assistant → Proxy Add-on → Your LLM Server (Ollama/llama.cpp/etc.)
          ↓           ↓
    Integration   Port 8080
```

This repository provides:
1. **Proxy Add-on**: Lightweight gateway to your external LLM server
2. **Custom Integration**: Connects to the proxy to provide conversation capabilities

## 🚀 Quick Start

### Step 1: Install the Proxy Add-on

1. In Home Assistant, go to **Settings** → **Add-ons** → **Add-on Store**
2. Click the three dots (⋮) → **Repositories**
3. Add: `https://github.com/tylergraf/local_llm`
4. Find "Local LLM Proxy" and click **Install**
5. Configure with your LLM server details:
   ```json
   {
     "llm_server_url": "http://192.168.1.100:11434",
     "api_key": "",
     "timeout": 120
   }
   ```
6. Click **Start**

### Step 2: Install the Integration

**Via HACS** (recommended):
1. Go to **HACS** → **Integrations**  
2. Click ⋮ → **Custom repositories**
3. Add: `https://github.com/tylergraf/local_llm`
4. Category: **Integration**
5. Download and install
6. Restart Home Assistant

**Manual**:
1. Copy `custom_components/local_llm` to your HA config directory
2. Restart Home Assistant

### Step 3: Configure the Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "Local LLM"
4. Configure:
   - **Base URL**: `http://localhost:8080/v1`
   - **API Key**: (leave blank)
   - **Model**: Your model name (e.g., `llama3.2:3b`)

## ✨ Features

### Proxy Add-on
- 🪶 **Lightweight**: Minimal resource usage (~30-50 MB RAM)
- 🎛️ **Easy Config**: Configure through Home Assistant UI
- 🔄 **Hot Reload**: Change LLM servers without reconfiguring integration
- 🛡️ **Error Handling**: Better timeout and error management
- 🌐 **Network Gateway**: Handles all external LLM communication

### Custom Integration
- 💬 **Full Conversation Agent**: Complete Home Assistant conversation support
- 🎨 **Service Calls**: Use in automations and scripts
- 🔧 **Configurable**: Custom prompts and settings
- 📊 **Status Monitoring**: See connection health

## 🧠 Supported LLM Servers

Works with any OpenAI-compatible API:

- **[Ollama](https://ollama.com/)** - Easy local LLM server
- **[llama.cpp](https://github.com/ggerganov/llama.cpp)** - Lightweight C++ implementation
- **[LM Studio](https://lmstudio.ai/)** - Desktop LLM server with GUI
- **[vLLM](https://github.com/vllm-project/vllm)** - High-performance serving
- **[LocalAI](https://localai.io/)** - Self-hosted OpenAI alternative
- **[text-generation-webui](https://github.com/oobabooga/text-generation-webui)** - Feature-rich web UI
- Any other OpenAI-compatible server

## 💡 Why Use the Proxy Add-on?

### Option A: With Proxy Add-on (Recommended)
```
HA Integration → Proxy Add-on → External LLM Server
```
✅ Easy configuration through UI  
✅ Centralized management  
✅ Change servers without reconfiguring  
✅ Better error handling  

### Option B: Direct Connection
```
HA Integration → External LLM Server
```
❌ Must reconfigure integration to change servers  
❌ Docker networking complexity  
❌ Less flexible  

## 📋 Example Configurations

### Ollama on Your Network
```json
{
  "llm_server_url": "http://192.168.1.50:11434",
  "api_key": "",
  "timeout": 120
}
```

### LM Studio on Another Machine
```json
{
  "llm_server_url": "http://10.0.0.100:1234",
  "api_key": "",
  "timeout": 120
}
```

### Remote Server with Authentication
```json
{
  "llm_server_url": "https://my-llm.example.com",
  "api_key": "your-api-key",
  "timeout": 180
}
```

## 🔧 Setting Up Your LLM Server

### Ollama (Easiest)

**Mac/Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:3b
ollama serve
```

**Windows:**  
Download from [ollama.com](https://ollama.com/)

### LM Studio

1. Download [LM Studio](https://lmstudio.ai/)
2. Download a model
3. Load model and start local server
4. Note the port (usually 1234)

### llama.cpp

```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make
./server -m models/your-model.gguf --host 0.0.0.0 --port 8080
```

## 🐛 Troubleshooting

### Add-on won't start
- Check add-on logs for specific errors
- Verify LLM server URL is correct and reachable
- Test connection: `curl http://your-server:11434/v1/models`

### Integration can't connect to proxy
- Ensure proxy add-on is running
- Check add-on logs
- Verify integration URL is `http://localhost:8080/v1`

### Timeout errors
- Increase timeout in add-on config
- Check if LLM server is overloaded
- Try a smaller/faster model

### Home Assistant in Docker can't reach LAN LLM
The proxy add-on solves this! It handles the networking.

But if needed:
- In add-on config, use your machine's IP instead of localhost
- Example: `http://192.168.1.50:11434` instead of `http://localhost:11434`

## 📁 Repository Structure

```
local_llm/
├── repository.json              # Add-on repository metadata
├── README.md                    # This file
├── INSTALL.md                   # Detailed installation guide
├── custom_components/           # Custom integration
│   └── local_llm/
│       ├── __init__.py
│       ├── conversation.py
│       └── ...
├── local-llm-proxy/            # Proxy add-on
│   ├── config.json
│   ├── Dockerfile
│   ├── proxy_server.py         # Lightweight Python proxy
│   ├── run.sh
│   └── ...
└── hacs.json                   # HACS metadata
```

## 🤝 Contributing

Contributions welcome! Please submit issues and pull requests.

## 📄 License

MIT License

## 🔗 Links

- [Home Assistant](https://www.home-assistant.io/)
- [Ollama](https://ollama.com/)
- [HACS](https://hacs.xyz/)
- [GitHub Issues](https://github.com/tylergraf/local_llm/issues)

