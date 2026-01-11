"""Evaluate trained model on training and test data."""

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np

try:
    from ultralytics import YOLO
except ImportError:
    print("ERROR: ultralytics not installed")
    print("Install with: pip install ultralytics")
    sys.exit(1)


def evaluate_on_dataset(model_path: str, dataset_yaml: str, split: str = "val"):
    """Evaluate model on a dataset split.

    Args:
        model_path: Path to trained model (.pt file)
        dataset_yaml: Path to dataset YAML file
        split: Dataset split ('train' or 'val')

    Returns:
        Dictionary with evaluation metrics
    """
    print(f"\n{'='*60}")
    print(f"Evaluating on {split} set")
    print(f"{'='*60}")

    # Load model
    print(f"Loading model: {model_path}")
    model = YOLO(model_path)

    # Run validation
    results = model.val(data=dataset_yaml, split=split, verbose=True)

    print(f"\n{split.upper()} Results:")
    print(f"  mAP50: {results.box.map50:.4f}")
    print(f"  mAP50-95: {results.box.map:.4f}")
    print(f"  Precision: {results.box.mp:.4f}")
    print(f"  Recall: {results.box.mr:.4f}")

    return results


def test_on_single_image(model_path: str, image_path: str, confidence: float = 0.25):
    """Test model on a single image.

    Args:
        model_path: Path to trained model
        image_path: Path to test image
        confidence: Confidence threshold
    """
    print(f"\n{'='*60}")
    print(f"Testing on image: {image_path}")
    print(f"{'='*60}")

    model = YOLO(model_path)

    # Load image
    img = cv2.imread(str(image_path))
    if img is None:
        print(f"ERROR: Could not load image {image_path}")
        return

    # Run inference
    results = model(img, conf=confidence, verbose=False)

    # Print results
    result = results[0]
    if result.boxes is not None and len(result.boxes) > 0:
        print(f"\nDetections: {len(result.boxes)}")
        for i, box in enumerate(result.boxes):
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            class_names = {0: "squirrel", 1: "skunk", 2: "raccoon"}
            class_name = class_names.get(cls_id, f"class_{cls_id}")
            xyxy = box.xyxy[0].cpu().numpy()
            x1, y1, x2, y2 = xyxy
            print(f"  Detection {i+1}: {class_name} (confidence: {conf:.3f})")
            print(f"    BBox: ({int(x1)}, {int(y1)}, {int(x2)}, {int(y2)})")
    else:
        print("No detections")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Evaluate trained model")
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Path to trained model (.pt file)",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="training/datasets/synthetic/dataset.yaml",
        help="Path to dataset YAML file",
    )
    parser.add_argument(
        "--test-train",
        action="store_true",
        help="Test on training set (in addition to validation)",
    )
    parser.add_argument(
        "--test-image",
        type=str,
        default=None,
        help="Path to single test image (not in training data)",
    )
    parser.add_argument(
        "--confidence",
        type=float,
        default=0.25,
        help="Confidence threshold (default: 0.25)",
    )

    args = parser.parse_args()

    model_path = Path(args.model)
    if not model_path.exists():
        print(f"ERROR: Model not found: {args.model}")
        sys.exit(1)

    dataset_yaml = Path(args.dataset)
    if not dataset_yaml.exists():
        print(f"ERROR: Dataset YAML not found: {args.dataset}")
        sys.exit(1)

    # Evaluate on validation set
    val_results = evaluate_on_dataset(str(model_path), str(dataset_yaml), split="val")

    # Optionally evaluate on training set
    if args.test_train:
        train_results = evaluate_on_dataset(str(model_path), str(dataset_yaml), split="train")

    # Test on single image if provided
    if args.test_image:
        test_img_path = Path(args.test_image)
        if test_img_path.exists():
            test_on_single_image(str(model_path), str(test_img_path), args.confidence)
        else:
            print(f"WARNING: Test image not found: {args.test_image}")

    print("\n" + "=" * 60)
    print("Evaluation complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
