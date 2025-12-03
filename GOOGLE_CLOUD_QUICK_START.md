# Google Cloud Setup - Quick Reference

## TL;DR

### 1. Get Credentials (5 minutes)
- Go to https://console.cloud.google.com
- Create project → Enable Speech-to-Text & Text-to-Speech APIs
- Create Service Account (`smarthome-voice-bot`)
- Download JSON key

### 2. Configure Project (2 ways)

**Option A: Environment Variable** (Mac/Linux)
```bash
echo 'export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"' >> ~/.zshrc
source ~/.zshrc
python assistant_BOT.py
```

**Option B: Project Directory**
```bash
python setup_google_credentials.py
# Choose option 2, provide JSON path
# Done - credentials copied to credentials/google-cloud-key.json
```

### 3. Install Packages
```bash
pip install google-cloud-texttospeech google-cloud-speech sounddevice scipy soundfile
```

### 4. Test
```bash
python -c "from speech import TTS; print('✓ Working')"
```

## Files Changed

| File | Change | Why |
|------|--------|-----|
| `speech.py` | Removed hardcoded Windows path, added dynamic loading | Works on Mac/Linux now |
| `.gitignore` | Added `credentials/` & `*.json` | Prevents credential leaks |
| `setup_google_credentials.py` | New helper script | Interactive setup wizard |
| `GOOGLE_CLOUD_SETUP.md` | Comprehensive guide | User documentation |
| `.github/copilot-instructions.md` | Updated speech module section | AI agent guidance |

## Detailed Setup Guide

See **GOOGLE_CLOUD_SETUP.md** for step-by-step instructions with screenshots.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "credentials not found" | Run `python setup_google_credentials.py` |
| Import error for google-cloud | Run `pip install google-cloud-texttospeech google-cloud-speech` |
| Microphone/speaker issues | Check system permissions, install `sounddevice` |
| API quota exceeded | Check GCP console, free tier has limits |

## What the Code Now Does

**Before:** Hardcoded Windows path → broke on Mac
```python
credential_path = "C:\\Users\\yuzba\\Documents\\GitHub\\nlp-2021-494bf1773dbc.json"
```

**After:** Tries environment variable → falls back to local directory
```python
def _setup_credentials():
    # Check GOOGLE_APPLICATION_CREDENTIALS env var
    # Fall back to credentials/google-cloud-key.json
    # Raise helpful error if not found
```

This means:
- ✓ Works on Mac, Linux, Windows
- ✓ Works with environment variables
- ✓ Works with local credential files
- ✓ Clear error messages if setup fails
