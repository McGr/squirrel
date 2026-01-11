# How to Try Out the ML Detector

## Quick Start Guide

### Method 1: Quick Test Script (Easiest)

Run the test script to see detections on all three classes:

```powershell
# Activate venv
.\venv\Scripts\Activate.ps1

# Run test script
python test_ml_detector.py
```

This will:
- Load the trained model
- Test on 3 unseen images (squirrel, skunk, raccoon)
- Show detection results with confidence scores
- Test the multi-class GPIO interface

**Expected Output:**
```
✅ DETECTED: SQUIRREL
   Confidence: 0.994 (99.4%)
   Bounding Box: x=326, y=180, w=94, h=90

✅ DETECTED: SKUNK
   Confidence: 0.995 (99.5%)
   Bounding Box: x=251, y=120, w=121, h=136

✅ DETECTED: RACCOON
   Confidence: 0.995 (99.5%)
   Bounding Box: x=366, y=296, w=130, h=149
```

---

### Method 2: Run with Debug Window (Visual)

See the detections with visual feedback:

```powershell
# Activate venv
.\venv\Scripts\Activate.ps1

# Test squirrel detection
python -m squirrel.main_ml --video-path training\test_images\val\images\squirrel_val_0000.jpg --model-path models\wildlife_detector.pt --debug

# Test skunk detection
python -m squirrel.main_ml --video-path training\test_images\val\images\skunk_val_0000.jpg --model-path models\wildlife_detector.pt --debug

# Test raccoon detection
python -m squirrel.main_ml --video-path training\test_images\val\images\raccoon_val_0000.jpg --model-path models\wildlife_detector.pt --debug
```

**What you'll see:**
- Debug window showing the image
- Green rectangle = Center detection region
- Colored bounding box = Detected animal:
  - **Yellow** = Squirrel
  - **White** = Skunk
  - **Gray** = Raccoon
- Text overlay with class name and confidence
- Press **'q'** to quit

---

### Method 3: Test on Validation Images (Full Set)

Test on the validation set to see all detections:

```powershell
# Activate venv
.\venv\Scripts\Activate.ps1

# Evaluate on validation set
python training/evaluate_model.py --model models/wildlife_detector.pt --dataset training/datasets/synthetic/dataset.yaml --test-train
```

This will show:
- Validation set results (30 images)
- Training set results (150 images)
- Per-class metrics
- Overall accuracy

---

## Step-by-Step Example Session

### 1. Open PowerShell

Navigate to project directory:
```powershell
cd C:\Users\mikem\OneDrive\Documents\Python\cursor\squirrel
```

### 2. Activate Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Run Quick Test

```powershell
python test_ml_detector.py
```

**Expected Output:**
```
============================================================
Testing ML Detector on Unseen Test Images
============================================================

Loading model: models/wildlife_detector.pt

============================================================
Testing: squirrel_val_0000.jpg
============================================================
✅ DETECTED: SQUIRREL
   Confidence: 0.994 (99.4%)
   Bounding Box: x=326, y=180, w=94, h=90
   Center Detection: True

============================================================
Testing: skunk_val_0000.jpg
============================================================
✅ DETECTED: SKUNK
   Confidence: 0.995 (99.5%)
   Bounding Box: x=251, y=120, w=121, h=136
   Center Detection: True

============================================================
Testing: raccoon_val_0000.jpg
============================================================
✅ DETECTED: RACCOON
   Confidence: 0.995 (99.5%)
   Bounding Box: x=366, y=296, w=130, h=149
   Center Detection: True

============================================================
Test Complete!
============================================================
```

### 4. Try Visual Debug Mode

```powershell
python -m squirrel.main_ml --video-path training\test_images\val\images\squirrel_val_0000.jpg --debug
```

You'll see a window with:
- The image
- Green center region box
- Yellow bounding box around the squirrel
- "Squirrel DETECTED" text
- Confidence score overlay

**Press 'q' to quit**

---

## Testing GPIO Simulation

The test script also shows how GPIO pins would trigger:

```
Testing Multi-Class GPIO Interface
============================================================

GPIO pins configured: {'squirrel': 18, 'skunk': 19, 'raccoon': 20}

Testing GPIO triggers:
  Triggering squirrel (GPIO 18)...
    State after trigger: False
  Triggering skunk (GPIO 19)...
    State after trigger: False
  Triggering raccoon (GPIO 20)...
    State after trigger: False

✅ GPIO test complete!
```

On Raspberry Pi, these pins would actually go HIGH when each class is detected.

---

## Test All Classes

Quick test on all three classes:

```powershell
# Quick test (fast, no window)
python test_ml_detector.py

# Visual test - Squirrel
python -m squirrel.main_ml --video-path training\test_images\val\images\squirrel_val_0000.jpg --debug

# Visual test - Skunk (in new terminal or after closing previous)
python -m squirrel.main_ml --video-path training\test_images\val\images\skunk_val_0000.jpg --debug

# Visual test - Raccoon
python -m squirrel.main_ml --video-path training\test_images\val\images\raccoon_val_0000.jpg --debug
```

---

## Custom GPIO Pins

Test with custom GPIO pin assignments:

```powershell
python -m squirrel.main_ml `
  --video-path training\test_images\val\images\squirrel_val_0000.jpg `
  --model-path models\wildlife_detector.pt `
  --squirrel-pin 22 `
  --skunk-pin 23 `
  --raccoon-pin 24 `
  --debug
```

---

## Troubleshooting

**"Model not found":**
- Check: `dir models\wildlife_detector.pt`
- Should exist if training completed

**"Image not found":**
- Check: `dir training\test_images\val\images`
- Images should exist from dataset generation

**No detections:**
- Try lowering confidence: `--confidence-threshold 0.15`
- Increase center region: `--center-threshold 0.8`

**Import errors:**
- Activate venv: `.\venv\Scripts\Activate.ps1`
- Reinstall: `pip install -e .`

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `python test_ml_detector.py` | Quick test all classes |
| `python -m squirrel.main_ml --video-path IMAGE --debug` | Visual test |
| `python training/evaluate_model.py --model models/wildlife_detector.pt --dataset training/datasets/synthetic/dataset.yaml` | Full evaluation |

---

## Next Steps

Once you've verified it works:
1. Try with your own images/videos
2. Test on Raspberry Pi with real camera
3. Retrain on real images for production use

Enjoy testing! 🐿️🦨🦝
