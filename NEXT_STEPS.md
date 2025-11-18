# Next Steps: Publishing Your Add-on Repository

Your repository has been successfully converted to a Home Assistant add-on repository! Here's what to do next:

## 1. Review the Structure

Your repository now contains:

```
local_llm/
├── repository.json              # Repository metadata
├── README.md                    # Main documentation
├── INSTALL.md                   # Installation guide (for custom integration)
├── hacs.json                    # HACS metadata (for custom integration)
├── custom_components/           # Custom integration (still available)
│   └── local_llm/
└── local-llm/                   # Add-on directory
    ├── config.json              # Add-on configuration
    ├── Dockerfile               # Docker build file
    ├── run.sh                   # Startup script
    ├── README.md                # Add-on documentation
    ├── DOCS.md                  # UI documentation
    ├── CHANGELOG.md             # Version history
    ├── ICONS.md                 # Icon guidelines
    ├── icon.png                 # Add-on icon (placeholder)
    └── logo.png                 # Add-on logo (placeholder)
```

## 2. Add Icons (Optional but Recommended)

Replace the placeholder `icon.png` and `logo.png` files in the `local-llm/` directory. See `local-llm/ICONS.md` for guidelines.

## 3. Commit and Push Changes

```bash
# Stage all new files
git add .

# Commit the changes
git commit -m "Convert to Home Assistant add-on repository

- Add repository.json for add-on store
- Create local-llm add-on with Ollama
- Update README with installation instructions
- Maintain backward compatibility with custom integration"

# Push to GitHub
git push origin main
```

## 4. Test the Add-on Repository

1. In Home Assistant, go to **Settings** → **Add-ons** → **Add-on Store**
2. Click the three dots (⋮) in the top right
3. Select **Repositories**
4. Add: `https://github.com/tylergraf/local_llm`
5. You should now see "Local LLM Server" in the add-on store

## 5. Install and Test

1. Click on "Local LLM Server"
2. Click **Install**
3. Configure the add-on:
   ```json
   {
     "default_model": "llama3.2:1b",
     "keep_alive": "5m"
   }
   ```
4. Click **Start**
5. Check the logs to see the model downloading
6. Once running, test the API at `http://localhost:11434/v1`

## 6. Configure Home Assistant Conversation

### Option A: Using OpenAI Conversation Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "OpenAI Conversation"
4. Configure:
   - **API Key**: `sk-dummy` (required but not used)
   - Click **Advanced** and set:
     - **Base URL**: `http://localhost:11434/v1`
     - **Model**: `llama3.2:1b` (same as add-on config)

### Option B: Using Local LLM Custom Integration

If you still have the custom integration installed:

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "Local LLM"
4. Enter base URL: `http://localhost:11434/v1`

## 7. Use in Automations

You can now use the LLM in automations:

```yaml
service: conversation.process
data:
  text: "What's the weather like today?"
  agent_id: conversation.openai  # Or your configured agent
```

## 8. Share with the Community (Optional)

Consider sharing your add-on:

1. **Home Assistant Community Forum**
   - Post in [Share Your Projects](https://community.home-assistant.io/c/projects/25)
   
2. **Reddit**
   - r/homeassistant
   - r/homeassistantaddons

3. **Add to awesome-home-assistant**
   - Submit PR to [awesome-home-assistant](https://github.com/frenck/awesome-home-assistant)

## Troubleshooting

### "Not a valid add-on repository" error

- Make sure `repository.json` exists in the root
- Verify `local-llm/config.json` exists
- Check JSON files are valid (no syntax errors)
- Push changes to GitHub before testing

### Add-on doesn't appear

- Refresh the add-on store page
- Check browser console for errors
- Verify the repository URL is correct in GitHub

### Model download fails

- Ensure sufficient disk space (5GB+ per model)
- Check internet connectivity
- Try a smaller model first
- Check add-on logs for specific errors

## Need Help?

- [Home Assistant Add-on Documentation](https://developers.home-assistant.io/docs/add-ons)
- [Ollama Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [GitHub Issues](https://github.com/tylergraf/local_llm/issues)

---

**Your add-on repository is ready! 🎉**
