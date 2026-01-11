"""Download and prepare datasets for training."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

# URLs and instructions for datasets
DATASET_INFO = {
    "squirrel": {
        "roboflow": "https://universe.roboflow.com/search?q=squirrel",
        "kaggle": "Search Kaggle for 'squirrel detection'",
        "notes": "Look for datasets with YOLO format available",
    },
    "skunk": {
        "roboflow": "https://universe.roboflow.com/search?q=skunk",
        "kaggle": "Search Kaggle for 'skunk wildlife'",
        "notes": "May need to combine with wildlife datasets",
    },
    "raccoon": {
        "roboflow": "https://universe.roboflow.com/search?q=raccoon",
        "kaggle": "Search Kaggle for 'raccoon detection'",
        "notes": "Common in wildlife detection datasets",
    },
}


def print_dataset_info():
    """Print information about where to find datasets."""
    print("=" * 60)
    print("Dataset Sources for Squirrel, Skunk, and Raccoon")
    print("=" * 60)
    print()

    for animal, info in DATASET_INFO.items():
        print(f"{animal.upper()}:")
        print(f"  Roboflow: {info['roboflow']}")
        print(f"  Kaggle: {info['kaggle']}")
        print(f"  Notes: {info['notes']}")
        print()

    print("RECOMMENDED APPROACH:")
    print("1. Go to https://universe.roboflow.com/")
    print("2. Search for each animal")
    print("3. Look for datasets with 'YOLO' format")
    print("4. Download and extract to training/datasets/")
    print("5. Ensure dataset.yaml is created with class names")
    print()
    print("ALTERNATIVE: Use COCO dataset and filter for relevant classes")
    print("  - COCO has some wildlife classes")
    print("  - Filter: small mammals, animals, etc.")
    print()


def create_sample_yaml():
    """Create a sample dataset.yaml file."""
    yaml_content = """# Dataset configuration for YOLO training
# Squirrel, Skunk, Raccoon Detection

path: training/datasets  # dataset root dir
train: train/images  # train images (relative to 'path')
val: val/images  # val images (relative to 'path')
test:  # optional, test images (relative to 'path')

# Classes
names:
  0: squirrel
  1: skunk
  2: raccoon

# Number of classes
nc: 3
"""
    yaml_path = Path("training/datasets/dataset.yaml")
    yaml_path.parent.mkdir(parents=True, exist_ok=True)

    if yaml_path.exists():
        print(f"dataset.yaml already exists at {yaml_path}")
        response = input("Overwrite? (y/n): ")
        if response.lower() != "y":
            return

    yaml_path.write_text(yaml_content)
    print(f"Created sample dataset.yaml at {yaml_path}")
    print("Please update paths and verify class names match your dataset.")


def check_roboflow_cli():
    """Check if Roboflow CLI is installed."""
    try:
        result = subprocess.run(
            ["roboflow", "--version"], capture_output=True, text=True, check=True
        )
        print(f"Roboflow CLI found: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_roboflow_cli():
    """Install Roboflow CLI."""
    print("Roboflow CLI not found. Installing...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "roboflow"], check=True)
        print("Roboflow CLI installed successfully!")
        print()
        print("To download datasets from Roboflow:")
        print("1. Sign up at https://roboflow.com/")
        print("2. Find a dataset")
        print("3. Use: roboflow download <workspace>/<project>/<version>")
        return True
    except subprocess.CalledProcessError:
        print("Failed to install Roboflow CLI")
        return False


def main():
    """Main function."""
    print_dataset_info()

    # Create dataset directory structure
    datasets_dir = Path("training/datasets")
    datasets_dir.mkdir(parents=True, exist_ok=True)

    print(f"Dataset directory created: {datasets_dir.absolute()}")
    print()

    # Check for Roboflow CLI
    if check_roboflow_cli():
        print("Roboflow CLI is available. You can use it to download datasets.")
    else:
        response = input("Install Roboflow CLI? (y/n): ")
        if response.lower() == "y":
            install_roboflow_cli()

    # Create sample YAML
    print()
    response = input("Create sample dataset.yaml? (y/n): ")
    if response.lower() == "y":
        create_sample_yaml()

    print()
    print("Next steps:")
    print("1. Download datasets from Roboflow or Kaggle")
    print("2. Organize them in the YOLO format")
    print("3. Update dataset.yaml with correct paths")
    print("4. Run: python training/train_yolo.py")


if __name__ == "__main__":
    main()
