#!/usr/bin/env bash
set -e

CONFIG_PATH=/data/options.json

echo "Starting Local LLM Proxy..."

# Read configuration
LLM_SERVER_URL=$(jq --raw-output '.llm_server_url' $CONFIG_PATH)
API_KEY=$(jq --raw-output '.api_key // empty' $CONFIG_PATH)
TIMEOUT=$(jq --raw-output '.timeout' $CONFIG_PATH)

# Export for proxy_server.py
export LLM_SERVER_URL="$LLM_SERVER_URL"
export API_KEY="$API_KEY"
export TIMEOUT="$TIMEOUT"

echo "══════════════════════════════════════════"
echo " Local LLM Proxy Configuration"
echo "══════════════════════════════════════════"
echo "  Target Server: $LLM_SERVER_URL"
echo "  Timeout: ${TIMEOUT}s"
echo "  Proxy Port: 8080"
echo "══════════════════════════════════════════"

# Start proxy server
exec python3 /app/proxy_server.py
