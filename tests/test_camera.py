"""Tests for camera interfaces."""

import os
import tempfile

import cv2
import numpy as np
import pytest

from squirrel.camera import (
    CameraInterface,
    PiCameraInterface,
    VideoCameraInterface,
)


class TestVideoCameraInterface:
    """Tests for VideoCameraInterface."""

    def test_init(self):
        """Test VideoCameraInterface initialization."""
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            temp_path = f.name

        # Create a dummy video file
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(temp_path, fourcc, 20.0, (640, 480))
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        out.write(frame)
        out.release()

        try:
            camera = VideoCameraInterface(temp_path)
            assert camera.video_path == temp_path
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_start_stop(self):
        """Test starting and stopping video camera."""
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            temp_path = f.name

        # Create a dummy video file
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(temp_path, fourcc, 20.0, (640, 480))
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        for _ in range(10):
            out.write(frame)
        out.release()

        try:
            camera = VideoCameraInterface(temp_path)
            camera.start()
            assert camera.is_opened() is True
            assert camera.width > 0
            assert camera.height > 0
            camera.stop()
            assert camera.is_opened() is False
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_read_frame(self):
        """Test reading frames from video."""
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            temp_path = f.name

        # Create a video with colored frames
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(temp_path, fourcc, 20.0, (640, 480))
        for i in range(5):
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            frame[:, :] = [i * 50, i * 50, i * 50]  # Different shades
            out.write(frame)
        out.release()

        try:
            camera = VideoCameraInterface(temp_path)
            camera.start()
            frame = camera.read()
            assert frame is not None
            assert isinstance(frame, np.ndarray)
            assert len(frame.shape) == 3
            camera.stop()
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_invalid_video_path(self):
        """Test error handling for invalid video path."""
        camera = VideoCameraInterface("nonexistent_video.mp4")
        with pytest.raises(ValueError, match="Could not open video file"):
            camera.start()


class TestPiCameraInterface:
    """Tests for PiCameraInterface."""

    def test_init(self):
        """Test PiCameraInterface initialization."""
        try:
            camera = PiCameraInterface(camera_index=0, width=1920, height=1080)
            assert camera.camera_index == 0
            assert camera.width == 1920
            assert camera.height == 1080
        except ImportError:
            pytest.skip("picamera2 not available (expected on non-Pi systems)")

    def test_import_error(self, monkeypatch):
        """Test ImportError when picamera2 is not available."""
        import squirrel.camera as camera_module

        original_import = camera_module.PICAMERA2_AVAILABLE
        camera_module.PICAMERA2_AVAILABLE = False

        with pytest.raises(ImportError, match="picamera2 is not available"):
            PiCameraInterface()

        camera_module.PICAMERA2_AVAILABLE = original_import
