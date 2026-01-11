"""GPIO interface for multi-class detection with different pins per class."""

from abc import ABC, abstractmethod
from typing import Dict, Optional

try:
    from gpiozero import OutputDevice

    GPIOZERO_AVAILABLE = True
except ImportError:
    GPIOZERO_AVAILABLE = False


class MultiClassGPIOInterface(ABC):
    """Abstract base class for multi-class GPIO interfaces."""

    @abstractmethod
    def setup_classes(self, class_pins: Dict[str, int]) -> None:
        """Set up GPIO pins for detection classes.

        Args:
            class_pins: Dictionary mapping class names to GPIO pin numbers
        """
        pass

    @abstractmethod
    def trigger_class(self, class_name: str, duration: float = 0.5) -> None:
        """Trigger GPIO pin for a specific class.

        Args:
            class_name: Name of the detected class
            duration: Duration to keep pin high (seconds)
        """
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """Clean up GPIO resources."""
        pass


class PiMultiClassGPIO(MultiClassGPIOInterface):
    """Raspberry Pi multi-class GPIO interface using gpiozero."""

    def __init__(self):
        """Initialize Pi multi-class GPIO interface."""
        if not GPIOZERO_AVAILABLE:
            raise ImportError(
                "gpiozero is not available. Install with: pip install gpiozero"
            )
        self._class_pins: Dict[str, int] = {}
        self._devices: Dict[str, OutputDevice] = {}

    def setup_classes(self, class_pins: Dict[str, int]) -> None:
        """Set up GPIO pins for detection classes.

        Args:
            class_pins: Dictionary mapping class names to GPIO pin numbers
        """
        self._class_pins = class_pins.copy()

        # Setup devices for each class
        for class_name, pin in class_pins.items():
            if class_name not in self._devices:
                self._devices[class_name] = OutputDevice(pin)

    def trigger_class(self, class_name: str, duration: float = 0.5) -> None:
        """Trigger GPIO pin for a specific class.

        Args:
            class_name: Name of the detected class
            duration: Duration to keep pin high (seconds)
        """
        import time

        if class_name not in self._devices:
            # Auto-setup if not already set up
            if class_name in self._class_pins:
                self._devices[class_name] = OutputDevice(self._class_pins[class_name])
            else:
                return

        # Turn on
        self._devices[class_name].on()

        # Wait for duration
        time.sleep(duration)

        # Turn off
        self._devices[class_name].off()

    def cleanup(self) -> None:
        """Clean up GPIO resources."""
        for device in self._devices.values():
            device.close()
        self._devices.clear()
        self._class_pins.clear()


class MockMultiClassGPIO(MultiClassGPIOInterface):
    """Mock multi-class GPIO interface for Windows development."""

    def __init__(self):
        """Initialize Mock multi-class GPIO interface."""
        self._class_pins: Dict[str, int] = {}
        self._pin_states: Dict[int, bool] = {}
        self._callbacks: Dict[str, list] = {}

    def setup_classes(self, class_pins: Dict[str, int]) -> None:
        """Set up GPIO pins for detection classes.

        Args:
            class_pins: Dictionary mapping class names to GPIO pin numbers
        """
        self._class_pins = class_pins.copy()

        # Initialize pin states
        for pin in class_pins.values():
            if pin not in self._pin_states:
                self._pin_states[pin] = False

    def trigger_class(self, class_name: str, duration: float = 0.5) -> None:
        """Trigger GPIO pin for a specific class.

        Args:
            class_name: Name of the detected class
            duration: Duration to keep pin high (seconds)
        """
        import time

        if class_name not in self._class_pins:
            return

        pin = self._class_pins[class_name]

        # Turn on
        old_state = self._pin_states.get(pin, False)
        self._pin_states[pin] = True

        # Trigger callbacks
        if class_name in self._callbacks:
            for callback in self._callbacks[class_name]:
                callback(class_name, pin, True)

        # Wait for duration
        time.sleep(duration)

        # Turn off
        self._pin_states[pin] = False

        # Trigger callbacks
        if class_name in self._callbacks:
            for callback in self._callbacks[class_name]:
                callback(class_name, pin, False)

    def cleanup(self) -> None:
        """Clean up GPIO resources."""
        self._class_pins.clear()
        self._pin_states.clear()
        self._callbacks.clear()

    def get_pin_state(self, class_name: str) -> bool:
        """Get the current state of a pin for a class (for testing).

        Args:
            class_name: Name of the class

        Returns:
            Current pin state (True/False)
        """
        if class_name not in self._class_pins:
            return False
        pin = self._class_pins[class_name]
        return self._pin_states.get(pin, False)

    def add_callback(self, class_name: str, callback) -> None:
        """Add a callback function for class triggers (for testing).

        Args:
            class_name: Name of the class
            callback: Callback function(class_name, pin, state)
        """
        if class_name not in self._callbacks:
            self._callbacks[class_name] = []
        self._callbacks[class_name].append(callback)
