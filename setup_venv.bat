@echo off
REM Setup script for Windows to create Python 3.13 virtual environment

echo Creating Python 3.13 virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing core dependencies...
pip install -e .

echo Installing development dependencies...
pip install -e ".[dev]"

echo Virtual environment setup complete!
echo.
echo To activate the virtual environment, run:
echo   venv\Scripts\activate.bat
