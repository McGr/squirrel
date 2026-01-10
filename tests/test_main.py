"""Tests for main application."""

import tempfile

import cv2
import numpy as np
import pytest

from squirrel.camera import VideoCameraInterface
from squirrel.detector import SquirrelDetector
from squirrel.gpio import MockGPIOInterface
from squirrel.main import SquirrelDetectorApp


class TestSquirrelDetectorApp:
    """Tests for SquirrelDetectorApp."""

    @pytest.fixture
    def temp_video(self):
        """Create a temporary video file for testing."""
        import os
        import time

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            temp_path = f.name

        # Create a video with a brown rectangle
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(temp_path, fourcc, 20.0, (640, 480))
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        # Add a brown rectangle in the center
        frame[200:280, 270:370] = [42, 42, 165]  # Brownish in center
        for _ in range(10):
            out.write(frame)
        out.release()
        # Give Windows time to release the file handle
        time.sleep(0.1)

        yield temp_path

        # Cleanup - try multiple times on Windows
        if os.path.exists(temp_path):
            for _ in range(5):
                try:
                    os.unlink(temp_path)
                    break
                except (PermissionError, OSError):
                    time.sleep(0.1)

    @pytest.fixture
    def app(self, temp_video):
        """Create a test application instance."""
        camera = VideoCameraInterface(temp_video)
        gpio = MockGPIOInterface()
        app = SquirrelDetectorApp(
            camera=camera,
            gpio=gpio,
            gpio_pin=18,
            confidence_threshold=0.3,
            center_threshold=0.5,
            debug=False,
        )
        yield app
        # Ensure cleanup happens
        if hasattr(app, 'camera') and app.camera.is_opened():
            app.camera.stop()

    def test_app_init(self, app):
        """Test application initialization."""
        assert app.camera is not None
        assert app.gpio is not None
        assert app.gpio_pin == 18
        assert app.detector is not None
        assert app.running is False

    def test_stop(self, app):
        """Test application stop."""
        app.stop()
        assert app.running is False

    def test_gpio_setup(self, app):
        """Test that GPIO pin is set up."""
        app.camera.start()
        try:
            # Pin should be initialized (False state)
            assert app.gpio.get_state(18) is False
        finally:
            app.camera.stop()

    def test_cleanup(self, app):
        """Test application cleanup."""
        app.camera.start()
        app.cleanup()
        assert app.camera.is_opened() is False

    def test_draw_debug(self, app):
        """Test debug drawing functionality."""
        app.debug = True
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        bbox = (200, 200, 100, 100)

        # Should not raise exception
        app._draw_debug(frame, True, bbox, 0.8)
        app._draw_debug(frame, False, None, 0.0)

    def test_signal_handler(self, app):
        """Test signal handler."""
        app.running = True
        app._signal_handler(None, None)
        assert app.running is False
