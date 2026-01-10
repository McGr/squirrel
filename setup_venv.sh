#!/bin/bash
# Setup script for Linux/Mac to create Python 3.13 virtual environment

set -e

echo "Creating Python 3.13 virtual environment..."
python3.13 -m venv venv || python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Upgrading pip..."
python -m pip install --upgrade pip

echo "Installing core dependencies..."
pip install -e .

echo "Installing development dependencies..."
pip install -e ".[dev]"

echo "Virtual environment setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
