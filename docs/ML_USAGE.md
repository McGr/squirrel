# ML Model Usage Guide

## Overview

The project now supports two detection modes:

1. **Simple Detector** (`squirrel-detector`) - Original color/shape-based detection (single class)
2. **ML Detector** (`wildlife-detector`) - YOLO v8 based ML model (multi-class: squirrel, skunk, raccoon)

## ML Detector Usage

### Command: `wildlife-detector`

The ML-based detector supports multi-class detection with different GPIO pins for each class.

### Basic Usage

**On Raspberry Pi:**
```bash
wildlife-detector --camera 0 --debug
```

**On Windows (with video):**
```bash
wildlife-detector --video-path path/to/video.mp4 --debug
```

### Full Options

```bash
wildlife-detector \
  --camera 0 \
  --model-path models/wildlife_detector.pt \
  --squirrel-pin 18 \
  --skunk-pin 19 \
  --raccoon-pin 20 \
  --confidence-threshold 0.25 \
  --center-threshold 0.3 \
  --device cpu \
  --debug
```

### Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--camera` | Camera index (Pi only) | 0 |
| `--video-path` | Video file path (Windows) | None |
| `--model-path` | Path to trained YOLO model (.pt) | Auto-detected |
| `--squirrel-pin` | GPIO pin for squirrel | 18 |
| `--skunk-pin` | GPIO pin for skunk | 19 |
| `--raccoon-pin` | GPIO pin for raccoon | 20 |
| `--confidence-threshold` | Detection confidence (0.0-1.0) | 0.25 |
| `--center-threshold` | Center region size (0.0-1.0) | 0.3 |
| `--device` | Inference device (cpu, cuda, 0, 1) | cpu |
| `--debug` | Enable debug visualization | False |

### GPIO Pin Assignment

Each detected class triggers a different GPIO pin:
- **Squirrel detected in center** → GPIO 18 (default)
- **Skunk detected in center** → GPIO 19 (default)
- **Raccoon detected in center** → GPIO 20 (default)

Pins can be customized with command-line arguments.

### Model Detection

The detector looks for models in this order:
1. `--model-path` argument (if provided)
2. `models/wildlife_detector.pt`
3. `training/runs/wildlife_detection/weights/best.pt`
4. Pre-trained YOLO v8 (fallback - not trained on wildlife)

### Example Session

```bash
# Install package
pip install -e .

# Run with trained model (Windows)
wildlife-detector --video-path test_video.mp4 --model-path models/wildlife_detector.pt --debug

# Run on Raspberry Pi with custom pins
wildlife-detector --camera 0 --squirrel-pin 18 --skunk-pin 23 --raccoon-pin 24 --debug
```

### Debug Mode

With `--debug` flag, you'll see:
- **Green rectangle**: Center detection region
- **Colored bounding boxes**: 
  - Yellow = Squirrel
  - White = Skunk
  - Gray = Raccoon
- **Class name and confidence** on detection
- **Status text** showing detection state

### Logging

The application logs detection events:
```
INFO - Squirrel detected in center! Confidence: 0.95, BBox: (200, 150, 100, 120)
INFO - Skunk detected in center! Confidence: 0.92, BBox: (300, 200, 120, 140)
INFO - Raccoon detected in center! Confidence: 0.88, BBox: (150, 180, 110, 130)
```

### Differences from Simple Detector

| Feature | Simple Detector | ML Detector |
|---------|----------------|-------------|
| Command | `squirrel-detector` | `wildlife-detector` |
| Classes | 1 (squirrel-like) | 3 (squirrel, skunk, raccoon) |
| GPIO | Single pin | Multiple pins (one per class) |
| Accuracy | ~30-50% | ~99.5% (on synthetic data) |
| Method | Color/shape heuristics | YOLO v8 ML model |
| Model file | None | `models/wildlife_detector.pt` |

### Performance

- **Inference speed**: ~200ms per frame (CPU)
- **Accuracy**: 99.5% mAP50 on synthetic data
- **Memory**: ~50-100MB for model loading
- **Recommended**: GPU (CUDA) for faster inference

### Troubleshooting

**Model not found:**
- Ensure `models/wildlife_detector.pt` exists
- Or use `--model-path` to specify model location

**No detections:**
- Lower `--confidence-threshold` (try 0.15-0.20)
- Check that video/images contain target animals
- Verify model is trained for your use case

**Slow performance:**
- Use GPU: `--device cuda` or `--device 0`
- Reduce image resolution (not yet configurable)
- Use smaller model (yolov8n, yolov8s)

### Next Steps

For production use:
1. Retrain model on real images of squirrels, skunks, and raccoons
2. Collect diverse dataset (lighting, angles, backgrounds)
3. Fine-tune on your specific use case
4. Test on Raspberry Pi with real camera
