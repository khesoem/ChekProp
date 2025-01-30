import pytest
from gpiozero import InputDevice, GPIODeviceError, PinInvalidState
from hypothesis import given, strategies as st
from unittest import mock
from gpiozero.pins.mock import MockFactory

# Helper strategies to generate valid inputs for the InputDevice class
@given(
    pin=st.integers(min_value=0, max_value=27),  # Assume GPIO pins range from 0 to 27
    pull_up=st.one_of(st.none(), st.booleans()),  # pull_up can be None, True, or False
    active_state=st.one_of(st.none(), st.booleans()),  # active_state can be None, True, or False
)
def test_input_device_properties(pin, pull_up, active_state):
    # Create a MockFactory
    pin_factory = MockFactory()
    
    # If pin is in the range 2 to 3, pull_up must be True
    if pull_up != True and pin in range(2, 4):
        with pytest.raises(Exception):
            device = InputDevice(pin, pull_up=pull_up, active_state=active_state, pin_factory=pin_factory)
        return

    # When pull_up is None, active_state must not be None
    if pull_up is None and active_state is None:
        with pytest.raises(PinInvalidState):
            device = InputDevice(pin, pull_up=pull_up, active_state=active_state, pin_factory=pin_factory)
        return

    # If pull_up is not None, active_state must be None
    if pull_up is not None and active_state is not None:
        with pytest.raises(PinInvalidState):
            device = InputDevice(pin, pull_up=pull_up, active_state=active_state, pin_factory=pin_factory)
        return

    # Now create the device
    device = InputDevice(pin, pull_up=pull_up, active_state=active_state, pin_factory=pin_factory)

    # Property: Pin should be in input mode
    assert device.pin.function == 'input'

    # Property: Pull-up state should match the input pull_up value
    pull_state = {None: 'floating', True: 'up', False: 'down'}[pull_up]
    assert device.pin.pull == pull_state

    # Property: Active state should be computed correctly
    if pull_up is not None:
        assert device._active_state == (pull_up is False)
    else:
        assert device._active_state == bool(active_state)

    # Check is_active against mock pin's state
    if device._active_state:
        device.pin.drive_high()
        assert device.is_active
        device.pin.drive_low()
        assert not device.is_active
    else:
        device.pin.drive_high()
        assert not device.is_active
        device.pin.drive_low()
        assert device.is_active

    # Property: __repr__ string should contain the correct pin number and active state
    assert repr(device).startswith(f"<gpiozero.InputDevice object on pin GPIO{pin}")
    assert f"pull_up={pull_up}" in repr(device)

    # Close the device
    device.close()
    assert repr(device) == '<gpiozero.InputDevice object closed>'


@given(
    pin=st.integers(min_value=0, max_value=27),
    pull_up=st.booleans(),
)
def test_input_device_active_state(pin, pull_up):
    # Create a MockFactory
    pin_factory = MockFactory()
    
    # If pin is in the range 2 to 3, pull_up must be True
    if pull_up != True and pin in range(2, 4):
        with pytest.raises(Exception):
            device = InputDevice(pin, pull_up=pull_up, pin_factory=pin_factory)
        return

    # Now create the device
    device = InputDevice(pin, pull_up=pull_up, pin_factory=pin_factory)

    # When pull_up is True, active state should be False (LOW is active)
    if pull_up:
        device.pin.drive_low()
        assert device.is_active
        device.pin.drive_high()
        assert not device.is_active
    # When pull_up is False, active state should be True (HIGH is active)
    else:
        device.pin.drive_high()
        assert device.is_active
        device.pin.drive_low()
        assert not device.is_active

    device.close()