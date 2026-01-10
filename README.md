# Squirrel Detector

A Python application designed to run on Raspberry Pi 4 that uses the HQ camera to detect squirrels in the center of the camera's field of view and trigger a GPIO pin. Also supports development on Windows 11 using video files.

## Features

- **Camera Support**: Works with Raspberry Pi HQ camera via `picamera2`, or video files on Windows
- **Squirrel Detection**: Uses computer vision techniques to detect squirrels in the camera frame
- **Center FOV Detection**: Only triggers when a squirrel is detected in the center region of the frame
- **GPIO Control**: Triggers GPIO pins on Raspberry Pi (emulated on Windows for development)
- **Cross-Platform**: Supports both Raspberry Pi and Windows 11 for development

## Installation

### From PyPI (when published)

```bash
pip install squirrel-detector
```

### From GitHub

```bash
pip install git+https://github.com/yourusername/squirrel.git
```

### For Raspberry Pi

```bash
pip install squirrel-detector[pi]
```

### Development Installation

```bash
git clone https://github.com/yourusername/squirrel.git
cd squirrel
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev,pi]"
```

## Usage

### On Raspberry Pi

```bash
squirrel-detector --camera 0 --gpio-pin 18
```

### On Windows (with video file)

```bash
squirrel-detector --video-path path/to/video.mp4 --gpio-pin 18
```

### Command Line Options

- `--camera`: Camera index (default: 0) - Raspberry Pi only
- `--video-path`: Path to video file for Windows development
- `--gpio-pin`: GPIO pin number to trigger (default: 18)
- `--center-threshold`: Percentage of center region to consider (default: 0.3)
- `--confidence-threshold`: Minimum confidence for detection (default: 0.5)
- `--debug`: Enable debug mode with visual output

## Project Structure

```
squirrel/
├── src/
│   └── squirrel/
│       ├── __init__.py
│       ├── main.py
│       ├── camera.py
│       ├── gpio.py
│       ├── detector.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   ├── test_camera.py
│   ├── test_gpio.py
│   ├── test_detector.py
│   └── test_main.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── pyproject.toml
├── README.md
└── requirements.txt
```

## Testing

Run tests with pytest:

```bash
pytest
```

With coverage:

```bash
pytest --cov=squirrel --cov-report=html
```

## Development

This project uses:
- Python 3.13+ (supports 3.10+)
- pytest for testing
- black for code formatting
- ruff for linting

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
