import pytest
from gpiozero.pins import \
    (
    pin_factory
)  # MockFactory and MockPin are added here
from unittest import mock
from gpiozero.devices import (
    GPIODevice,
    CompositeDevice,
)
from gpiozero.exc import \
    InputDeviceError  # MockFactoryError for the testing environment
from gpiozero.pins import MockPin
from gpiozero.pins import Factory  # Import the Factory
from gpiozero import InputDevice

# Mock up a factory function that creates a mock pin for the test environment
class MockFactory:
    def __init__(self, pin_class=None, pin_factory=None):
        self.pin_class = pin_class
        if pin_factory is not None:
            self.pin_factory = pin_factory
    def pin(self, pin):
        if self.pin_class is None:  # or MockPin:
            return MockPin(pin)
        else:
            return self.pin_class(port=pin)


class TestInputDeviceProperty:
    """
    Property based tests for the InputDevice class.
    """

    def test_pull_up_property(self):
        """
        Test the 'pull_up' property.
        """
        # Test with pull_up True
        device = InputDevice(pin=1, pull_up=True)
        assert device.pull_up is True
        device.close()

        # Test with pull_up False
        device = InputDevice(pin=1, pull_up=False)
        assert device.pull_up is False
        device.close()

    def test_active_state_property(self):
        """
        Test the 'active_state' property.
        """
        # Test with pull_up True and active_state set to None
        device = InputDevice(pin=1, pull_up=True)
        assert device._active_state is not None
        device.close()

        # Test with pull_up False and active_state set to None
        device = InputDevice(pin=1, pull_up=False)
        assert device._active_state is not None
        device.close()

        # Test with pull_up None and valid active_state
        device = InputDevice(pin=1, pull_up=None, active_state=True)
        assert device._active_state is True
        device.close()

        device = InputDevice(pin=1, pull_up=None, active_state=False)
        assert device._active_state is False
        device.close()

    def test_pin_pull_setting(self):
        """
        Test that the pin pull setting is configured correctly.
        """
        # Test pull_up True
        mock_factory = MockFactory()
        device = InputDevice(pin=1, pull_up=True, pin_factory=mock_factory)
        assert mock_factory.pin(1).pull == 'up'
        device.close()

        # Test pull_up False
        mock_factory = MockFactory()
        device = InputDevice(pin=1, pull_up=False, pin_factory=mock_factory)
        assert mock_factory.pin(1).pull == 'down'
        device.close()

        # Test pull_up None
        mock_factory = MockFactory()
        device = InputDevice(pin=1, pull_up=None, active_state=True, pin_factory=mock_factory)
        assert mock_factory.pin(1).pull == 'floating'
        device.close()

    def test_initialization_with_invalid_state(self):
        """
        Test initialization with invalid active_state settings.
        """
        with pytest.raises(InputDeviceError):
            InputDevice(pin=1, pull_up=None, active_state=None)
        with pytest.raises(InputDeviceError):
            InputDevice(pin=1, pull_up=True, active_state=True)  # Should not allow this config