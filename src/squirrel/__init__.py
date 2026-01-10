"""Squirrel Detector - A Raspberry Pi application for detecting squirrels."""

__version__ = "0.1.0"

from squirrel.detector import SquirrelDetector
from squirrel.camera import CameraInterface, PiCameraInterface, VideoCameraInterface
from squirrel.gpio import GPIOInterface, PiGPIOInterface, MockGPIOInterface

__all__ = [
    "SquirrelDetector",
    "CameraInterface",
    "PiCameraInterface",
    "VideoCameraInterface",
    "GPIOInterface",
    "PiGPIOInterface",
    "MockGPIOInterface",
    "__version__",
]
