# Changelog

All notable changes to the Squirrel Detector project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-12-19

### Added
- Initial project setup with standard Python project structure (src layout)
- Camera interface abstraction with support for:
  - Raspberry Pi HQ Camera via `picamera2`
  - Video file interface for Windows development using OpenCV
- GPIO interface abstraction with support for:
  - Real GPIO control on Raspberry Pi via `gpiozero`
  - Mock GPIO interface for Windows development with callback support
- Squirrel detection module using computer vision:
  - Color-based detection (brown/reddish-brown color ranges)
  - Shape analysis (aspect ratio filtering, size filtering)
  - Configurable confidence thresholds
  - Center field-of-view detection with configurable region percentage
- Main application entry point with CLI:
  - Command-line argument parsing
  - Cross-platform camera initialization
  - GPIO pin configuration
  - Debug mode with visual output
  - Signal handling for graceful shutdown
- Comprehensive test suite with pytest:
  - 36 test cases covering all modules
  - 61% overall code coverage (94% for detector, 80% for utils)
  - Tests for camera, GPIO, detector, main app, and utilities
  - Platform-specific test skipping for Pi-only features
- GitHub Actions CI/CD workflows:
  - Multi-platform testing (Ubuntu, Windows, macOS)
  - Multiple Python version support (3.10, 3.11, 3.12, 3.13)
  - Code linting with ruff and black
  - Coverage reporting with pytest-cov
  - Automated version bumping on commits to main branch
  - PyPI publishing workflow
- Project documentation:
  - Comprehensive README with installation and usage instructions
  - Quick start guide (QUICKSTART.md)
  - Contributing guidelines (CONTRIBUTING.md)
  - Test video sourcing guide (docs/TEST_VIDEOS.md)
  - Project summary documentation
- Package configuration:
  - Modern `pyproject.toml` setup
  - Pip-installable package structure
  - Entry point: `squirrel-detector` command
  - Optional dependencies for Pi-specific features (`[pi]` extra)
  - Development dependencies group (`[dev]` extra)
- Utility scripts:
  - Version bumping script (`scripts/bump_version.py`)
  - Virtual environment setup scripts (Windows and Unix)
- Virtual environment setup:
  - Python 3.13 virtual environment configured
  - Requirements files for core, Pi-specific, and dev dependencies
- Pre-commit hooks configuration (optional)
- Makefile for common development tasks
- MIT License file

### Technical Details
- Python 3.10+ compatibility
- Uses OpenCV for computer vision operations
- Uses numpy for array operations
- Abstract base classes for extensibility
- Cross-platform compatibility (Raspberry Pi and Windows)

---

## [Unreleased]

### Future Enhancements
- Machine learning-based detection (YOLO, TensorFlow Lite)
- Configuration file support (YAML/JSON)
- Enhanced logging with file output
- Web interface for monitoring
- Email/SMS notifications on detection
- Video recording on detection
- Multi-camera support
- Detection history/analytics
