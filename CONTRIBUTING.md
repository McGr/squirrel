# Contributing to Squirrel Detector

Thank you for your interest in contributing to the Squirrel Detector project!

## Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/squirrel.git
   cd squirrel
   ```

2. **Create a virtual environment** (Python 3.13 recommended):
   ```bash
   # Windows
   setup_venv.bat
   
   # Linux/Mac
   chmod +x setup_venv.sh
   ./setup_venv.sh
   
   # Or manually
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev,pi]"
   ```

3. **Install pre-commit hooks** (optional but recommended):
   ```bash
   pre-commit install
   ```

## Running Tests

Run the full test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=squirrel --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_detector.py
```

## Code Style

This project uses:
- **Black** for code formatting
- **Ruff** for linting

Format code:
```bash
black src/ tests/
ruff check --fix src/ tests/
```

Or use the Makefile:
```bash
make format
```

## Making Changes

1. Create a new branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and ensure tests pass:
   ```bash
   pytest
   make lint
   ```

3. Commit your changes (follow conventional commits if possible):
   ```bash
   git commit -m "feat: add new feature"
   ```

4. Push and create a pull request

## Version Bumping

Version bumping is handled automatically by GitHub Actions when pushing to the main branch. The patch version (least significant digit) is automatically incremented.

To manually bump version:
```bash
python scripts/bump_version.py
```

## Testing on Windows

For Windows development, use video files:
```bash
squirrel-detector --video-path path/to/test_video.mp4 --debug
```

See `docs/TEST_VIDEOS.md` for information on finding test videos.

## Testing on Raspberry Pi

On a Raspberry Pi, install the Pi-specific dependencies:
```bash
pip install -e ".[pi]"
```

Then run with the camera:
```bash
squirrel-detector --camera 0 --gpio-pin 18 --debug
```

## Project Structure

```
squirrel/
├── src/squirrel/      # Main source code
├── tests/             # Test suite
├── scripts/           # Utility scripts
├── docs/              # Documentation
└── .github/workflows/ # CI/CD workflows
```

## Questions?

Feel free to open an issue for questions or discussions!
