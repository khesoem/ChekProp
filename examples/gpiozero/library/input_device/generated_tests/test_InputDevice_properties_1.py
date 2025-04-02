import unittest
from gpiozero import InputDevice, Device, PinInvalidState, PinFixedPull
from gpiozero.pins.mock import MockFactory, MockPin
from hypothesis import given, assume, HealthCheck, settings
from hypothesis import strategies as st
from hypothesis.errors import InvalidArgument


class MockInputPin(MockPin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._value = False  # Initialize to a default value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = bool(value)  # Ensure value is boolean


class TestInputDeviceProperties(unittest.TestCase):

    def setUp(self):
        # Reset the pin factory before each test to avoid cross-test contamination
        Device.pin_factory = MockFactory(pin_class=MockInputPin)  # Or a fresh MockFactory if needed.

    @settings(suppress_health_check=[HealthCheck.differing_executors])
    @given(pull_up=st.sampled_from([True, False]))
    def test_repr_property(self, pull_up: bool):

        with InputDevice(4, pull_up=pull_up) as device:
            assert repr(device).startswith('<gpiozero.InputDevice object')
            assert "pull_up=" + str(pull_up) in repr(device)

    # def test_invalid_active_state_missing(self):
    #     with self.assertRaises(PinInvalidState) as exc:
    #         InputDevice(4, pull_up=None)
    #     assert str(exc.exception) == 'Pin GPIO4 is defined as floating, but "active_state" is not defined'
    #
    # def test_invalid_active_state_present(self):
    #     with self.assertRaises(PinInvalidState) as exc:
    #         InputDevice(4, pull_up=True, active_state=True)
    #     assert str(exc.exception) == 'Pin GPIO4 is not floating, but "active_state" is not None'
    #
    # def test_input_initial_values(self):
    #     # Create a MockFactory and use it as pin_factory on Device
    #     Device.pin_factory = MockFactory()
    #     with InputDevice(4, pull_up=True) as device:
    #         assert repr(device).startswith('<gpiozero.InputDevice object')
    #         assert device.pin.function == 'input'
    #         assert device.pin.pull == 'up'
    #         assert device.pull_up
    #     assert repr(device) == '<gpiozero.InputDevice object closed>'
    #     with InputDevice(4, pull_up=False) as device:
    #         assert device.pin.pull == 'down'
    #         assert not device.pull_up
    #
    # def test_input_is_active_low(self):
    #     # Create a MockFactory and use it as pin_factory on Device
    #     Device.pin_factory = MockFactory()
    #     with InputDevice(2, pull_up=True) as device:
    #         device.pin.drive_high()
    #         assert not device.is_active
    #         assert repr(device) == '<gpiozero.InputDevice object on pin GPIO2, pull_up=True, is_active=False>'
    #         device.pin.drive_low()
    #         assert device.is_active
    #         assert repr(device) == '<gpiozero.InputDevice object on pin GPIO2, pull_up=True, is_active=True>'
    #
    # def test_input_is_active_high(self):
    #     # Create a MockFactory and use it as pin_factory on Device
    #     Device.pin_factory = MockFactory()
    #     with InputDevice(4, pull_up=False) as device:
    #         device.pin.drive_high()
    #         assert device.is_active
    #         assert repr(device) == '<gpiozero.InputDevice object on pin GPIO4, pull_up=False, is_active=True>'
    #         device.pin.drive_low()
    #         assert not device.is_active
    #         assert repr(device) == '<gpiozero.InputDevice object on pin GPIO4, pull_up=False, is_active=False>'
    #
    # def test_input_pulled_up(self):
    #     # Create a MockFactory and use it as pin_factory on Device
    #     Device.pin_factory = MockFactory()
    #     with self.assertRaises(PinFixedPull):
    #         InputDevice(2, pull_up=False)
    #
    # def test_input_is_active_low_externally_pulled_up(self):
    #     # Create a MockFactory and use it as pin_factory on Device
    #     Device.pin_factory = MockFactory()
    #     device = InputDevice(4, pull_up=None, active_state=False)
    #     device.pin.drive_high()
    #     assert repr(device) == '<gpiozero.InputDevice object on pin GPIO4, pull_up=None, is_active=False>'
    #     assert not device.is_active
    #     device.pin.drive_low()
    #     assert repr(device) == '<gpiozero.InputDevice object on pin GPIO4, pull_up=None, is_active=True>'
    #     assert device.is_active
    #
    # def test_input_is_active_high_externally_pulled_down(self):
    #     # Create a MockFactory and use it as pin_factory on Device
    #     Device.pin_factory = MockFactory()
    #     device = InputDevice(4, pull_up=None, active_state=True)
    #     device.pin.drive_high()
    #     assert repr(device) == '<gpiozero.InputDevice object on pin GPIO4, pull_up=None, is_active=True>'
    #     assert device.is_active
    #     device.pin.drive_low()
    #     assert repr(device) == '<gpiozero.InputDevice object on pin GPIO4, pull_up=None, is_active=False>'
    #     assert not device.is_active
    #
    # def test_input_invalid_pull_up(self):
    #     # Create a MockFactory and use it as pin_factory on Device
    #     Device.pin_factory = MockFactory()
    #     with self.assertRaises(PinInvalidState) as exc:
    #         InputDevice(4, pull_up=None)
    #     assert str(exc.exception) == 'Pin GPIO4 is defined as floating, but "active_state" is not defined'
    #
    # def test_input_invalid_active_state(self):
    #     # Create a MockFactory and use it as pin_factory on Device
    #     Device.pin_factory = MockFactory()
    #     with self.assertRaises(PinInvalidState) as exc:
    #         InputDevice(4, active_state=True)
    #     assert str(exc.exception) == 'Pin GPIO4 is not floating, but "active_state" is not None'

if __name__ == '__main__':
    unittest.main()