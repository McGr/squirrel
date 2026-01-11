# Squirrel Detection Method

## Current Implementation: Not a Trained Model

**Important**: The current squirrel detector is **NOT** a machine learning model and is **NOT trained** on squirrel images. It uses a basic computer vision approach with color and shape heuristics.

## How It Currently Works

### Detection Algorithm

The current implementation uses **simple computer vision techniques**:

1. **Color Detection** (HSV color space):
   - Looks for brown/reddish-brown colors in the image
   - Uses two color ranges:
     - Range 1: HSV [10-20, 50-255, 50-255] (orange-brown)
     - Range 2: HSV [0-10, 50-255, 50-255] (red-brown)
   - Creates a mask of brown-colored pixels

2. **Morphological Operations**:
   - Cleans up the color mask (removes noise)
   - Closes gaps in detected regions
   - Opens to remove small artifacts

3. **Contour Analysis**:
   - Finds the largest brown blob in the image
   - Filters by size (1% to 50% of frame area)
   - Filters by aspect ratio (0.5 to 2.5)

4. **Confidence Scoring**:
   - Based on blob size relative to frame
   - Adjusted by aspect ratio (prefers 1:1 to 2:1 ratios)

### Limitations

❌ **No actual squirrel recognition** - just looks for brown objects  
❌ **High false positive rate** - will detect any brown object (dogs, cats, tree trunks, etc.)  
❌ **No shape recognition** - doesn't understand what a squirrel looks like  
❌ **Color-dependent** - won't work with gray squirrels or in poor lighting  
❌ **Not trained** - no machine learning model used

### Expected Accuracy

**Current accuracy is LOW** (estimated 30-50% at best):
- Will detect many non-squirrel brown objects
- May miss squirrels that are too dark/light or in shadows
- Works best with:
  - Clear lighting
  - Brown/red squirrels (not gray)
  - Squirrels that are clearly visible and brown-colored

## Why This Approach Was Used

This was implemented as a **foundation/prototype** approach because:
1. No training data required
2. Simple to implement and test
3. Fast execution (no ML inference)
4. Good starting point for development

The code comments explicitly state:
```python
# For a real implementation, you would load a trained model here
# This is a placeholder that uses color and shape analysis
# In production, you might want to use a trained model
```

## Recommended Improvements for Production

For **actual squirrel detection**, you should integrate a real ML model:

### Option 1: Use Pre-trained Object Detection (Easiest)
- **YOLO v8** (Ultralytics) - pre-trained on COCO dataset (includes squirrel-like animals)
- **TensorFlow Object Detection API** - MobileNet or EfficientDet models
- **COCO dataset** includes some small animal classes

### Option 2: Fine-tune a Model (Better Accuracy)
- Use **YOLO v8** or **Detectron2**
- Collect squirrel images (500+ images recommended)
- Label bounding boxes around squirrels
- Fine-tune the model on your dataset

### Option 3: Train from Scratch (Best Accuracy)
- Collect large dataset (1000+ squirrel images)
- Include various:
  - Lighting conditions
  - Angles
  - Backgrounds
  - Squirrel colors (brown, gray, black)
- Train a custom YOLO or Faster R-CNN model

### Option 4: Use Existing Wildlife Detection Models
- Look for pre-trained wildlife detection models
- Many research projects share trained models for small animals

## Current Use Case

The current implementation is suitable for:
- ✅ **Prototyping** and testing the system architecture
- ✅ **Development** of the camera/GPIO pipeline
- ✅ **Demonstration** of the concept
- ✅ **Testing** with brown objects in controlled environments

**NOT suitable for**:
- ❌ Production deployment expecting accurate detection
- ❌ Real-world squirrel monitoring
- ❌ Critical applications requiring high accuracy

## Conclusion

**The model is NOT trained on squirrels** - it's a simple color/shape heuristic that will detect any brown object roughly the right size. For production use, you'll need to integrate a real machine learning model trained on squirrel images.
