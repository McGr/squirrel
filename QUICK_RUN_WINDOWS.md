# Quick Start: Run Squirrel Detector on Windows

## Quick Answer: Is the Model Trained on Squirrels?

**NO** - The current detector is **NOT trained** on squirrels. It's a simple computer vision approach that:
- Looks for **brown/reddish-brown** colors
- Filters by size and shape (aspect ratio)
- **Will detect ANY brown object** (dogs, cats, tree trunks, etc.)
- **Estimated accuracy: 30-50%** (very low for production use)

**For details**: See `docs/DETECTION_METHOD.md`

## Quick Run Guide (PowerShell)

### 1. Activate Environment

```powershell
cd C:\Users\mikem\OneDrive\Documents\Python\cursor\squirrel
.\venv\Scripts\Activate.ps1
```

### 2. Get a Test Video

**Option A: Download from Pexels (Free)**
1. Go to: https://www.pexels.com/videos/search/squirrel/
2. Click a video → Download → Save as `squirrel_test.mp4`
3. Save to project folder or a location you remember

**Option B: Use YouTube Downloader**
```powershell
pip install yt-dlp
yt-dlp -f "best[height<=1080]" "YOUTUBE_URL" -o squirrel_test.mp4
```

### 3. Run the Detector

**Basic command**:
```powershell
squirrel-detector --video-path "squirrel_test.mp4" --debug
```

**With custom settings** (better for testing):
```powershell
squirrel-detector --video-path "squirrel_test.mp4" --confidence-threshold 0.3 --debug
```

### 4. What You'll See

- **Debug window**: Shows video with green box (center region) and red/green boxes (detections)
- **Console**: Logs when "squirrel" is detected
- **Press 'q'**: To quit

## Example Commands

```powershell
# Navigate to project
cd C:\Users\mikem\OneDrive\Documents\Python\cursor\squirrel

# Activate venv
.\venv\Scripts\Activate.ps1

# Run with test video (adjust path as needed)
squirrel-detector --video-path "C:\Users\mikem\Videos\squirrel.mp4" --debug

# Or if video is in project folder
squirrel-detector --video-path "squirrel_test.mp4" --confidence-threshold 0.3 --debug
```

## Important Notes

⚠️ **This will detect ANY brown object**, not just squirrels
⚠️ **Low accuracy** - prototype/development tool only
⚠️ **For production**, you'd need a real ML model (YOLO, TensorFlow, etc.)

## Full Documentation

- **Running on Windows**: `docs/RUNNING_ON_WINDOWS.md`
- **Detection Method**: `docs/DETECTION_METHOD.md`
- **Test Videos**: `docs/TEST_VIDEOS.md`
