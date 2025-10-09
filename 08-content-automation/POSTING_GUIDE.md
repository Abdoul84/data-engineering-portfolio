# 📱 Content Posting Guide

## 🎯 Recommended Workflow: Semi-Automated

The pipeline generates videos automatically, but posting is **manual** (by design). This approach:
- ✅ Avoids TikTok Business verification hassle
- ✅ Gives you creative control before posting
- ✅ Still saves 90% of the work
- ✅ Works for all platforms (TikTok, Instagram, YouTube)

---

## 📹 Step-by-Step: From Generation to Post

### Step 1: Generate Video (Automated - 2 minutes)

```bash
cd 08-content-automation

# Generate video with caption
python3 -m src.main --save
```

**Output**:
```
✅ Video saved to: /tmp/planet_earth_20251009_173045.mp4
📝 Caption:
🌍 Why I Wouldn't Recommend Planet Earth: Lion Edition

In the African savanna, nature shows no mercy... 😈

#PlanetEarthParody #WhyNotRecommend #NatureHorror #AttenboroughVibes 
#Wildlife #DarkHumor #NatureDocumentary #BBCEarth #TikTokNature #LionFacts
```

### Step 2: Review Video (30 seconds)

```bash
# Open the video to review
open /tmp/planet_earth_20251009_173045.mp4
```

Check:
- ✅ Video quality
- ✅ Audio sync
- ✅ Text overlay visible
- ✅ Overall vibe

### Step 3: Post to Platform (1 minute)

#### Option A: TikTok (Mobile App)

1. **AirDrop/Transfer** video to your phone:
   - macOS: AirDrop from Finder
   - Windows: Email or cloud storage
   - Or use USB cable

2. **Open TikTok App**:
   - Tap "+" button
   - Select "Upload"
   - Choose the video

3. **Paste Caption**:
   - Copy caption from terminal output
   - Paste into TikTok description
   - Hashtags are already included

4. **Post Settings**:
   - Cover: Auto-select or choose frame
   - Who can view: Public
   - Allow comments: Yes
   - Allow duet/stitch: Your choice

5. **Post!** 🎉

#### Option B: Instagram Reels (Mobile App)

1. **Transfer** video to phone (same as TikTok)

2. **Open Instagram**:
   - Tap "+" button
   - Select "Reel"
   - Upload video

3. **Edit** (if needed):
   - Trim to 30 seconds
   - Add music (optional)
   - Adjust cover

4. **Caption**:
   - Paste generated caption
   - Instagram auto-detects hashtags

5. **Share to Feed**: Post! 🎉

#### Option C: YouTube Shorts (Desktop or Mobile)

1. **Go to**: https://studio.youtube.com/

2. **Upload**:
   - Click "Create" → "Upload videos"
   - Select video from `/tmp/`

3. **Video Details**:
   - **Title**: "Why I Wouldn't Recommend Planet Earth: [Animal] Edition"
   - **Description**: Paste generated caption
   - **Audience**: Not made for kids (dark humor)

4. **Shorts Settings**:
   - Check "This is a Short"
   - Thumbnail: Auto-generated

5. **Publish**: Post! 🎉

---

## 🤖 Future: Full Automation (Optional)

If you want **100% automation** later, you can add:

### Option 1: YouTube Shorts API (Easiest)

**Setup** (30 minutes):
```bash
# 1. Google Cloud Console
# - Create project
# - Enable YouTube Data API v3
# - Create OAuth credentials

# 2. Install SDK
pip install google-auth-oauthlib google-api-python-client

# 3. Implement uploader
# See: src/posting/youtube_uploader.py (template below)
```

**No business verification needed!**

### Option 2: Twitter/X API (Also Easy)

**Setup** (15 minutes):
```bash
# 1. Apply at: https://developer.twitter.com/
# 2. Get API keys (usually approved same day)
# 3. Install tweepy
pip install tweepy

# 4. Upload videos with Twitter API v2
```

**Free tier**: 1,500 tweets/month

### Option 3: TikTok API (Hard Mode)

**Only if you have**:
- ✅ Registered business entity
- ✅ Business documents (registration, tax ID)
- ✅ 1-2 weeks to wait for approval
- ✅ Patience for TikTok's approval process

**See**: `API_SETUP.md` for full TikTok Business verification process

---

## 📊 Time Comparison

| Step | Manual | Fully Automated |
|------|--------|-----------------|
| **Script Writing** | 10 min | ✅ Automated (1 sec) |
| **Voiceover Recording** | 5 min | ✅ Automated (5 sec) |
| **Finding Footage** | 20 min | ✅ Automated (30 sec) |
| **Video Editing** | 30 min | ✅ Automated (2 min) |
| **Caption Writing** | 5 min | ✅ Automated (1 sec) |
| **Posting** | 1 min | 🟡 Manual (30 sec-1 min) |
| **TOTAL** | ~70 min | ~4 minutes |

**Time saved**: 66 minutes per video (94% automation!)

---

## 🎨 Pro Tips

### Content Quality

1. **Preview First**: Always watch before posting
2. **Best Times**: Post at peak hours (7-9 PM local time)
3. **Consistency**: Post daily or every other day
4. **Engagement**: Respond to comments quickly

### Caption Optimization

The auto-generated captions are good, but you can:
- Add emoji reactions 😱🦁🌍
- Include call-to-action ("Which animal next?")
- Tag relevant accounts (nature photographers)
- Use trending sounds (if available)

### Multi-Platform Strategy

Post the **same video** to multiple platforms:
```bash
# Generate once
python3 -m src.main --save

# Post to:
1. TikTok (max reach)
2. Instagram Reels (secondary audience)
3. YouTube Shorts (long-term discovery)
4. Twitter/X (bonus traffic)
```

**4x the exposure, 5 minutes total work!**

---

## 🔧 Troubleshooting

### "Video too large for TikTok"

TikTok limit: 287 MB (our videos are ~8-15 MB, always safe)

If it's too large:
```bash
# Re-encode with smaller bitrate
ffmpeg -i /tmp/planet_earth_*.mp4 -b:v 1M -b:a 128k output.mp4
```

### "Caption too long"

Limits:
- TikTok: 2,200 characters (we're ~400, always safe)
- Instagram: 2,200 characters (we're safe)
- YouTube: 5,000 characters (plenty of room)

### "Video not uploading"

Check:
- ✅ File format: MP4 (our output)
- ✅ Resolution: 1080×1920 (our output)
- ✅ Duration: <60 seconds (ours is 30s)
- ✅ File size: <287 MB (ours is ~10 MB)

All specs are already correct! ✅

---

## 📈 Growth Strategy

### Week 1-2: Test & Learn
- Post 1 video/day
- Test different animals/locations
- Track which videos perform best

### Week 3-4: Optimize
- Focus on high-performing content types
- Experiment with posting times
- Engage with comments

### Month 2+: Scale
- Post 2-3 videos/day (multi-platform)
- Build content calendar
- Analyze metrics
- Consider automation (YouTube/Twitter APIs)

---

## 🎯 Automation Roadmap

If you want to add full automation later:

**Phase 1** (Current): ✅ Complete
- Script generation
- Video production
- Manual posting

**Phase 2** (Optional - 2 hours):
- Add YouTube Shorts API
- Automated posting to YouTube
- Keep manual TikTok/Instagram

**Phase 3** (Optional - 1 hour):
- Add Twitter/X API
- Automated cross-posting
- Still manual TikTok/Instagram

**Phase 4** (Only if needed - 2 weeks):
- TikTok Business verification
- Full automation across all platforms

---

## 💡 Bottom Line

**Current setup is perfect for**:
- ✅ Portfolio projects
- ✅ Personal content creation
- ✅ Testing and iterating
- ✅ Learning content automation

**You save 94% of the time** while maintaining quality control.

The remaining 6% (manual posting) is:
- Quick (1 minute)
- Easy (copy/paste)
- Worth it (no API hassles)

**Don't overcomplicate it!** This workflow works great. 🎉

---

**Questions?** See `README.md` for full documentation or `API_SETUP.md` for automation options.

