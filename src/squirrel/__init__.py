"""Squirrel Detector - A Raspberry Pi application for detecting squirrels."""

__version__ = "0.1.0"

from squirrel.detector import SquirrelDetector
from squirrel.detector_ml import MLDetector
from squirrel.camera import CameraInterface, PiCameraInterface, VideoCameraInterface
from squirrel.gpio import GPIOInterface, PiGPIOInterface, MockGPIOInterface
from squirrel.gpio_multiclass import (
    MultiClassGPIOInterface,
    PiMultiClassGPIO,
    MockMultiClassGPIO,
)

__all__ = [
    "SquirrelDetector",
    "MLDetector",
    "CameraInterface",
    "PiCameraInterface",
    "VideoCameraInterface",
    "GPIOInterface",
    "PiGPIOInterface",
    "MockGPIOInterface",
    "MultiClassGPIOInterface",
    "PiMultiClassGPIO",
    "MockMultiClassGPIO",
    "__version__",
]
