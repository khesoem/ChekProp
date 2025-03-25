import pytest
from hypothesis import given, strategies as st, settings
from gpiozero import InputDevice, Device
from gpiozero.pins.mock import MockFactory, MockPin
from gpiozero.exc import PinInvalidState

# 1. Extract Properties:
#    - pin:  The GPIO pin the device is connected to.  (via GPIODevice superclass, tested implicitly)
#    - pull_up:  Whether a pull-up resistor is used (True), pull-down (False), or floating (None).
#    - active_state: Whether the device is active when the pin is HIGH.
#    - is_active:  Whether the device is currently active (derived from pin state and active_state).
#    - pin_factory: The factory used to create the pins, defaults to None.
#    - pin.function: should be "input"
#    - pin.pull: "up", "down", or "floating" base on argument pull_up
#    - Device is closed

# 2. Understand Class Behavior (from provided tests and code):
#    - `pull_up` setting impacts pin pull direction.
#    - `active_state` is derived from `pin_state` and the constructor args.
#    - Exceptions are raised for invalid combinations of parameters (e.g., floating pin without active_state).
#    - `__repr__` provides a string representation of the device, including pin, pull_up, and is_active.
#    - Device should close correctly.

# 3. Property-Based Tests:

# Settings for hypothesis (adjust as needed)
settings.register_profile("ci", deadline=None) # disable deadline if tests run too long
settings.load_profile("ci")

@pytest.fixture(autouse=True)
def mock_pin_factory():
    Device.pin_factory = MockFactory(pin_class=MockPin)
    yield
    Device.pin_factory = None  # reset after each test to avoid side effects




@given(st.booleans())
def test_pull_up_affects_pin_pull(pull_up):
    with InputDevice(4, pull_up=pull_up) as device:
        if pull_up:
            assert device.pin.pull == 'up'
            assert device.pull_up is True
        else:
            assert device.pin.pull == 'down'
            assert device.pull_up is False

@given(st.none())
def test_pull_up_none_affects_pin_pull(pull_up):
    with pytest.raises(PinInvalidState):
        InputDevice(4, pull_up=pull_up) # must define active_state

@given(st.booleans())
def test_active_state_affects_is_active_basic(active_state):
      with InputDevice(4, pull_up=False, active_state=active_state) as device:
          device.pin.state = 1
          assert device.is_active == active_state
          device.pin.state = 0
          assert device.is_active == (not active_state)
      with InputDevice(4, pull_up=True, active_state=active_state) as device:
          device.pin.state = 1
          assert device.is_active == (not active_state) # opposite because of the pullup
          device.pin.state = 0
          assert device.is_active == active_state

@given(st.booleans(), st.booleans())
def test_is_active_reflects_pin_state_and_pull_up(pull_up, pin_state):
    with InputDevice(4, pull_up=pull_up) as device:
        device.pin.state = pin_state
        if pull_up:
            assert device.is_active == (pin_state == 0)  # Pull-up inverts
        else:
            assert device.is_active == (pin_state == 1)

@given(st.booleans(), st.sampled_from([0, 1]))
def test_is_active_reflects_pin_state_with_active_state(active_state, pin_state):
    with InputDevice(4, pull_up=None, active_state=active_state) as device:
        device.pin.state = pin_state
        assert device.is_active == (pin_state == 1 and active_state) or (pin_state == 0 and not active_state)

@given(st.booleans(), st.integers(min_value=1, max_value=10))
def test_initialization_sets_pin_function(pull_up, pin):
    with InputDevice(pin, pull_up=pull_up) as device:
        assert device.pin.function == 'input'


# def test_repr_contains_expected_values():
#     with InputDevice(pin=5, pull_up=True) as device:
#         expected_str = f"<gpiozero.InputDevice object on pin <MockPin object on 5>, pull_up=True, is_active={device.is_active}>"
#         assert str(device).startswith("<gpiozero.InputDevice object")
#         assert "pull_up=True" in str(device)
#         assert str(device).endswith(f"is_active={device.is_active}>")
#
#     with InputDevice(pin=6, pull_up=False) as device:
#         assert "pull_up=False" in str(device)
#
#
# def test_closed_repr():
#     device = InputDevice(7, pull_up=True)
#     device.close()
#     assert str(device) == "<gpiozero.InputDevice object closed>"

@given(st.booleans())
def test_close_releases_pin(pull_up):
    device = InputDevice(8, pull_up=pull_up)
    device.close()
    assert device.pin.function is None
    assert device.pin.pull is None  # pin.pull is set to None during close