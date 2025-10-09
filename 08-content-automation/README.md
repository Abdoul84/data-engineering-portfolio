# 🌍 Planet Earth Parody - Automated Content Pipeline

**Why I Wouldn't Recommend Planet Earth** - An automated content generation pipeline that creates dark humor nature documentary parodies in the style of BBC's Planet Earth, complete with AI voiceover, stock footage, and automated posting to TikTok.

## 🎯 Project Overview

This project demonstrates advanced data engineering and automation skills by building a **zero-storage content pipeline** that:

1. **Generates** creative scripts using randomized templates
2. **Synthesizes** voiceover audio with gTTS (British accent)
3. **Fetches** stock footage from Pexels API
4. **Composes** final videos with text overlays and filters
5. **Posts** directly to TikTok via API

**All processing happens in-memory** - no files saved locally (zero storage footprint).

## 🏗️ Architecture

```
Script Generator (Python)
    ↓
gTTS Audio (in-memory) → Pexels Video (streaming) → MoviePy Composition
    ↓
TikTok API (direct upload)
```

### Key Technical Features

- **In-Memory Processing**: All media processing uses BytesIO streams
- **API Integration**: Pexels (video), TikTok (posting), gTTS (audio)
- **Automated Scheduling**: GitHub Actions runs daily at 10 AM UTC
- **Zero Storage**: No local file saves (except optional /tmp for testing)
- **Error Handling**: Robust retry logic and fallback mechanisms

## 📦 Tech Stack

| Component | Technology | Cost |
|-----------|-----------|------|
| **Script Generation** | Python | Free |
| **Text-to-Speech** | gTTS | Free (unlimited) |
| **Stock Footage** | Pexels API | Free (200 req/hour) |
| **Video Editing** | MoviePy | Free |
| **Automation** | GitHub Actions | Free (2,000 min/month) |
| **Social Media** | TikTok API | Free (requires OAuth) |

**Total Cost**: $0/month 💰

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- FFmpeg (for video processing)
- Pexels API key (free)
- TikTok Developer account (optional, for real posting)

### Installation

```bash
cd 08-content-automation

# Install dependencies
pip install -r requirements.txt

# Install FFmpeg (macOS)
brew install ffmpeg

# Install FFmpeg (Ubuntu)
sudo apt-get install ffmpeg
```

### Configuration

1. **Copy example config:**
   ```bash
   cp config/config.yaml.example config/config.yaml
   ```

2. **Add your Pexels API key:**
   - Register at: https://www.pexels.com/api/
   - Add key to `config/config.yaml`:
     ```yaml
     pexels:
       api_key: "YOUR_KEY_HERE"
     ```

3. **Optional - TikTok Setup:**
   - Register app at: https://developers.tiktok.com/
   - Complete OAuth 2.0 flow
   - Add access token to config

### Usage

#### Test Individual Components

```bash
# Test script generation
python -m src.generation.planet_earth_generator

# Test TTS (saves to /tmp for testing)
python -m src.media.tts_generator

# Test video fetching (requires Pexels API key)
export PEXELS_API_KEY="your_key"
python -m src.media.video_fetcher

# Test TikTok upload (dry run)
python -m src.posting.tiktok_uploader
```

#### Run Full Pipeline

```bash
# Dry run (no actual posting)
python -m src.main

# Save output to /tmp for inspection
python -m src.main --save

# Generate multiple videos
python -m src.main --batch 3
```

#### Expected Output

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

================================================================================
Pipeline execution completed
================================================================================
```

## 🤖 Automated Scheduling

### GitHub Actions Setup

The pipeline runs automatically daily at 10 AM UTC via GitHub Actions.

**Setup Instructions:**

1. **Add API Keys as Secrets:**
   - Go to: Repository Settings → Secrets and variables → Actions
   - Add:
     - `PEXELS_API_KEY` (required for video fetching)
     - `TIKTOK_ACCESS_TOKEN` (optional, enables real posting)

2. **Enable Workflow:**
   - Go to Actions tab
   - Enable "Planet Earth Parody - Automated Content Generation"

3. **Manual Trigger (Optional):**
   - Go to Actions → Planet Earth Parody workflow
   - Click "Run workflow"
   - Choose whether to save output as artifact

### Workflow Features

- ✅ Runs daily at 10 AM UTC
- ✅ Manual trigger available
- ✅ Saves lightweight JSON logs (<1KB per run)
- ✅ Optional: Save video artifacts for testing
- ✅ Automatic retry on transient failures
- ✅ Notification on success/failure

## 📁 Project Structure

```
08-content-automation/
├── config/
│   ├── config.yaml           # Main configuration
│   └── config.yaml.example   # Example config
├── logs/                     # Lightweight JSON logs
├── src/
│   ├── generation/
│   │   └── planet_earth_generator.py  # Script generation
│   ├── media/
│   │   ├── tts_generator.py          # Text-to-speech
│   │   ├── video_fetcher.py          # Stock footage
│   │   └── video_composer.py         # Video assembly
│   ├── posting/
│   │   └── tiktok_uploader.py        # TikTok API
│   └── main.py              # Main orchestrator
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🎬 Example Content

### Sample Script

> "In the unforgiving African savanna, the majestic lion reveals why Planet Earth is no vacation spot. Behold as it devours prey with the enthusiasm of a Black Friday sale, leaving zero room for polite picnics. I would not recommend this blue marble—unless you fancy a front-row seat to nature's unfiltered chaos. Proceed... if you dare."

### Sample Caption

```
🌍 Why I Wouldn't Recommend Planet Earth: Lion Edition

In the African savanna, nature shows no mercy... 😈

#PlanetEarthParody #WhyNotRecommend #NatureHorror #AttenboroughVibes 
#Wildlife #DarkHumor #NatureDocumentary #BBCEarth #TikTokNature #LionFacts
```

### Visual Style

- **Format**: Vertical 9:16 (TikTok/Reels)
- **Duration**: 30 seconds
- **Effects**: Dark filter, high contrast, desaturated
- **Overlay**: "NOT RECOMMENDED" in bold red text
- **Vibe**: Nature horror trailer meets BBC documentary

## 🔧 Troubleshooting

### Common Issues

**1. FFmpeg not found**
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# Download from: https://ffmpeg.org/download.html
```

**2. Pexels API limit reached**
- Free tier: 200 requests/hour
- Wait 1 hour or upgrade to Pro

**3. MoviePy errors**
- Ensure FFmpeg is installed and in PATH
- Try: `pip install --upgrade moviepy imageio-ffmpeg`

**4. Memory issues**
- Videos are processed in RAM (typically 10-50 MB)
- Ensure at least 2GB free RAM
- Streams are cleaned up after each stage

### Debug Mode

Enable verbose logging:

```python
# In config/config.yaml
logging:
  level: "DEBUG"
```

Or via environment variable:
```bash
export PYTHONLOGLEVEL=DEBUG
python -m src.main
```

## 📊 Performance Metrics

Typical execution time:
- Script generation: <1 second
- TTS audio: 2-5 seconds
- Video fetch: 10-30 seconds (depends on file size)
- Video composition: 60-120 seconds
- Upload: 10-20 seconds

**Total**: ~2-3 minutes per video

Memory usage:
- Peak: 50-100 MB (during video composition)
- After cleanup: ~10 MB

## 🎓 Learning Outcomes

This project demonstrates:

1. **API Integration**: Pexels, TikTok, gTTS
2. **In-Memory Processing**: BytesIO streams, zero local storage
3. **Automated Pipelines**: GitHub Actions scheduling
4. **Media Processing**: MoviePy video editing
5. **Error Handling**: Robust retry and fallback logic
6. **Configuration Management**: YAML configs, environment variables
7. **Logging**: Lightweight JSON logs for monitoring

## 📝 License

This project is part of a data engineering portfolio and is provided for educational purposes.

## 🙏 Credits

- **Inspiration**: BBC's Planet Earth documentary series
- **Stock Footage**: Pexels (https://www.pexels.com)
- **Text-to-Speech**: gTTS (Google Text-to-Speech)
- **Video Processing**: MoviePy

---

**Developed by**: Abdoul Top  
**Portfolio**: https://github.com/Abdoul84/data-engineering-portfolio

