"""Script to bump version number in pyproject.toml and __init__.py."""

import re
import sys
from pathlib import Path


def bump_version_patch(version: str) -> str:
    """Bump the patch version (least significant digit)."""
    parts = version.split(".")
    if len(parts) != 3:
        raise ValueError(f"Version must be in format X.Y.Z, got: {version}")
    major, minor, patch = parts
    new_patch = str(int(patch) + 1)
    return f"{major}.{minor}.{new_patch}"


def update_pyproject_toml(new_version: str) -> None:
    """Update version in pyproject.toml."""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    content = pyproject_path.read_text(encoding="utf-8")
    
    # Update version in [project] section
    def replace_version(match):
        return f'{match.group(1)}{new_version}{match.group(3)}'
    
    pattern = r'(^version\s*=\s*")([^"]+)(")'
    content = re.sub(pattern, replace_version, content, flags=re.MULTILINE)
    
    pyproject_path.write_text(content, encoding="utf-8")
    print(f"Updated pyproject.toml version to {new_version}")


def update_init_py(new_version: str) -> None:
    """Update version in __init__.py."""
    init_path = Path(__file__).parent.parent / "src" / "squirrel" / "__init__.py"
    content = init_path.read_text(encoding="utf-8")
    
    # Update __version__ assignment
    def replace_version(match):
        return f'{match.group(1)}{new_version}{match.group(3)}'
    
    pattern = r'(^__version__\s*=\s*")([^"]+)(")'
    content = re.sub(pattern, replace_version, content, flags=re.MULTILINE)
    
    init_path.write_text(content, encoding="utf-8")
    print(f"Updated __init__.py version to {new_version}")


def main():
    """Main function."""
    # Read current version from pyproject.toml
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    if not pyproject_path.exists():
        print("Error: pyproject.toml not found")
        sys.exit(1)
    
    content = pyproject_path.read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    if not match:
        print("Error: Could not find version in pyproject.toml")
        sys.exit(1)
    
    current_version = match.group(1)
    new_version = bump_version_patch(current_version)
    
    print(f"Bumping version from {current_version} to {new_version}")
    
    update_pyproject_toml(new_version)
    update_init_py(new_version)


if __name__ == "__main__":
    main()
