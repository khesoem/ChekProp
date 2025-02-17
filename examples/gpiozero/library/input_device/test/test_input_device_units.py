from gpiozero import *
from gpiozero.pins.mock import MockFactory

def test_input_initial_values():
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