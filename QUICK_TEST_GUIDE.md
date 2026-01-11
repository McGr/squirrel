# Quick Test Guide - Try the ML Detector Now!

## ✅ Test Results

The ML detector successfully detects all three classes on unseen test images:

- ✅ **Squirrel**: 99.4% confidence
- ✅ **Skunk**: 99.5% confidence
- ✅ **Raccoon**: 99.5% confidence

## 🚀 Three Ways to Try It

### Method 1: Quick Test Script (Fastest - Recommended)

**Run this command:**

```powershell
# 1. Activate venv
.\venv\Scripts\Activate.ps1

# 2. Run test script
python test_ml_detector.py
```

**What you'll see:**
- Detection results for all three classes
- Confidence scores (99.4-99.5%)
- Bounding box coordinates
- GPIO simulation test

**Output example:**
```
✅ DETECTED: SQUIRREL
   Confidence: 0.994 (99.4%)
   Bounding Box: x=326, y=180, w=94, h=90

✅ DETECTED: SKUNK
   Confidence: 0.995 (99.5%)
   Bounding Box: x=251, y=120, w=120, h=135

✅ DETECTED: RACCOON
   Confidence: 0.995 (99.5%)
   Bounding Box: x=366, y=296, w=129, h=149
```

---

### Method 2: Visual Test with Debug Window (See Detections)

**Run this command:**

```powershell
# 1. Activate venv
.\venv\Scripts\Activate.ps1

# 2. Test squirrel detection (opens a window)
python -m squirrel.main_ml --video-path training\test_images\val\images\squirrel_val_0000.jpg --debug
```

**What you'll see:**
- Debug window showing the image
- **Green rectangle** = Center detection region
- **Yellow bounding box** = Squirrel detected
- **Text overlay** = "Squirrel DETECTED" with confidence score
- Press **'q'** to quit

**Try all three classes:**
```powershell
# Squirrel (Yellow box)
python -m squirrel.main_ml --video-path training\test_images\val\images\squirrel_val_0000.jpg --debug

# Skunk (White box)
python -m squirrel.main_ml --video-path training\test_images\val\images\skunk_val_0000.jpg --debug

# Raccoon (Gray box)
python -m squirrel.main_ml --video-path training\test_images\val\images\raccoon_val_0000.jpg --debug
```

---

### Method 3: Full Evaluation (Detailed Metrics)

**Run this command:**

```powershell
# 1. Activate venv
.\venv\Scripts\Activate.ps1

# 2. Full evaluation
python training/evaluate_model.py --model models\wildlife_detector.pt --dataset training/datasets/synthetic/dataset.yaml --test-train
```

**What you'll see:**
- Validation set metrics (30 images)
- Training set metrics (150 images)
- Per-class precision, recall, mAP
- Overall accuracy statistics

---

## 📋 Step-by-Step: Try It Now

### Copy and paste these commands:

```powershell
# Navigate to project
cd C:\Users\mikem\OneDrive\Documents\Python\cursor\squirrel

# Activate venv
.\venv\Scripts\Activate.ps1

# Quick test (recommended first)
python test_ml_detector.py
```

**That's it!** You'll see detection results for all three classes.

---

## 🎯 Expected Results

Based on our testing, you should see:

| Class | Confidence | Status |
|-------|-----------|--------|
| Squirrel | ~99.4% | ✅ Detected |
| Skunk | ~99.5% | ✅ Detected |
| Raccoon | ~99.5% | ✅ Detected |

All three classes are correctly identified with high confidence!

---

## 🔧 Command Options

### Basic Command
```powershell
python -m squirrel.main_ml --video-path IMAGE.jpg --debug
```

### Full Command with Options
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

---

## 📁 Test Images Available

You have test images ready to use:

- `training\test_images\val\images\squirrel_val_0000.jpg`
- `training\test_images\val\images\skunk_val_0000.jpg`
- `training\test_images\val\images\raccoon_val_0000.jpg`

These are **unseen images** (not in training data) - perfect for testing!

---

## 🎨 Visual Debug Mode

When using `--debug` flag, you'll see:
- **Green rectangle**: Center detection region
- **Colored bounding boxes**:
  - 🟡 **Yellow** = Squirrel
  - ⚪ **White** = Skunk
  - ⚫ **Gray** = Raccoon
- **Class name and confidence** overlay
- **Status text**: "Squirrel DETECTED" or "Monitoring..."

**Press 'q' to quit**

---

## 🐿️ GPIO Simulation

The test script also simulates GPIO triggers:
- Squirrel detection → GPIO 18 (would trigger on Pi)
- Skunk detection → GPIO 19 (would trigger on Pi)
- Raccoon detection → GPIO 20 (would trigger on Pi)

On Raspberry Pi, these pins would actually go HIGH when each class is detected!

---

## 📚 More Information

- **Quick Test**: `test_ml_detector.py` (fastest)
- **Visual Test**: `python -m squirrel.main_ml --video-path IMAGE --debug`
- **Full Guide**: See `HOW_TO_TRY_IT.md` or `docs/ML_USAGE.md`

---

## ✅ Success Criteria

You'll know it's working when you see:
- ✅ All three classes detected
- ✅ Confidence scores > 95%
- ✅ Correct bounding boxes
- ✅ Debug window shows colored boxes (if using --debug)

**It's working!** 🎉
