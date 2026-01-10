"""Tests for utility functions."""

import platform
import sys

import pytest

from squirrel.utils import get_platform, is_raspberry_pi, is_windows, validate_version


def test_validate_version():
    """Test Python version validation."""
    assert validate_version() is True
    # Should work for Python 3.10+


def test_is_windows():
    """Test Windows detection."""
    result = is_windows()
    # Should match actual platform
    assert isinstance(result, bool)
    if platform.system() == "Windows":
        assert result is True


def test_is_raspberry_pi():
    """Test Raspberry Pi detection."""
    result = is_raspberry_pi()
    # Should return False on non-Pi systems
    assert isinstance(result, bool)
    # On Windows/development machines, should be False
    if platform.system() == "Windows":
        assert result is False


def test_get_platform():
    """Test platform detection."""
    platform_name = get_platform()
    assert isinstance(platform_name, str)
    assert platform_name in ["raspberry_pi", "windows", "linux", "darwin"]
