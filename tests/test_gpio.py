"""Tests for GPIO interfaces."""

import pytest

from squirrel.gpio import (
    GPIOInterface,
    MockGPIOInterface,
    PiGPIOInterface,
)


class TestMockGPIOInterface:
    """Tests for MockGPIOInterface."""

    def test_init(self):
        """Test MockGPIOInterface initialization."""
        gpio = MockGPIOInterface()
        assert gpio._pins == {}
        assert gpio._callbacks == {}

    def test_setup(self):
        """Test GPIO pin setup."""
        gpio = MockGPIOInterface()
        gpio.setup(18)
        assert 18 in gpio._pins
        assert gpio._pins[18] is False

    def test_output(self):
        """Test GPIO pin output."""
        gpio = MockGPIOInterface()
        gpio.output(18, True)
        assert gpio.get_state(18) is True
        gpio.output(18, False)
        assert gpio.get_state(18) is False

    def test_output_auto_setup(self):
        """Test that output automatically sets up pin."""
        gpio = MockGPIOInterface()
        gpio.output(18, True)
        assert 18 in gpio._pins
        assert gpio.get_state(18) is True

    def test_cleanup_all(self):
        """Test cleanup of all pins."""
        gpio = MockGPIOInterface()
        gpio.setup(18)
        gpio.setup(19)
        gpio.cleanup()
        assert gpio._pins == {}
        assert gpio._callbacks == {}

    def test_cleanup_single_pin(self):
        """Test cleanup of single pin."""
        gpio = MockGPIOInterface()
        gpio.setup(18)
        gpio.setup(19)
        gpio.cleanup(18)
        assert 18 not in gpio._pins
        assert 19 in gpio._pins

    def test_callback(self):
        """Test callback functionality."""
        gpio = MockGPIOInterface()
        callback_called = []
        callback_values = []

        def test_callback(pin, value):
            callback_called.append(pin)
            callback_values.append(value)

        gpio.add_callback(18, test_callback)
        gpio.output(18, True)
        assert 18 in callback_called
        assert True in callback_values

    def test_callback_only_on_change(self):
        """Test callback only triggers on value change."""
        gpio = MockGPIOInterface()
        callback_count = 0

        def test_callback(pin, value):
            nonlocal callback_count
            callback_count += 1

        gpio.add_callback(18, test_callback)
        gpio.output(18, True)
        assert callback_count == 1
        gpio.output(18, True)  # Same value
        assert callback_count == 1  # Should not increment
        gpio.output(18, False)
        assert callback_count == 2  # Should increment


class TestPiGPIOInterface:
    """Tests for PiGPIOInterface."""

    def test_init(self):
        """Test PiGPIOInterface initialization."""
        try:
            gpio = PiGPIOInterface()
            assert gpio._pins == {}
        except ImportError:
            pytest.skip("gpiozero not available (expected on non-Pi systems)")

    def test_import_error(self, monkeypatch):
        """Test ImportError when gpiozero is not available."""
        import squirrel.gpio as gpio_module

        original_import = gpio_module.GPIOZERO_AVAILABLE
        gpio_module.GPIOZERO_AVAILABLE = False

        with pytest.raises(ImportError, match="gpiozero is not available"):
            PiGPIOInterface()

        gpio_module.GPIOZERO_AVAILABLE = original_import
