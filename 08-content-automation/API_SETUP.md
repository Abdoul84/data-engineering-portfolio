# 🔑 API Setup Guide

Complete guide to setting up all API integrations for the Planet Earth Parody Pipeline.

## 📊 Overview

| API | Required? | Cost | Rate Limit | Purpose |
|-----|-----------|------|------------|---------|
| **Pexels** | ✅ Yes | Free | 200 req/hour | Stock video footage |
| **gTTS** | ✅ Yes | Free | Unlimited | Text-to-speech voiceover |
| **TikTok** | ⚠️ Optional | Free | Varies | Automated posting |

## 1. Pexels API (Required)

### Why We Need It
- Provides high-quality stock footage for our videos
- Free tier is generous (200 requests/hour = 200 videos/day)
- No credit card required

### Setup Steps

1. **Go to Pexels API:**
   - Visit: https://www.pexels.com/api/
   - Click "Get Started"

2. **Create Account:**
   - Sign up with email (takes 30 seconds)
   - Verify your email

3. **Get Your API Key:**
   - Once logged in, go to: https://www.pexels.com/api/
   - Your API key is displayed immediately
   - Copy it (looks like: `abc123xyz...`)

4. **Add to Config:**
   ```yaml
   # config/config.yaml
   pexels:
     api_key: "YOUR_KEY_HERE"  # Paste your actual key
   ```

5. **Test It:**
   ```bash
   export PEXELS_API_KEY="your_key_here"
   python3 -m src.media.video_fetcher
   ```

### Rate Limits

- **Free Tier**: 200 requests per hour
- **What Counts**: Each video search/download = 1 request
- **Our Usage**: 1 request per video generated
- **Enough For**: 200 videos/day (way more than we need!)

### Best Practices

- ✅ Cache results when possible
- ✅ Don't make unnecessary requests
- ✅ Be specific with search queries
- ⚠️ Don't share your API key publicly

### Troubleshooting

**"Invalid API key"**
- Make sure you copied the entire key
- Check for extra spaces or newlines
- Try regenerating your key on Pexels

**"Rate limit exceeded"**
- Wait 1 hour for reset
- Free tier: 200 requests/hour
- Consider spacing out requests

## 2. gTTS (Google Text-to-Speech)

### Why We Need It
- Generates natural-sounding voiceovers
- Completely free, no API key needed
- British accent option for BBC documentary vibe

### Setup Steps

**That's it! No setup needed.**

gTTS is already included in `requirements.txt` and works out of the box.

### Features

- **Languages**: 100+ supported
- **Accents**: British (co.uk), American (com), Australian (com.au), etc.
- **Rate Limits**: None (unlimited usage)
- **Quality**: Natural-sounding MP3 audio

### Customization

```python
# In src/media/tts_generator.py
tts = TTSGenerator(
    lang='en',      # Language
    tld='co.uk',    # British accent (BBC style)
    slow=False      # Normal speed
)
```

Available accents:
- `co.uk` - British (our default)
- `com` - American
- `com.au` - Australian
- `co.in` - Indian
- `ca` - Canadian

### Test It

```bash
python3 -m src.media.tts_generator
```

## 3. TikTok API (Optional)

### Why It's Optional
- Pipeline works fine in "dry run" mode without it
- You can manually upload generated videos
- Real posting requires TikTok Developer approval

### When You Need It
- ✅ To enable fully automated posting
- ✅ To schedule posts via GitHub Actions
- ❌ Not needed for video generation
- ❌ Not needed for testing

### Setup Steps (Advanced)

**⚠️ Note**: TikTok API requires developer approval and OAuth setup. For most users, dry run mode is sufficient.

#### Option A: Dry Run Mode (Recommended)

Leave default config:
```yaml
# config/config.yaml
tiktok:
  access_token: "YOUR_TIKTOK_ACCESS_TOKEN"

processing:
  dry_run: true  # No actual posting
```

Videos will be generated but not posted. You can:
- Save to `/tmp` with `--save` flag
- Manually upload to TikTok
- Review before posting

#### Option B: Real TikTok API (Advanced Users)

**Prerequisites:**
- TikTok Developer account
- Registered application
- OAuth 2.0 knowledge
- User consent for posting

**Steps:**

1. **Apply for TikTok Developer Access:**
   - Visit: https://developers.tiktok.com/
   - Click "Register"
   - Fill out application (approval may take days/weeks)

2. **Create an App:**
   - Go to TikTok Developer Portal
   - Create new application
   - Request "Content Posting API" access
   - Provide app description and use case

3. **Configure OAuth 2.0:**
   - Set redirect URL
   - Note your Client ID and Client Secret
   - Implement OAuth flow (see TikTok docs)

4. **Get Access Token:**
   - User must authorize your app
   - Exchange authorization code for access token
   - Token typically expires after 24 hours

5. **Add to Config:**
   ```yaml
   # config/config.yaml
   tiktok:
     access_token: "act.your_token_here"
   
   processing:
     dry_run: false  # Enable real posting
   ```

**Important Notes:**
- TikTok API access requires approval (not instant)
- Access tokens expire (need refresh token flow)
- Rate limits vary by approval tier
- Some regions may have restrictions

**For most users, we recommend:**
1. Use dry run mode
2. Generate videos locally
3. Manually upload to TikTok
4. Skip the OAuth complexity

## Configuration Summary

### Minimal Setup (Recommended)

```yaml
# config/config.yaml

# Only this is required:
pexels:
  api_key: "your_pexels_key_here"

# Leave these as defaults:
tiktok:
  access_token: "YOUR_TIKTOK_ACCESS_TOKEN"

content:
  video_duration: 30
  posting_frequency: "daily"

processing:
  in_memory_only: true
  cleanup_streams: true
  dry_run: true  # No actual TikTok posting
```

### Full Setup (Advanced)

```yaml
# config/config.yaml

pexels:
  api_key: "your_pexels_key_here"

tiktok:
  access_token: "act.your_tiktok_token_here"

content:
  video_duration: 30
  posting_frequency: "daily"

processing:
  in_memory_only: true
  cleanup_streams: true
  dry_run: false  # Enable real posting

logging:
  level: "INFO"
  save_logs: true
  log_file: "logs/pipeline.json"
```

## Environment Variables (Alternative)

Instead of `config.yaml`, you can use environment variables:

```bash
export PEXELS_API_KEY="your_key_here"
export TIKTOK_ACCESS_TOKEN="your_token_here"
```

Pipeline will automatically detect and use them.

## Security Best Practices

### ✅ Do:
- Keep API keys in `config.yaml` (gitignored)
- Use environment variables in CI/CD
- Rotate keys periodically
- Use GitHub Secrets for automation

### ❌ Don't:
- Commit `config.yaml` with real keys
- Share keys publicly
- Hard-code keys in Python files
- Post keys in GitHub issues/PRs

## Testing Your Setup

Run this to verify all APIs:

```bash
# Test everything at once
python3 -m src.main --save

# Or test individually:
python3 -m src.generation.planet_earth_generator  # No API needed
python3 -m src.media.tts_generator                # No API needed
export PEXELS_API_KEY="your_key"
python3 -m src.media.video_fetcher                # Pexels API
python3 -m src.posting.tiktok_uploader            # TikTok (dry run)
```

## Need Help?

**Pexels Issues:**
- Check: https://www.pexels.com/api/documentation/
- Support: https://www.pexels.com/support

**gTTS Issues:**
- Docs: https://gtts.readthedocs.io/
- GitHub: https://github.com/pndurette/gTTS

**TikTok Issues:**
- Developer Portal: https://developers.tiktok.com/
- Documentation: https://developers.tiktok.com/doc/

---

**Quick Start**: Most users only need Pexels API (free, takes 30 seconds). Everything else works without API keys!

