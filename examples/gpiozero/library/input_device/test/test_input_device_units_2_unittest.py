import unittest
from gpiozero import *
from gpiozero.pins.mock import MockFactory
from examples.gpiozero.library.input_device.src.input_devices import InputDevice

class UnitTest2(unittest.TestCase):
    def test_input_initial_values(self):
        # Create a MockFactory and use it as pin_factory on Device
        Device.pin_factory = MockFactory()
        with InputDevice(4, pull_up=True) as device:
            assert repr(device).startswith('<gpiozero.InputDevice object')
            assert device.pin.function == 'input'
            assert device.pin.pull == 'up'
            assert device.pull_up
        assert repr(device) == '<gpiozero.InputDevice object closed>'
        with InputDevice(4, pull_up=False) as device:
            assert device.pin.pull == 'down'
            assert not device.pull_up

    def test_input_is_active_low(self):
        # Create a MockFactory and use it as pin_factory on Device
        Device.pin_factory = MockFactory()
        with InputDevice(2, pull_up=True) as device:
            device.pin.drive_high()
            assert not device.is_active
            assert repr(device) == '<gpiozero.InputDevice object on pin GPIO2, pull_up=True, is_active=False>'
            device.pin.drive_low()
            assert device.is_active
            assert repr(device) == '<gpiozero.InputDevice object on pin GPIO2, pull_up=True, is_active=True>'

    def test_input_is_active_high(self):
        # Create a MockFactory and use it as pin_factory on Device
        Device.pin_factory = MockFactory()
        with InputDevice(4, pull_up=False) as device:
            device.pin.drive_high()
            assert device.is_active
            assert repr(device) == '<gpiozero.InputDevice object on pin GPIO4, pull_up=False, is_active=True>'
            device.pin.drive_low()
            assert not device.is_active
            assert repr(device) == '<gpiozero.InputDevice object on pin GPIO4, pull_up=False, is_active=False>'

    def test_input_pulled_up(self):
        # Create a MockFactory and use it as pin_factory on Device
        Device.pin_factory = MockFactory()
        with self.assertRaises(PinFixedPull):
            InputDevice(2, pull_up=False)

    def test_input_is_active_low_externally_pulled_up(self):
        # Create a MockFactory and use it as pin_factory on Device
        Device.pin_factory = MockFactory()
        device = InputDevice(4, pull_up=None, active_state=False)
        device.pin.drive_high()
        assert repr(device) == '<gpiozero.InputDevice object on pin GPIO4, pull_up=None, is_active=False>'
        assert not device.is_active
        device.pin.drive_low()
        assert repr(device) == '<gpiozero.InputDevice object on pin GPIO4, pull_up=None, is_active=True>'
        assert device.is_active

    def test_input_is_active_high_externally_pulled_down(self):
        # Create a MockFactory and use it as pin_factory on Device
        Device.pin_factory = MockFactory()
        device = InputDevice(4, pull_up=None, active_state=True)
        device.pin.drive_high()
        assert repr(device) == '<gpiozero.InputDevice object on pin GPIO4, pull_up=None, is_active=True>'
        assert device.is_active
        device.pin.drive_low()
        assert repr(device) == '<gpiozero.InputDevice object on pin GPIO4, pull_up=None, is_active=False>'
        assert not device.is_active

    def test_input_invalid_pull_up(self):
        # Create a MockFactory and use it as pin_factory on Device
        Device.pin_factory = MockFactory()
        with self.assertRaises(PinInvalidState) as exc:
            InputDevice(4, pull_up=None)
        assert str(exc.exception) == 'Pin GPIO4 is defined as floating, but "active_state" is not defined'

    def test_input_invalid_active_state(self):
        # Create a MockFactory and use it as pin_factory on Device
        Device.pin_factory = MockFactory()
        with self.assertRaises(PinInvalidState) as exc:
            InputDevice(4, active_state=True)
        assert str(exc.exception) == 'Pin GPIO4 is not floating, but "active_state" is not None'

if __name__ == '__main__':
    unittest.main()