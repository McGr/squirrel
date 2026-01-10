"""GPIO interface for Raspberry Pi and Windows emulation."""

from abc import ABC, abstractmethod
from typing import Optional

try:
    from gpiozero import OutputDevice
    GPIOZERO_AVAILABLE = True
except ImportError:
    GPIOZERO_AVAILABLE = False


class GPIOInterface(ABC):
    """Abstract base class for GPIO interfaces."""

    @abstractmethod
    def setup(self, pin: int) -> None:
        """Set up a GPIO pin as output."""
        pass

    @abstractmethod
    def output(self, pin: int, value: bool) -> None:
        """Set GPIO pin output value."""
        pass

    @abstractmethod
    def cleanup(self, pin: Optional[int] = None) -> None:
        """Clean up GPIO resources."""
        pass


class PiGPIOInterface(GPIOInterface):
    """Raspberry Pi GPIO interface using gpiozero."""

    def __init__(self):
        """Initialize Pi GPIO interface."""
        if not GPIOZERO_AVAILABLE:
            raise ImportError(
                "gpiozero is not available. Install with: pip install gpiozero"
            )
        self._pins: dict[int, OutputDevice] = {}

    def setup(self, pin: int) -> None:
        """Set up a GPIO pin as output."""
        if pin not in self._pins:
            self._pins[pin] = OutputDevice(pin)

    def output(self, pin: int, value: bool) -> None:
        """Set GPIO pin output value."""
        if pin not in self._pins:
            self.setup(pin)

        if value:
            self._pins[pin].on()
        else:
            self._pins[pin].off()

    def cleanup(self, pin: Optional[int] = None) -> None:
        """Clean up GPIO resources."""
        if pin is None:
            for device in self._pins.values():
                device.close()
            self._pins.clear()
        elif pin in self._pins:
            self._pins[pin].close()
            del self._pins[pin]


class MockGPIOInterface(GPIOInterface):
    """Mock GPIO interface for Windows development."""

    def __init__(self):
        """Initialize Mock GPIO interface."""
        self._pins: dict[int, bool] = {}
        self._callbacks: dict[int, list] = {}

    def setup(self, pin: int) -> None:
        """Set up a GPIO pin as output."""
        if pin not in self._pins:
            self._pins[pin] = False

    def output(self, pin: int, value: bool) -> None:
        """Set GPIO pin output value."""
        if pin not in self._pins:
            self.setup(pin)

        old_value = self._pins.get(pin, False)
        self._pins[pin] = value

        # Trigger callbacks if value changed
        if old_value != value and pin in self._callbacks:
            for callback in self._callbacks[pin]:
                callback(pin, value)

    def cleanup(self, pin: Optional[int] = None) -> None:
        """Clean up GPIO resources."""
        if pin is None:
            self._pins.clear()
            self._callbacks.clear()
        elif pin in self._pins:
            del self._pins[pin]
            if pin in self._callbacks:
                del self._callbacks[pin]

    def get_state(self, pin: int) -> bool:
        """Get the current state of a pin (for testing)."""
        return self._pins.get(pin, False)

    def add_callback(self, pin: int, callback) -> None:
        """Add a callback function for pin state changes (for testing)."""
        if pin not in self._callbacks:
            self._callbacks[pin] = []
        self._callbacks[pin].append(callback)
