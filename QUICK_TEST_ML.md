# Quick Test Guide - ML Detector

## Quick Test on Windows (PowerShell)

### Step 1: Activate Virtual Environment

```powershell
cd C:\Users\mikem\OneDrive\Documents\Python\cursor\squirrel
.\venv\Scripts\Activate.ps1
```

### Step 2: Test with a Single Image

Use one of the test images we generated:

```powershell
# Test on a squirrel image (not in training data)
python -m squirrel.main_ml --video-path training\test_images\val\images\squirrel_val_0000.jpg --model-path models\wildlife_detector.pt --debug

# Test on a skunk image
python -m squirrel.main_ml --video-path training\test_images\val\images\skunk_val_0000.jpg --model-path models\wildlife_detector.pt --debug

# Test on a raccoon image
python -m squirrel.main_ml --video-path training\test_images\val\images\raccoon_val_0000.jpg --model-path models\wildlife_detector.pt --debug
```

### Step 3: Create a Test Video (Optional)

If you want to test with a video file, you can create a simple video from the test images, or download a video from the web.

## Quick Test Commands

### Minimal Command (uses default model location)
```powershell
python -m squirrel.main_ml --video-path training\test_images\val\images\squirrel_val_0000.jpg --debug
```

### Full Command with All Options
```powershell
python -m squirrel.main_ml `
  --video-path training\test_images\val\images\squirrel_val_0000.jpg `
  --model-path models\wildlife_detector.pt `
  --squirrel-pin 18 `
  --skunk-pin 19 `
  --raccoon-pin 20 `
  --confidence-threshold 0.25 `
  --center-threshold 0.3 `
  --debug
```

## What You'll See

### Debug Window
- **Green rectangle**: Center detection region
- **Colored bounding box**: 
  - Yellow = Squirrel
  - White = Skunk
  - Gray = Raccoon
- **Text overlay**: Class name and confidence score
- **Status**: "Squirrel DETECTED" or "Monitoring..."

### Console Output
```
INFO - Starting wildlife detector with ML model...
INFO - Classes: ['squirrel', 'skunk', 'raccoon']
INFO - GPIO pins: {'squirrel': 18, 'skunk': 19, 'raccoon': 20}
INFO - Monitoring for wildlife. GPIO pins will trigger on detection.
INFO - Squirrel detected in center! Confidence: 0.99, BBox: (326, 180, 94, 90)
```

### Press 'q' to quit

## Testing All Classes

Test all three classes in sequence:

```powershell
# Squirrel
python -m squirrel.main_ml --video-path training\test_images\val\images\squirrel_val_0000.jpg --model-path models\wildlife_detector.pt --debug

# Skunk (in new terminal/window)
python -m squirrel.main_ml --video-path training\test_images\val\images\skunk_val_0000.jpg --model-path models\wildlife_detector.pt --debug

# Raccoon
python -m squirrel.main_ml --video-path training\test_images\val\images\raccoon_val_0000.jpg --model-path models\wildlife_detector.pt --debug
```

## On Raspberry Pi

Once deployed to Raspberry Pi:

```bash
# Activate venv
source venv/bin/activate

# Run with camera
wildlife-detector --camera 0 --model-path models/wildlife_detector.pt --debug

# Or with custom pins
wildlife-detector --camera 0 --squirrel-pin 18 --skunk-pin 19 --raccoon-pin 20 --debug
```

## Troubleshooting

**"Model not found":**
- Check that `models/wildlife_detector.pt` exists
- Or specify path with `--model-path`

**"No detections":**
- The test images should work (we tested them)
- Try lowering `--confidence-threshold` to 0.15

**Image file not found:**
- Check the path: `training\test_images\val\images\`
- Use full path if needed: `--video-path C:\full\path\to\image.jpg`

## Expected Results

Since we tested these exact images earlier:
- **squirrel_val_0000.jpg**: Should detect squirrel with ~99.4% confidence
- **skunk_val_0000.jpg**: Should detect skunk with ~99.5% confidence
- **raccoon_val_0000.jpg**: Should detect raccoon with ~99.5% confidence
