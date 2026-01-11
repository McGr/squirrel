# Running Squirrel Detector on Windows (PowerShell)

This guide explains how to run the Squirrel Detector on Windows 11 using PowerShell.

## Prerequisites

1. **Python 3.10+ installed** (preferably 3.13)
2. **Virtual environment activated** (if using one)
3. **Package installed** in development mode
4. **Test video file** (MP4 format recommended)

## Step 1: Activate Virtual Environment

If you have a virtual environment set up:

```powershell
# Navigate to project directory
cd C:\Users\mikem\OneDrive\Documents\Python\cursor\squirrel

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

If PowerShell execution policy blocks the script:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Step 2: Verify Installation

Check that the package is installed:

```powershell
# Check if package is installed
python -c "import squirrel; print(squirrel.__version__)"

# Check if command is available
squirrel-detector --help
```

If not installed, install it:
```powershell
pip install -e .
```

## Step 3: Get a Test Video

You need a video file to test with. See `docs/TEST_VIDEOS.md` for sources.

**Quick option**: Download from Pexels (free, no attribution needed):
1. Go to https://www.pexels.com/videos/
2. Search for "squirrel" or "garden squirrel"
3. Download a video (preferably MP4 format)
4. Save it to your project directory or a known location

**Example locations**:
- `C:\Users\mikem\Videos\squirrel.mp4`
- `C:\Users\mikem\OneDrive\Documents\Python\cursor\squirrel\test_videos\squirrel.mp4`

## Step 4: Run the Detector

### Basic Command (with debug window)

```powershell
squirrel-detector --video-path "C:\path\to\your\squirrel_video.mp4" --debug
```

### With Custom Settings

```powershell
squirrel-detector `
  --video-path "C:\path\to\your\squirrel_video.mp4" `
  --gpio-pin 18 `
  --confidence-threshold 0.3 `
  --center-threshold 0.5 `
  --debug
```

### Without Debug Window (for logging only)

```powershell
squirrel-detector --video-path "C:\path\to\your\squirrel_video.mp4"
```

## Command-Line Arguments

| Argument | Description | Default | Example |
|----------|-------------|---------|---------|
| `--video-path` | Path to video file (required on Windows) | None | `--video-path "video.mp4"` |
| `--gpio-pin` | GPIO pin number (mock on Windows) | 18 | `--gpio-pin 18` |
| `--confidence-threshold` | Minimum detection confidence (0.0-1.0) | 0.5 | `--confidence-threshold 0.3` |
| `--center-threshold` | Center region size (0.0-1.0) | 0.3 | `--center-threshold 0.5` |
| `--debug` | Show debug window with visual output | False | `--debug` |

## Example Session

```powershell
# 1. Navigate to project
cd C:\Users\mikem\OneDrive\Documents\Python\cursor\squirrel

# 2. Activate venv
.\venv\Scripts\Activate.ps1

# 3. Run with debug window
squirrel-detector --video-path "C:\Users\mikem\Videos\squirrel.mp4" --debug

# 4. Watch the debug window - you'll see:
#    - Green rectangle showing center detection region
#    - Red/Green boxes around detected objects
#    - Detection status and confidence scores
#    - Press 'q' to quit
```

## What You'll See

### Debug Mode (--debug flag)

A window will open showing:
- **Green rectangle**: Center detection region (configurable size)
- **Red/Green boxes**: Detected objects (bounding boxes)
- **Text overlay**: 
  - "DETECTED" or "Monitoring..." status
  - Confidence score when detected
  - Bounding box coordinates

### Console Output

Logs will show:
```
INFO - Starting squirrel detector...
INFO - Monitoring for squirrels. GPIO pin 18 will trigger on detection.
INFO - Squirrel detected in center! Confidence: 0.75, BBox: (200, 150, 100, 120)
INFO - Squirrel detected in center! Confidence: 0.82, BBox: (205, 152, 98, 118)
```

### Important Notes

⚠️ **Remember**: The current detector uses simple color/shape heuristics, NOT a trained ML model. It will detect any brown object, not just squirrels. See `docs/DETECTION_METHOD.md` for details.

## Troubleshooting

### "Could not open video file"
- Check the file path is correct
- Verify the video file exists
- Try using absolute path instead of relative
- Check file format (MP4, AVI, MOV should work)

### "Module not found" errors
```powershell
pip install -e ".[dev]"
```

### Video window doesn't show
- Make sure you used the `--debug` flag
- Check if OpenCV window appears (might be behind other windows)
- Try pressing Alt+Tab to find the window

### Video plays too fast/slow
- The detector processes frames at ~30 FPS
- Video playback speed depends on your system
- Use `--debug` to see real-time processing

### No detections
- The detector looks for brown/reddish-brown objects
- Try lowering `--confidence-threshold` (e.g., 0.3)
- Ensure the video has brown objects in it
- Try increasing `--center-threshold` to detect objects in larger center region

## Getting Test Videos

### Free Sources

1. **Pexels Videos** (https://www.pexels.com/videos/)
   - Search: "squirrel", "garden squirrel", "wildlife"
   - Free, high quality
   - Download MP4 format

2. **Pixabay Videos** (https://pixabay.com/videos/)
   - Search: "squirrel", "garden", "wildlife"
   - Free, various resolutions

3. **YouTube** (with proper permissions)
   - Use `yt-dlp` to download:
   ```powershell
   pip install yt-dlp
   yt-dlp -f "best[height<=1080]" "YOUTUBE_URL" -o squirrel_test.mp4
   ```

### Creating Test Videos

If you have a camera or phone:
1. Record videos of squirrels (or brown objects for testing)
2. Transfer to your computer
3. Convert to MP4 if needed (using HandBrake or similar)

## Example Video Recommendations

For testing purposes, any video with:
- Brown/reddish-brown objects
- Clear visibility
- Good lighting
- Objects moving in the frame

Will work with the current detector (though it's not actually detecting squirrels - just brown objects).

## Next Steps

For better accuracy, consider:
1. Integrating a real ML model (YOLO, TensorFlow)
2. Training on actual squirrel images
3. Using pre-trained wildlife detection models

See `docs/DETECTION_METHOD.md` for details on improving detection accuracy.
