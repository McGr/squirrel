# ML Model Training for Squirrel, Skunk, and Raccoon Detection

This directory contains scripts and resources for training a YOLO v8 object detection model to detect Squirrels, Skunks, and Raccoons.

## Overview

We're using **YOLO v8 (Ultralytics)** for object detection because:
- State-of-the-art accuracy
- Efficient inference on Raspberry Pi
- Easy to train and deploy
- Good balance between speed and accuracy

## Dataset Sources

### Option 1: Roboflow (Recommended - Free)

1. Go to https://universe.roboflow.com/
2. Search for datasets:
   - "squirrel" datasets
   - "wildlife" datasets
   - "small mammals" datasets
3. Export in YOLO format
4. Download and extract to `training/datasets/`

### Option 2: Kaggle

1. Search Kaggle for:
   - "squirrel detection"
   - "wildlife detection"
   - "raccoon dataset"
2. Download and convert to YOLO format

### Option 3: Custom Dataset

1. Collect images from:
   - Pexels, Pixabay (free images)
   - Your own camera
   - Wildlife photography sites
2. Label using LabelImg or Roboflow
3. Organize in YOLO format

## Dataset Structure

```
training/datasets/
├── train/
│   ├── images/
│   │   ├── img001.jpg
│   │   ├── img002.jpg
│   │   └── ...
│   └── labels/
│       ├── img001.txt
│       ├── img002.txt
│       └── ...
├── val/
│   ├── images/
│   └── labels/
└── dataset.yaml  # Dataset configuration
```

## Training Classes

- **0**: squirrel
- **1**: skunk
- **2**: raccoon

## Quick Start

1. Prepare dataset (see dataset preparation script)
2. Run training:
   ```bash
   python training/train_yolo.py --epochs 100
   ```
3. Model will be saved to `training/models/best.pt`
4. Use the model in the application

## Files

- `train_yolo.py` - Main training script
- `prepare_dataset.py` - Dataset preparation utilities
- `download_datasets.py` - Script to download datasets from various sources
- `evaluate_model.py` - Model evaluation script
- `convert_model.py` - Convert YOLO model to ONNX/TensorRT if needed
