from gpiozero import *
from examples.gpiozero.library.input_device.src.gpiozero.input_devices import InputDevice

def test_input_initial_values(mock_factory):
    pin = mock_factory.pin(4)
    with InputDevice(4, pull_up=True) as device:
        assert repr(device).startswith('<gpiozero.InputDevice object')
        assert pin.function == 'input'
        assert pin.pull == 'up'
        assert device.pull_up
    assert repr(device) == '<gpiozero.InputDevice object closed>'
    with InputDevice(4, pull_up=False) as device:
        assert pin.pull == 'down'
        assert not device.pull_up