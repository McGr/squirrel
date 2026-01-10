"""Main entry point for the Squirrel Detector application."""

import argparse
import logging
import signal
import sys
import time
from typing import Optional

import cv2

from squirrel.camera import CameraInterface, PiCameraInterface, VideoCameraInterface
from squirrel.detector import SquirrelDetector
from squirrel.gpio import GPIOInterface, MockGPIOInterface, PiGPIOInterface
from squirrel.utils import is_raspberry_pi, is_windows

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class SquirrelDetectorApp:
    """Main application class for squirrel detection."""

    def __init__(
        self,
        camera: CameraInterface,
        gpio: GPIOInterface,
        gpio_pin: int,
        confidence_threshold: float = 0.5,
        center_threshold: float = 0.3,
        debug: bool = False,
    ):
        """Initialize the application.

        Args:
            camera: Camera interface
            gpio: GPIO interface
            gpio_pin: GPIO pin number to trigger
            confidence_threshold: Minimum confidence for detection
            center_threshold: Percentage of center region
            debug: Enable debug mode with visual output
        """
        self.camera = camera
        self.gpio = gpio
        self.gpio_pin = gpio_pin
        self.detector = SquirrelDetector(
            confidence_threshold=confidence_threshold,
            center_threshold=center_threshold,
        )
        self.debug = debug
        self.running = False

        # Setup GPIO
        self.gpio.setup(gpio_pin)

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
        logger.info("Starting squirrel detector...")
        self.camera.start()

        if not self.camera.is_opened():
            logger.error("Failed to open camera")
            return

        self.running = True
        last_trigger_time = 0
        trigger_cooldown = 2.0  # Minimum seconds between triggers

        logger.info(f"Monitoring for squirrels. GPIO pin {self.gpio_pin} will trigger on detection.")

        try:
            while self.running:
                frame = self.camera.read()

                if frame is None:
                    logger.warning("Failed to read frame")
                    time.sleep(0.1)
                    continue

                # Detect squirrel in center
                detected, bbox, confidence = self.detector.detect_and_check_center(frame)

                if detected:
                    current_time = time.time()
                    if current_time - last_trigger_time >= trigger_cooldown:
                        logger.info(
                            f"Squirrel detected in center! Confidence: {confidence:.2f}, "
                            f"BBox: {bbox}"
                        )
                        self.gpio.output(self.gpio_pin, True)
                        last_trigger_time = current_time

                        # Keep GPIO high for a short duration
                        time.sleep(0.5)
                        self.gpio.output(self.gpio_pin, False)

                if self.debug:
                    # Draw detection results on frame
                    self._draw_debug(frame, detected, bbox, confidence)
                    cv2.imshow("Squirrel Detector", frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        self.stop()

                time.sleep(0.033)  # ~30 FPS

        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        finally:
            self.cleanup()

    def _draw_debug(self, frame, detected, bbox, confidence):
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
            color = (0, 255, 0) if detected else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(
                frame,
                f"Squirrel: {confidence:.2f}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2,
            )

        # Draw status text
        status = "DETECTED" if detected else "Monitoring..."
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


def create_gpio_interface() -> GPIOInterface:
    """Create appropriate GPIO interface based on platform."""
    if is_raspberry_pi():
        try:
            return PiGPIOInterface()
        except ImportError:
            logger.warning("Raspberry Pi detected but gpiozero not available, using mock GPIO")
            return MockGPIOInterface()
    else:
        logger.info("Not running on Raspberry Pi, using mock GPIO interface")
        return MockGPIOInterface()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Squirrel Detector - Detect squirrels in camera view and trigger GPIO"
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
        "--gpio-pin",
        type=int,
        default=18,
        help="GPIO pin number to trigger (default: 18)",
    )
    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.5,
        help="Minimum confidence for detection (0.0-1.0, default: 0.5)",
    )
    parser.add_argument(
        "--center-threshold",
        type=float,
        default=0.3,
        help="Percentage of center region to consider (0.0-1.0, default: 0.3)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode with visual output",
    )

    args = parser.parse_args()

    try:
        camera = create_camera_interface(args)
        gpio = create_gpio_interface()

        app = SquirrelDetectorApp(
            camera=camera,
            gpio=gpio,
            gpio_pin=args.gpio_pin,
            confidence_threshold=args.confidence_threshold,
            center_threshold=args.center_threshold,
            debug=args.debug,
        )

        app.run()

    except Exception as e:
        logger.error(f"Error running application: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
