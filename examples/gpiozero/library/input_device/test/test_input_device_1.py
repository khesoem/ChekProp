import pytest
from hypothesis import given
from hypothesis import strategies as st
from gpiozero import InputDevice, GPIODevice, Device
from gpiozero.pins.mock import MockFactory

# Generate a strategy for pins
pin_strategy = st.integers(min_value=0, max_value=10)

# Boolean or None strategy
bool_or_none = st.one_of(st.booleans(), st.none())

# Generate a strategy for pins with predefined pull values
prefixed_pin_strategy = st.integers(min_value=2, max_value=3)

def mock_factory():
    save_factory = Device.pin_factory
    Device.pin_factory = MockFactory()
    try:
        yield Device.pin_factory
        # This reset() may seem redundant given we're re-constructing the
        # factory for each function that requires it but MockFactory (via
        # LocalFactory) stores some info at the class level which reset()
        # clears.
    finally:
        if Device.pin_factory is not None:
            Device.pin_factory.reset()
        Device.pin_factory = save_factory

# Test changing prefixed pull of a pin
@given(
    pin=prefixed_pin_strategy,
    pull_up=bool_or_none,
    active_state=bool_or_none,
)
def test_changing_prefixed_pin_pull(pin, pull_up, active_state):
    pin_factory = mock_factory()
    # Test initialization raises errors for invalid input combinations
    if pull_up is not True:
        with pytest.raises(Exception):
            device = InputDevice(pin, pull_up=pull_up, active_state=active_state, pin_factory=pin_factory)

# Test initialization
@given(
    pin=pin_strategy,
    pull_up=bool_or_none,
    active_state=bool_or_none,
)
def test_input_device_initialization(pin, pull_up, active_state):
    pin_factory = MockFactory()
    # Test initialization does not raise errors for valid input combinations
    if (pull_up is None and active_state is None) or (pull_up is not None and active_state is not None):
        with pytest.raises(Exception):
            device = InputDevice(pin, pull_up=pull_up, active_state=active_state, pin_factory=pin_factory)
    elif pull_up != True and pin in range(2, 4):
        with pytest.raises(Exception):
            device = InputDevice(pin, pull_up=pull_up, active_state=active_state, pin_factory=pin_factory)
    else:
        device = InputDevice(pin=pin, pull_up=pull_up, active_state=active_state, pin_factory=pin_factory)
        assert isinstance(device, InputDevice)

# # Test pull_up property
# @given(
#     pull_up=bool_or_none,
#     active_state=bool_or_none,
#     pin_factory=pin_factory_strategy(),
# )
# def test_pull_up_property(pull_up, active_state, pin_factory):
#     pin = MockPin(2)
#     if pull_up is None and active_state is None:
#         with pytest.raises(Exception):
#             device = InputDevice(pin, pull_up=pull_up, active_state=active_state, pin_factory=pin_factory)
#     else:
#         device = InputDevice(pin, pull_up=pull_up, active_state=active_state, pin_factory=pin_factory)
#         if pull_up is None:
#             assert device.pull_up is None
#         else:
#             assert device.pull_up == pull_up

# # Test is_active property consistency
# @given(
#     pin=pin_strategy,
#     pull_up=bool_or_none,
#     active_state=bool_or_none,
#     pin_factory=pin_factory_strategy(),
# )
# def test_is_active_property(pin, pull_up, active_state, pin_factory):
#     if pull_up is None and active_state is None:
#         with pytest.raises(Exception):
#             device = InputDevice(pin, pull_up=pull_up, active_state=active_state, pin_factory=pin_factory)
#     else:
#         device = InputDevice(pin, pull_up=pull_up, active_state=active_state, pin_factory=pin_factory)
#         if pull_up is True:
#             assert device.is_active == (not device.pin.state)
#         elif pull_up is False:
#             assert device.is_active == device.pin.state
