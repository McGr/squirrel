"""Train YOLO v8 model for Squirrel, Skunk, and Raccoon detection."""

import argparse
import sys
from pathlib import Path

try:
    from ultralytics import YOLO
except ImportError:
    print("ERROR: ultralytics not installed")
    print("Install with: pip install ultralytics")
    sys.exit(1)


def train_model(
    dataset_yaml: str = "training/datasets/dataset.yaml",
    epochs: int = 100,
    batch_size: int = 16,
    img_size: int = 640,
    model_size: str = "n",  # n=nano, s=small, m=medium, l=large, x=xlarge
    device: str = "cpu",
    project: str = "training/runs",
    name: str = "wildlife_detection",
):
    """Train YOLO v8 model.

    Args:
        dataset_yaml: Path to dataset YAML file
        epochs: Number of training epochs
        batch_size: Batch size for training
        img_size: Image size for training
        model_size: Model size (n, s, m, l, x)
        device: Device to use (cpu, cuda, 0, 1, etc.)
        project: Project directory for outputs
        name: Experiment name
    """
    dataset_path = Path(dataset_yaml)

    if not dataset_path.exists():
        print(f"ERROR: Dataset YAML not found: {dataset_yaml}")
        print("Please create dataset.yaml or run training/download_datasets.py")
        sys.exit(1)

    print("=" * 60)
    print("Training YOLO v8 Model")
    print("=" * 60)
    print(f"Dataset: {dataset_yaml}")
    print(f"Epochs: {epochs}")
    print(f"Batch size: {batch_size}")
    print(f"Image size: {img_size}")
    print(f"Model size: {model_size}")
    print(f"Device: {device}")
    print("=" * 60)
    print()

    # Load YOLO model (pre-trained on COCO)
    model_name = f"yolov8{model_size}.pt"
    print(f"Loading pre-trained model: {model_name}")
    model = YOLO(model_name)

    # Train the model
    print("Starting training...")
    print()

    results = model.train(
        data=str(dataset_path),
        epochs=epochs,
        imgsz=img_size,
        batch=batch_size,
        device=device,
        project=project,
        name=name,
        patience=50,  # Early stopping patience
        save=True,
        save_period=10,  # Save checkpoint every 10 epochs
        val=True,  # Validate during training
        plots=True,  # Generate plots
        verbose=True,
    )

    print()
    print("=" * 60)
    print("Training Complete!")
    print("=" * 60)
    print(f"Best model saved to: {project}/{name}/weights/best.pt")
    print(f"Last model saved to: {project}/{name}/weights/last.pt")
    print()
    print("To use the model in your application:")
    print(f"  Copy {project}/{name}/weights/best.pt to models/wildlife_detector.pt")
    print()

    return results


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Train YOLO v8 model for wildlife detection")
    parser.add_argument(
        "--dataset",
        type=str,
        default="training/datasets/dataset.yaml",
        help="Path to dataset YAML file",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=100,
        help="Number of training epochs (default: 100)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=16,
        help="Batch size for training (default: 16)",
    )
    parser.add_argument(
        "--img-size",
        type=int,
        default=640,
        help="Image size for training (default: 640)",
    )
    parser.add_argument(
        "--model-size",
        type=str,
        default="n",
        choices=["n", "s", "m", "l", "x"],
        help="Model size: n=nano, s=small, m=medium, l=large, x=xlarge (default: n)",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        help="Device to use: cpu, cuda, 0, 1, etc. (default: cpu)",
    )
    parser.add_argument(
        "--project",
        type=str,
        default="training/runs",
        help="Project directory for outputs (default: training/runs)",
    )
    parser.add_argument(
        "--name",
        type=str,
        default="wildlife_detection",
        help="Experiment name (default: wildlife_detection)",
    )

    args = parser.parse_args()

    train_model(
        dataset_yaml=args.dataset,
        epochs=args.epochs,
        batch_size=args.batch_size,
        img_size=args.img_size,
        model_size=args.model_size,
        device=args.device,
        project=args.project,
        name=args.name,
    )


if __name__ == "__main__":
    main()
