"""Generate synthetic dataset for demonstration and testing."""

import argparse
import random
import shutil
from pathlib import Path

import cv2
import numpy as np
import yaml

# Class colors (simulating animals)
CLASS_COLORS = {
    "squirrel": (42, 42, 165),  # Brown in BGR
    "skunk": (255, 255, 255),  # White in BGR
    "raccoon": (128, 128, 128),  # Gray in BGR
}

CLASS_IDS = {"squirrel": 0, "skunk": 1, "raccoon": 2}


def generate_synthetic_image(width: int, height: int, class_name: str) -> tuple:
    """Generate a synthetic image with a colored blob.

    Args:
        width: Image width
        height: Image height
        class_name: Class name (squirrel, skunk, raccoon)

    Returns:
        Tuple of (image, bbox) where bbox is (x, y, w, h) in normalized format
    """
    # Create background (green/grass-like)
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:, :] = [0, 100, 0]  # Dark green background

    # Get class color
    color = CLASS_COLORS[class_name]

    # Random position (not too close to edges)
    margin = 50
    blob_width = random.randint(80, 150)
    blob_height = random.randint(80, 150)
    x = random.randint(margin, width - blob_width - margin)
    y = random.randint(margin, height - blob_height - margin)

    # Draw elliptical blob (animal-like shape)
    center = (x + blob_width // 2, y + blob_height // 2)
    axes = (blob_width // 2, blob_height // 2)
    cv2.ellipse(img, center, axes, 0, 0, 360, color, -1)  # Filled ellipse

    # Add some noise/texture
    noise = np.random.randint(-20, 20, (height, width, 3), dtype=np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    # Normalize bbox (YOLO format: center_x, center_y, width, height)
    center_x = (x + blob_width / 2) / width
    center_y = (y + blob_height / 2) / height
    norm_w = blob_width / width
    norm_h = blob_height / height

    bbox = (center_x, center_y, norm_w, norm_h)

    return img, bbox


def create_dataset(output_dir: Path, num_train: int, num_val: int):
    """Create synthetic dataset.

    Args:
        output_dir: Output directory
        num_train: Number of training images per class
        num_val: Number of validation images per class
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create directory structure
    train_img_dir = output_dir / "train" / "images"
    train_label_dir = output_dir / "train" / "labels"
    val_img_dir = output_dir / "val" / "images"
    val_label_dir = output_dir / "val" / "labels"

    for dir_path in [train_img_dir, train_label_dir, val_img_dir, val_label_dir]:
        dir_path.mkdir(parents=True, exist_ok=True)

    classes = list(CLASS_IDS.keys())
    img_size = 640

    print(f"Generating {num_train} training images per class...")
    # Generate training images
    for class_name in classes:
        for i in range(num_train):
            img, bbox = generate_synthetic_image(img_size, img_size, class_name)
            img_filename = f"{class_name}_train_{i:04d}.jpg"
            label_filename = f"{class_name}_train_{i:04d}.txt"

            # Save image
            img_path = train_img_dir / img_filename
            cv2.imwrite(str(img_path), img)

            # Save label (YOLO format)
            class_id = CLASS_IDS[class_name]
            label_path = train_label_dir / label_filename
            with open(label_path, "w") as f:
                f.write(f"{class_id} {bbox[0]:.6f} {bbox[1]:.6f} {bbox[2]:.6f} {bbox[3]:.6f}\n")

    print(f"Generating {num_val} validation images per class...")
    # Generate validation images
    for class_name in classes:
        for i in range(num_val):
            img, bbox = generate_synthetic_image(img_size, img_size, class_name)
            img_filename = f"{class_name}_val_{i:04d}.jpg"
            label_filename = f"{class_name}_val_{i:04d}.txt"

            # Save image
            img_path = val_img_dir / img_filename
            cv2.imwrite(str(img_path), img)

            # Save label
            class_id = CLASS_IDS[class_name]
            label_path = val_label_dir / label_filename
            with open(label_path, "w") as f:
                f.write(f"{class_id} {bbox[0]:.6f} {bbox[1]:.6f} {bbox[2]:.6f} {bbox[3]:.6f}\n")

    # Create dataset.yaml
    yaml_path = output_dir / "dataset.yaml"
    yaml_content = {
        "path": str(output_dir.absolute()),
        "train": "train/images",
        "val": "val/images",
        "nc": len(classes),
        "names": {idx: name for idx, name in enumerate(classes)},
    }

    with open(yaml_path, "w") as f:
        yaml.dump(yaml_content, f, default_flow_style=False)

    print(f"\nDataset created at: {output_dir}")
    print(f"Training images: {num_train * len(classes)}")
    print(f"Validation images: {num_val * len(classes)}")
    print(f"Dataset YAML: {yaml_path}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Generate synthetic dataset for training")
    parser.add_argument(
        "--output",
        type=str,
        default="training/datasets/synthetic",
        help="Output directory (default: training/datasets/synthetic)",
    )
    parser.add_argument(
        "--train-per-class",
        type=int,
        default=50,
        help="Number of training images per class (default: 50)",
    )
    parser.add_argument(
        "--val-per-class",
        type=int,
        default=10,
        help="Number of validation images per class (default: 10)",
    )

    args = parser.parse_args()

    output_dir = Path(args.output)

    if output_dir.exists():
        response = input(f"Directory {output_dir} exists. Overwrite? (y/n): ")
        if response.lower() != "y":
            print("Cancelled.")
            return
        shutil.rmtree(output_dir)

    create_dataset(output_dir, args.train_per_class, args.val_per_class)


if __name__ == "__main__":
    main()
