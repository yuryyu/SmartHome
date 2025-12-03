# Google Cloud Speech-to-Text & Text-to-Speech Setup Guide

This guide explains how to set up Google Cloud credentials for the SmartHome voice assistant (`assistant_BOT.py`).

## Overview

The SmartHome project uses two Google Cloud APIs:
- **Cloud Speech-to-Text**: Convert user speech to text
- **Cloud Text-to-Speech**: Convert text responses to speech

## Prerequisites

- Google Cloud account (free tier available: https://cloud.google.com/free)
- Python 3.7+ installed
- Required packages: `google-cloud-texttospeech`, `google-cloud-speech`, `sounddevice`, `scipy`, `soundfile`

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click the project dropdown at the top
3. Click "NEW PROJECT"
4. Enter project name: `SmartHome` (or your preference)
5. Click "CREATE"

## Step 2: Enable Required APIs

1. In the Cloud Console, search for "Speech-to-Text API"
   - Click on it
   - Click "ENABLE"

2. Search for "Text-to-Speech API"
   - Click on it
   - Click "ENABLE"

## Step 3: Create a Service Account

1. In the Cloud Console, go to **IAM & Admin** → **Service Accounts**
2. Click **CREATE SERVICE ACCOUNT**
3. Fill in details:
   - Service account name: `smarthome-voice-bot`
   - Description: `Voice assistant for SmartHome`
4. Click **CREATE AND CONTINUE**
5. Grant roles (click **CONTINUE** for the roles section):
   - **Editor** (or more restrictively: **Cloud Speech Editor** + **Cloud Text-to-Speech Editor**)
6. Click **CONTINUE** then **DONE**

## Step 4: Download the JSON Key

1. In **Service Accounts**, click on the account you just created (`smarthome-voice-bot`)
2. Go to the **KEYS** tab
3. Click **ADD KEY** → **Create new key**
4. Choose **JSON** format
5. Click **CREATE**
   - The JSON file downloads automatically
   - **Keep this file safe** - it contains credentials

## Step 5: Configure SmartHome Project

### Option A: Use Environment Variable (Recommended)

**On Mac/Linux:**

1. Open your shell profile:
   ```bash
   nano ~/.zshrc
   ```

2. Add this line (replace with your actual path):
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/downloaded/key.json"
   ```

3. Save and reload:
   ```bash
   source ~/.zshrc
   ```

4. Verify:
   ```bash
   echo $GOOGLE_APPLICATION_CREDENTIALS
   ```

Then run the bot:
```bash
python assistant_BOT.py
```

**On Windows (Command Prompt):**
```cmd
set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\downloaded\key.json
python assistant_BOT.py
```

**On Windows (PowerShell):**
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\downloaded\key.json"
python assistant_BOT.py
```

### Option B: Use Project Directory (Alternative)

If you prefer not to use environment variables:

1. Run the setup script:
   ```bash
   python setup_google_credentials.py
   ```

2. Choose option 2 (store in project directory)

3. Provide the path to your JSON key when prompted

This will:
- Copy your credentials to `credentials/google-cloud-key.json`
- Update `.gitignore` to prevent accidental commits
- Make credentials load automatically

## Step 6: Install Required Packages

```bash
pip install google-cloud-texttospeech google-cloud-speech
pip install sounddevice scipy soundfile pocketsphinx
```

## Step 7: Test the Setup

```bash
python -c "from speech import STT, TTS; print('✓ Google Cloud imports working')"
```

Or run a quick test:
```python
from speech import TTS

ts = TTS()
response = ts.tts_request("Hello, this is a test")
ts.save2file(response, "test.wav")
print("✓ Text-to-Speech working - check test.wav")
```

## Troubleshooting

### "Google Cloud credentials not found"
- Verify `GOOGLE_APPLICATION_CREDENTIALS` is set:
  ```bash
  echo $GOOGLE_APPLICATION_CREDENTIALS
  ```
- Or ensure `credentials/google-cloud-key.json` exists
- Run `python setup_google_credentials.py` to configure

### "Permission denied" when importing google-cloud modules
- Install packages: `pip install google-cloud-texttospeech google-cloud-speech`
- Verify your service account has the right roles in GCP

### API quota exceeded
- Check your GCP console for usage
- Free tier includes 1M characters/month for TTS, 60 minutes/month for STT
- Monitor usage in **APIs & Services** → **Quotas**

### Audio playback issues
- Install sounddevice: `pip install sounddevice scipy soundfile`
- Check microphone/speaker permissions on your system

## Security Best Practices

1. **Never commit your JSON key to Git**
   - It's already in `.gitignore` - keep it that way
   
2. **Use environment variables in production**
   - Easier to manage across different machines
   - Better for CI/CD pipelines

3. **Rotate keys periodically**
   - In GCP, delete old keys and create new ones

4. **Restrict service account permissions**
   - Don't give "Editor" role - use specific roles instead

## File Locations

After setup, your project structure will look like:
```
SmartHome/
├── speech.py                          (automatically loads credentials)
├── assistant_BOT.py                   (uses speech.py)
├── setup_google_credentials.py        (helper script)
├── credentials/                       (if using local storage)
│   └── google-cloud-key.json         (DO NOT COMMIT)
└── .gitignore                        (includes credentials/)
```

## Next Steps

Once configured, run the voice assistant:
```bash
python assistant_BOT.py
```

The bot will:
1. Greet you with speech
2. Listen for voice commands
3. Process natural language
4. Respond with synthesized speech

Enjoy your smart home voice assistant!
