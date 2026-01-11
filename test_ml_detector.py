"""Quick test script for ML detector."""

import sys
from pathlib import Path

import cv2
from squirrel.detector_ml import MLDetector
from squirrel.gpio_multiclass import MockMultiClassGPIO

# Test images
test_images = [
    "training/test_images/val/images/squirrel_val_0000.jpg",
    "training/test_images/val/images/skunk_val_0000.jpg",
    "training/test_images/val/images/raccoon_val_0000.jpg",
]


def test_detector():
    """Test the ML detector on test images."""
    print("=" * 60)
    print("Testing ML Detector on Unseen Test Images")
    print("=" * 60)
    print()

    # Load model
    model_path = "models/wildlife_detector.pt"
    if not Path(model_path).exists():
        print(f"ERROR: Model not found at {model_path}")
        print("Please ensure the model exists or specify a different path.")
        sys.exit(1)

    print(f"Loading model: {model_path}")
    detector = MLDetector(model_path=model_path, confidence_threshold=0.25)

    # Test each image
    for img_path in test_images:
        path = Path(img_path)
        if not path.exists():
            print(f"WARNING: Image not found: {img_path}")
            continue

        print(f"\n{'='*60}")
        print(f"Testing: {path.name}")
        print(f"{'='*60}")

        # Load image
        frame = cv2.imread(str(path))
        if frame is None:
            print(f"ERROR: Could not load image {img_path}")
            continue

        # Detect
        detected, bbox, confidence, class_name = detector.detect(frame)

        if detected and class_name:
            x, y, w, h = bbox
            print(f"✅ DETECTED: {class_name.upper()}")
            print(f"   Confidence: {confidence:.3f} ({confidence*100:.1f}%)")
            print(f"   Bounding Box: x={x}, y={y}, w={w}, h={h}")
            print(f"   Center Detection: {detector.is_in_center(frame, bbox)}")
        else:
            print("❌ No detection")

    print()
    print("=" * 60)
    print("Test Complete!")
    print("=" * 60)


def test_multiclass_gpio():
    """Test multi-class GPIO interface."""
    print("\n" + "=" * 60)
    print("Testing Multi-Class GPIO Interface")
    print("=" * 60)
    print()

    gpio = MockMultiClassGPIO()

    # Setup pins
    class_pins = {
        "squirrel": 18,
        "skunk": 19,
        "raccoon": 20,
    }

    gpio.setup_classes(class_pins)
    print(f"GPIO pins configured: {class_pins}")

    # Test triggers
    print("\nTesting GPIO triggers:")
    for class_name in ["squirrel", "skunk", "raccoon"]:
        print(f"  Triggering {class_name} (GPIO {class_pins[class_name]})...")
        gpio.trigger_class(class_name, duration=0.1)
        state = gpio.get_pin_state(class_name)
        print(f"    State after trigger: {state}")

    gpio.cleanup()
    print("\n✅ GPIO test complete!")


if __name__ == "__main__":
    print("ML Detector Quick Test")
    print()

    try:
        test_detector()
        test_multiclass_gpio()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
