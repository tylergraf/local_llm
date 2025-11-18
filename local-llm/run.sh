#!/usr/bin/with-contenv bashio

# ==============================================================================
# Home Assistant Add-on: Local LLM Server
# Runs Ollama LLM server
# ==============================================================================

bashio::log.info "Starting Ollama server..."

# Get configuration
DEFAULT_MODEL=$(bashio::config 'default_model')
KEEP_ALIVE=$(bashio::config 'keep_alive')

bashio::log.info "Default model: ${DEFAULT_MODEL}"
bashio::log.info "Keep alive: ${KEEP_ALIVE}"

# Start Ollama server in background
ollama serve &
SERVER_PID=$!

# Wait for server to be ready
bashio::log.info "Waiting for Ollama server to start..."
while ! curl -s http://localhost:11434/api/tags > /dev/null; do
    sleep 1
done

bashio::log.info "Ollama server is ready!"

# Pull default model if specified
if [ -n "${DEFAULT_MODEL}" ]; then
    bashio::log.info "Pulling default model: ${DEFAULT_MODEL}"
    ollama pull "${DEFAULT_MODEL}"
    bashio::log.info "Model ${DEFAULT_MODEL} is ready!"
fi

bashio::log.info "Local LLM Server is fully operational!"

# Keep the container running
wait $SERVER_PID
