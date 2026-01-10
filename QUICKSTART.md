# Quick Start Guide

## Installation

### On Windows (Development)

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd squirrel
   setup_venv.bat
   venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

3. **Run tests**:
   ```bash
   pytest
   ```

4. **Run with a test video**:
   ```bash
   squirrel-detector --video-path path/to/squirrel_video.mp4 --debug
   ```

### On Raspberry Pi

1. **Install the package**:
   ```bash
   pip install -e ".[pi]"
   ```

2. **Run with camera**:
   ```bash
   squirrel-detector --camera 0 --gpio-pin 18 --debug
   ```

## Finding Test Videos

See `docs/TEST_VIDEOS.md` for information on where to find or create test videos for Windows development.

## Project Structure

- `src/squirrel/` - Main source code
- `tests/` - Test suite
- `scripts/` - Utility scripts (version bumping, etc.)
- `.github/workflows/` - CI/CD workflows

## Development Commands

```bash
# Run tests
pytest

# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Install pre-commit hooks
pre-commit install
```

## Version Bumping

Version is automatically bumped on commits to main branch via GitHub Actions. To manually bump:

```bash
python scripts/bump_version.py
```
