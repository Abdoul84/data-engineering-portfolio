# 🚀 Quick Start Guide - Planet Earth Parody Pipeline

Get your automated content pipeline running in **under 5 minutes**!

## Prerequisites

- Python 3.10+ installed
- FFmpeg installed (for video processing)
- Pexels API key (free, takes 30 seconds to get)

## Step 1: Install Dependencies

```bash
cd 08-content-automation

# Install Python packages
pip install -r requirements.txt

# Install FFmpeg
# macOS:
brew install ffmpeg

# Ubuntu/Debian:
sudo apt-get install ffmpeg

# Windows:
# Download from https://ffmpeg.org/download.html
```

## Step 2: Get Pexels API Key

1. Go to: https://www.pexels.com/api/
2. Click "Get Started" (free)
3. Sign up with email
4. Copy your API key

**Takes 30 seconds!**

## Step 3: Configure Pipeline

```bash
# Copy example config
cp config/config.yaml.example config/config.yaml

# Edit config and add your Pexels API key
# (Use any text editor)
nano config/config.yaml
```

Replace:
```yaml
pexels:
  api_key: "YOUR_PEXELS_API_KEY"
```

With your actual key:
```yaml
pexels:
  api_key: "abc123xyz..."
```

## Step 4: Test It!

### Test 1: Generate a Script (Instant)

```bash
python3 -m src.generation.planet_earth_generator
```

**Expected Output:**
```
🌍 Planet Earth Parody Generator
================================================================================

📝 VOICEOVER SCRIPT:
In the unforgiving African savanna, the majestic lion reveals why Planet Earth
is no vacation spot. Behold as it devours prey with the enthusiasm of a Black 
Friday sale, leaving zero room for polite picnics...
```

✅ **If you see this, scripts are working!**

### Test 2: Generate Audio (5 seconds)

```bash
python3 -m src.media.tts_generator
```

**Expected Output:**
```
🎙️  Text-to-Speech Generator (In-Memory)
⏱️  Estimated duration: 25.2 seconds
🔄 Generating audio...
✅ Success! Generated 45234 bytes
```

✅ **If you see this, TTS is working!**

### Test 3: Fetch Video (30 seconds)

```bash
export PEXELS_API_KEY="your_key_here"
python3 -m src.media.video_fetcher
```

**Expected Output:**
```
🎬 Video Fetcher (In-Memory)
🔍 Searching for: lion in African savanna
✅ Success! Video loaded to memory (12.45 MB)
```

✅ **If you see this, video fetching works!**

## Step 5: Run Full Pipeline (Dry Run)

```bash
python3 -m src.main --save
```

This will:
1. Generate a random script
2. Create TTS voiceover
3. Fetch stock footage
4. Compose final video
5. Save to `/tmp/planet_earth_*.mp4` (for testing)

**Takes 2-3 minutes** (mostly video composition)

**Expected Output:**
```
================================================================================
Starting Planet Earth Parody Pipeline
================================================================================

[1/5] 📝 Generating script...
✅ Generated: lion in African savanna

[2/5] 🎙️  Generating voiceover...
✅ Audio generated: 45.23 KB

[3/5] 🎬 Fetching stock footage...
✅ Video fetched: 12.45 MB

[4/5] 🎬 Composing final video...
   (This may take 1-2 minutes...)
✅ Video composed: 8.67 MB

[5/5] 📤 Uploading to TikTok...
✅ Upload successful (DRY RUN MODE - no actual post)

🧹 Cleaning up memory...
✅ Memory cleaned
```

✅ **Success!** Check `/tmp/` for your video.

## Troubleshooting

### "command not found: python"

Use `python3` instead:
```bash
python3 -m src.main
```

### "FFmpeg not found"

Install FFmpeg:
```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt-get install ffmpeg
```

### "Pexels API key required"

Make sure you:
1. Added your key to `config/config.yaml`
2. Saved the file

### "Video composition failed"

- Ensure FFmpeg is installed and in PATH
- Try: `ffmpeg -version` (should show version info)
- Reinstall moviepy: `pip install --upgrade moviepy imageio-ffmpeg`

## What's Next?

### Enable Automated Posting (Optional)

To post to TikTok automatically:

1. Register app at: https://developers.tiktok.com/
2. Complete OAuth 2.0 flow
3. Add access token to `config/config.yaml`:
   ```yaml
   tiktok:
     access_token: "your_token_here"
   ```
4. Set `dry_run: false` in config
5. Run: `python3 -m src.main`

### Automate with GitHub Actions

See main [README.md](README.md) for GitHub Actions setup instructions.

## Need Help?

- Check main [README.md](README.md) for detailed documentation
- Review individual module tests (they have CLI modes)
- Open an issue on GitHub

---

**That's it!** You now have a fully functional automated content pipeline. 🎉

**Next**: Check out [README.md](README.md) for advanced configuration and deployment options.

