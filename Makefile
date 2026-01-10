.PHONY: help install install-dev test lint format clean venv setup

help:
	@echo "Available commands:"
	@echo "  make setup        - Set up virtual environment and install dependencies"
	@echo "  make install      - Install the package in editable mode"
	@echo "  make install-dev  - Install with development dependencies"
	@echo "  make test         - Run tests with pytest"
	@echo "  make lint         - Run linters (ruff)"
	@echo "  make format       - Format code with black and ruff"
	@echo "  make clean        - Clean up build artifacts"
	@echo "  make venv         - Create virtual environment (Python 3.13)"

venv:
	python3.13 -m venv venv || python3 -m venv venv
	@echo "Virtual environment created. Activate with: source venv/bin/activate"

setup: venv
	. venv/bin/activate && pip install --upgrade pip
	. venv/bin/activate && pip install -e ".[dev]"
	@echo "Setup complete! Activate the venv with: source venv/bin/activate"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest -v --cov=squirrel --cov-report=term-missing --cov-report=html

test-fast:
	pytest -v

lint:
	ruff check src/ tests/
	black --check src/ tests/

format:
	black src/ tests/
	ruff check --fix src/ tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
