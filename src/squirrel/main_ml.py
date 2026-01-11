"""ML-based main entry point for multi-class wildlife detection."""

import argparse
import logging
import signal
import sys
import time
from typing import Dict, Optional

import cv2

from squirrel.camera import CameraInterface, PiCameraInterface, VideoCameraInterface
from squirrel.detector_ml import MLDetector
from squirrel.gpio_multiclass import (
    MultiClassGPIOInterface,
    MockMultiClassGPIO,
    PiMultiClassGPIO,
)
from squirrel.utils import is_raspberry_pi, is_windows

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class WildlifeDetectorApp:
    """Main application class for ML-based multi-class wildlife detection."""

    def __init__(
        self,
        camera: CameraInterface,
        gpio: MultiClassGPIOInterface,
        class_pins: Dict[str, int],
        model_path: Optional[str] = None,
        confidence_threshold: float = 0.25,
        center_threshold: float = 0.3,
        device: str = "cpu",
        debug: bool = False,
    ):
        """Initialize the ML-based application.

        Args:
            camera: Camera interface
            gpio: Multi-class GPIO interface
            class_pins: Dictionary mapping class names to GPIO pins
            model_path: Path to trained YOLO model
            confidence_threshold: Minimum confidence for detection
            center_threshold: Percentage of center region
            device: Device for inference (cpu, cuda, etc.)
            debug: Enable debug mode with visual output
        """
        self.camera = camera
        self.gpio = gpio
        self.class_pins = class_pins.copy()
        self.detector = MLDetector(
            model_path=model_path,
            confidence_threshold=confidence_threshold,
            center_threshold=center_threshold,
            device=device,
        )
        self.debug = debug
        self.running = False

        # Setup GPIO for all classes
        self.gpio.setup_classes(self.class_pins)

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logger.info("Received shutdown signal, stopping...")
        self.stop()

    def stop(self):
        """Stop the application."""
        self.running = False

    def run(self):
        """Run the main detection loop."""
        logger.info("Starting wildlife detector with ML model...")
        logger.info(f"Classes: {list(self.class_pins.keys())}")
        logger.info(f"GPIO pins: {self.class_pins}")
        self.camera.start()

        if not self.camera.is_opened():
            logger.error("Failed to open camera")
            return

        self.running = True
        last_trigger_time: Dict[str, float] = {}
        trigger_cooldown = 2.0  # Minimum seconds between triggers per class

        logger.info("Monitoring for wildlife. GPIO pins will trigger on detection.")

        try:
            while self.running:
                frame = self.camera.read()

                if frame is None:
                    logger.warning("Failed to read frame")
                    time.sleep(0.1)
                    continue

                # Detect wildlife in center
                detected, bbox, confidence, class_name = self.detector.detect_and_check_center(
                    frame
                )

                if detected and class_name:
                    current_time = time.time()
                    last_time = last_trigger_time.get(class_name, 0)

                    if current_time - last_time >= trigger_cooldown:
                        logger.info(
                            f"{class_name.capitalize()} detected in center! "
                            f"Confidence: {confidence:.2f}, BBox: {bbox}"
                        )

                        # Trigger GPIO for this class
                        self.gpio.trigger_class(class_name, duration=0.5)
                        last_trigger_time[class_name] = current_time

                if self.debug:
                    # Draw detection results on frame
                    self._draw_debug(frame, detected, bbox, confidence, class_name)
                    cv2.imshow("Wildlife Detector (ML)", frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        self.stop()

                time.sleep(0.033)  # ~30 FPS

        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        finally:
            self.cleanup()

    def _draw_debug(self, frame, detected, bbox, confidence, class_name):
        """Draw debug information on frame."""
        height, width = frame.shape[:2]

        # Draw center region
        center_region_width = int(width * self.detector.center_threshold)
        center_region_height = int(height * self.detector.center_threshold)
        center_x = width // 2
        center_y = height // 2
        x1 = center_x - center_region_width // 2
        y1 = center_y - center_region_height // 2
        x2 = center_x + center_region_width // 2
        y2 = center_y + center_region_height // 2
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Draw bounding box if detected
        if detected and bbox:
            x, y, w, h = bbox

            # Class-specific colors
            if class_name == "squirrel":
                color = (0, 255, 255)  # Yellow
            elif class_name == "skunk":
                color = (255, 255, 255)  # White
            elif class_name == "raccoon":
                color = (128, 128, 128)  # Gray
            else:
                color = (0, 255, 0)  # Green

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

            cv2.putText(
                frame,
                f"{class_name.capitalize()}: {confidence:.2f}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2,
            )

        # Draw status text
        status = f"{class_name.capitalize()} DETECTED" if detected and class_name else "Monitoring..."
        cv2.putText(
            frame,
            status,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0) if detected else (255, 255, 255),
            2,
        )

    def cleanup(self):
        """Clean up resources."""
        logger.info("Cleaning up...")
        self.camera.stop()
        self.gpio.cleanup()
        if self.debug:
            cv2.destroyAllWindows()


def create_camera_interface(args) -> CameraInterface:
    """Create appropriate camera interface based on platform and arguments."""
    if args.video_path:
        if not is_windows():
            logger.warning("Video path specified on non-Windows platform, using it anyway")
        return VideoCameraInterface(args.video_path)

    if is_raspberry_pi():
        return PiCameraInterface(camera_index=args.camera, width=1920, height=1080)
    else:
        # Fallback to OpenCV camera on other platforms
        import cv2

        class OpenCVCameraInterface(CameraInterface):
            """OpenCV camera interface for non-Pi platforms."""

            def __init__(self, camera_index: int = 0):
                self.camera_index = camera_index
                self._cap: Optional[cv2.VideoCapture] = None

            def start(self):
                self._cap = cv2.VideoCapture(self.camera_index)

            def stop(self):
                if self._cap:
                    self._cap.release()

            def read(self):
                if self._cap:
                    ret, frame = self._cap.read()
                    return frame if ret else None
                return None

            def is_opened(self):
                return self._cap is not None and self._cap.isOpened()

            @property
            def width(self):
                return int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH)) if self._cap else 0

            @property
            def height(self):
                return int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) if self._cap else 0

        logger.warning(
            "Not running on Raspberry Pi. Using OpenCV camera interface. "
            "For best results, use --video-path with a video file on Windows."
        )
        return OpenCVCameraInterface(camera_index=args.camera)


def create_multiclass_gpio() -> MultiClassGPIOInterface:
    """Create appropriate multi-class GPIO interface based on platform."""
    if is_raspberry_pi():
        try:
            return PiMultiClassGPIO()
        except ImportError:
            logger.warning("Raspberry Pi detected but gpiozero not available, using mock GPIO")
            return MockMultiClassGPIO()
    else:
        logger.info("Not running on Raspberry Pi, using mock GPIO interface")
        return MockMultiClassGPIO()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Wildlife Detector (ML) - Detect squirrels, skunks, and raccoons with ML model"
    )
    parser.add_argument(
        "--camera",
        type=int,
        default=0,
        help="Camera index (default: 0). Raspberry Pi only when not using --video-path",
    )
    parser.add_argument(
        "--video-path",
        type=str,
        default=None,
        help="Path to video file for Windows development",
    )
    parser.add_argument(
        "--model-path",
        type=str,
        default=None,
        help="Path to trained YOLO model (.pt file). If not provided, uses default location or pre-trained model.",
    )
    parser.add_argument(
        "--squirrel-pin",
        type=int,
        default=18,
        help="GPIO pin for squirrel detection (default: 18)",
    )
    parser.add_argument(
        "--skunk-pin",
        type=int,
        default=19,
        help="GPIO pin for skunk detection (default: 19)",
    )
    parser.add_argument(
        "--raccoon-pin",
        type=int,
        default=20,
        help="GPIO pin for raccoon detection (default: 20)",
    )
    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.25,
        help="Minimum confidence for detection (0.0-1.0, default: 0.25)",
    )
    parser.add_argument(
        "--center-threshold",
        type=float,
        default=0.3,
        help="Percentage of center region to consider (0.0-1.0, default: 0.3)",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        help="Device for inference: cpu, cuda, 0, 1, etc. (default: cpu)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode with visual output",
    )

    args = parser.parse_args()

    # Map class names to GPIO pins
    class_pins = {
        "squirrel": args.squirrel_pin,
        "skunk": args.skunk_pin,
        "raccoon": args.raccoon_pin,
    }

    try:
        camera = create_camera_interface(args)
        gpio = create_multiclass_gpio()

        app = WildlifeDetectorApp(
            camera=camera,
            gpio=gpio,
            class_pins=class_pins,
            model_path=args.model_path,
            confidence_threshold=args.confidence_threshold,
            center_threshold=args.center_threshold,
            device=args.device,
            debug=args.debug,
        )

        app.run()

    except Exception as e:
        logger.error(f"Error running application: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
