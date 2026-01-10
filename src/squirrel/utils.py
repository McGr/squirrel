"""Utility functions for the Squirrel Detector project."""

import platform
import sys
from typing import Optional


def is_raspberry_pi() -> bool:
    """Check if running on Raspberry Pi."""
    try:
        with open("/proc/cpuinfo", "r", encoding="utf-8") as f:
            cpuinfo = f.read()
            return "Raspberry Pi" in cpuinfo or "BCM" in cpuinfo
    except (FileNotFoundError, PermissionError):
        return False


def is_windows() -> bool:
    """Check if running on Windows."""
    return platform.system() == "Windows"


def get_platform() -> str:
    """Get the current platform."""
    if is_raspberry_pi():
        return "raspberry_pi"
    if is_windows():
        return "windows"
    return platform.system().lower()


def validate_version() -> bool:
    """Validate Python version is 3.10 or higher."""
    return sys.version_info >= (3, 10)
