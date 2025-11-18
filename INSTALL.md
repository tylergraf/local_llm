# Installation Instructions

## Step 1: Locate Your Home Assistant Config Directory

Your Home Assistant configuration directory is typically at:
- **Home Assistant OS**: `/config/`
- **Home Assistant Container**: `/config/` (mapped volume)
- **Home Assistant Core**: `~/.homeassistant/` or where you installed it

## Step 2: Copy the Integration

You need to copy the `local_llm` folder into your `custom_components` directory.

### If you're on the Home Assistant machine:

```bash
# Navigate to where you cloned this repo
cd /Users/tylergraf/dev/local_llm

# Copy to Home Assistant config
mkdir -p /path/to/homeassistant/config/custom_components
cp -r custom_components/local_llm /path/to/homeassistant/config/custom_components/
```

### If Home Assistant is on another machine (SSH):

```bash
# From your development machine
cd /Users/tylergraf/dev/local_llm
scp -r custom_components/local_llm user@homeassistant-ip:/config/custom_components/
```

### If using Home Assistant OS via add-ons:

1. Install the "File Editor" or "Samba share" add-on
2. Access your config folder
3. Create a `custom_components` folder if it doesn't exist
4. Copy the `local_llm` folder into it

## Step 3: Verify Installation

Your directory structure should look like this:

```
config/
├── custom_components/
│   └── local_llm/
│       ├── __init__.py
│       ├── manifest.json
│       ├── config_flow.py
│       ├── const.py
│       ├── conversation.py
│       ├── entity.py
│       ├── ai_task.py
│       ├── strings.json
│       ├── services.yaml
│       └── icons.json
└── configuration.yaml
```

## Step 4: Restart Home Assistant

**Important**: You must do a FULL restart, not just reload:

1. Go to **Settings** → **System** → **Hardware**
2. Click the three dots in the top right
3. Select **Restart Home Assistant**
4. Wait for it to fully restart (1-2 minutes)

## Step 5: Clear Browser Cache

Home Assistant caches integration data in your browser. Either:
- Hard refresh: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
- Or open Home Assistant in an incognito/private window

## Step 6: Add the Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration** (bottom right)
3. Search for "Local LLM"
4. If it doesn't appear, go back to Step 3 and verify your installation

## Step 7: Configure

Enter your local LLM server details:
- **Base URL**: e.g., `http://localhost:11434/v1`
- **API Key**: Leave blank if not needed

## Common Issues

### "Local LLM" doesn't appear in integration list

✓ Check file permissions - files must be readable by Home Assistant
✓ Verify manifest.json is valid JSON
✓ Check Home Assistant logs for errors
✓ Make sure you did a full restart (not reload)

### Docker Users

If Home Assistant is in Docker and your LLM is on the host:
- Use `http://host.docker.internal:11434/v1` instead of `localhost`
- Or use the host machine's IP address

