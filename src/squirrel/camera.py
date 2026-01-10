"""Camera interface for Raspberry Pi and video file support."""

from abc import ABC, abstractmethod
from typing import Optional

import cv2
import numpy as np

try:
    from picamera2 import Picamera2
    PICAMERA2_AVAILABLE = True
except ImportError:
    PICAMERA2_AVAILABLE = False


class CameraInterface(ABC):
    """Abstract base class for camera interfaces."""

    @abstractmethod
    def start(self) -> None:
        """Start the camera."""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Stop the camera."""
        pass

    @abstractmethod
    def read(self) -> Optional[np.ndarray]:
        """Read a frame from the camera."""
        pass

    @abstractmethod
    def is_opened(self) -> bool:
        """Check if camera is opened."""
        pass

    @property
    @abstractmethod
    def width(self) -> int:
        """Get frame width."""
        pass

    @property
    @abstractmethod
    def height(self) -> int:
        """Get frame height."""
        pass


class PiCameraInterface(CameraInterface):
    """Raspberry Pi HQ Camera interface using picamera2."""

    def __init__(self, camera_index: int = 0, width: int = 1920, height: int = 1080):
        """Initialize Pi Camera interface.

        Args:
            camera_index: Camera index (typically 0 for HQ camera)
            width: Frame width
            height: Frame height
        """
        if not PICAMERA2_AVAILABLE:
            raise ImportError(
                "picamera2 is not available. Install with: pip install picamera2"
            )

        self.camera_index = camera_index
        self._width = width
        self._height = height
        self._camera: Optional[Picamera2] = None

    def start(self) -> None:
        """Start the camera."""
        if self._camera is not None:
            return

        self._camera = Picamera2(self.camera_index)
        config = self._camera.create_preview_configuration(
            main={"size": (self._width, self._height)}
        )
        self._camera.configure(config)
        self._camera.start()

    def stop(self) -> None:
        """Stop the camera."""
        if self._camera is not None:
            self._camera.stop()
            self._camera.close()
            self._camera = None

    def read(self) -> Optional[np.ndarray]:
        """Read a frame from the camera."""
        if self._camera is None:
            return None

        try:
            frame = self._camera.capture_array()
            # Convert from RGB to BGR for OpenCV compatibility
            if len(frame.shape) == 3:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            return frame
        except Exception:
            return None

    def is_opened(self) -> bool:
        """Check if camera is opened."""
        return self._camera is not None

    @property
    def width(self) -> int:
        """Get frame width."""
        return self._width

    @property
    def height(self) -> int:
        """Get frame height."""
        return self._height


class VideoCameraInterface(CameraInterface):
    """Video file camera interface for Windows development."""

    def __init__(self, video_path: str):
        """Initialize Video Camera interface.

        Args:
            video_path: Path to video file
        """
        self.video_path = video_path
        self._cap: Optional[cv2.VideoCapture] = None
        self._width: int = 0
        self._height: int = 0

    def start(self) -> None:
        """Start the video capture."""
        if self._cap is not None:
            return

        self._cap = cv2.VideoCapture(self.video_path)
        if not self._cap.isOpened():
            raise ValueError(f"Could not open video file: {self.video_path}")

        self._width = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self._height = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def stop(self) -> None:
        """Stop the video capture."""
        if self._cap is not None:
            self._cap.release()
            self._cap = None

    def read(self) -> Optional[np.ndarray]:
        """Read a frame from the video."""
        if self._cap is None:
            return None

        ret, frame = self._cap.read()
        if not ret:
            # Loop the video
            self._cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self._cap.read()
            if not ret:
                return None

        return frame

    def is_opened(self) -> bool:
        """Check if video capture is opened."""
        return self._cap is not None and self._cap.isOpened()

    @property
    def width(self) -> int:
        """Get frame width."""
        return self._width

    @property
    def height(self) -> int:
        """Get frame height."""
        return self._height
