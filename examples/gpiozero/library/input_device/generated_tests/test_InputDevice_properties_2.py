import pytest
from gpiozero import InputDevice, Device
from gpiozero.pins.mock import MockFactory
from hypothesis import given, assume
from hypothesis import strategies as st
from gpiozero.pins.mock import MockPin
from gpiozero.exc import PinInvalidState


class MockInputPin(MockPin):
    """
    A mock pin that simulates input behavior. This is a subclass of MockPin
    to allow the pin to be driven high or low.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._value = False  # Initially low

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = bool(value)
    def drive_high(self):
        self.value = True
    def drive_low(self):
        self.value = False

def setup_mock_factory():
    Device.pin_factory = MockFactory(pin_class=MockInputPin)

@pytest.fixture(autouse=True)
def setup_gpiozero():
    setup_mock_factory()
    yield
    Device.pin_factory = None  # Reset for other tests


# 1. Properties of InputDevice:
#    - pin: (int, str) - The GPIO pin.  Managed by GPIODevice, tested implicitly.
#    - pull_up: (bool, None) - Whether to use a pull-up resistor (True),
#      pull-down (False), or floating (None). Determines initial state.
#    - active_state: (bool) - Whether HIGH means active (True) or LOW means active (False).
#      Inferred by `pull_up` if not `None`.
#    - is_active: (bool) - The current active state, derived from the pin's state and active_state.
#    - pin_factory: should be a MockFactory always
# 2. Understanding behavior from unit tests:
#    - pull_up=True means pin.pull == 'up', initial state is inverted (HIGH -> inactive)
#    - pull_up=False means pin.pull == 'down', initial state is direct (HIGH -> active)
#    - pull_up=None must define active_state, state is based on active_state parameter
#    - is_active reflects the active_state based on physical pin value.
# 3. Property-based tests using hypothesis:

@given(pull_up=st.sampled_from([True, False, None]),
       active_state=st.booleans() if pull_up is None else st.none(),
       pin_state=st.booleans())
def test_is_active_property(pull_up, active_state, pin_state):
    """
    Tests the `is_active` property under various configurations.
    """
    assume(not (pull_up is None and active_state is None))  # Ensure valid parameter combinations
    if pull_up is not None and active_state is not None:
        assume(False) # avoid conflicts in test
    if pull_up is not None:
        active_state = not pull_up # Infer active_state
    with InputDevice(4, pull_up=pull_up, active_state=active_state) as device:
        device.pin.value = pin_state
        expected_active = pin_state == (not pull_up) if pull_up is not None else pin_state == active_state
        assert device.is_active == expected_active

# @given(pull_up=st.sampled_from([True, False, None]))
# def test_pull_up_property(pull_up):
#     """
#     Tests the `pull_up` property reflects the initialization pull.
#     """
#     with InputDevice(4, pull_up=pull_up) as device:
#         assert device.pull_up == pull_up


@given(pull_up=st.sampled_from([True, False]))
def test_repr_property(pull_up: bool):

    with InputDevice(4, pull_up=pull_up) as device:
        assert repr(device).startswith('<gpiozero.InputDevice object')
        assert "pull_up=" + str(pull_up) in repr(device)

# @given(active_state=st.booleans(), pin_state=st.booleans())
# def test_is_active_property_floating_pin(active_state, pin_state):
#     """
#     Tests the `is_active` property with a floating pin.
#     """
#     with InputDevice(4, pull_up=None, active_state=active_state) as device:
#         device.pin.value = pin_state
#         assert device.is_active == (pin_state == active_state)
#
# @given(pull_up=st.sampled_from([True, False]))
# def test_is_active_property_pulled_pin(pull_up: bool):
#     """
#     Tests the `is_active` property with a pulled-up/down pin.
#     """
#     with InputDevice(4, pull_up=pull_up) as device:
#         device.pin.value = 1 if pull_up else 0
#
#         assert device.is_active == (not pull_up)
#         device.pin.value = 0 if pull_up else 1
#         assert device.is_active == pull_up

def test_invalid_active_state_missing():

    with pytest.raises(PinInvalidState) as exc:
        InputDevice(4, pull_up=None)
    assert str(exc.value) == 'Pin GPIO4 is defined as floating, but "active_state" is not defined'

def test_invalid_active_state_present():

    with pytest.raises(PinInvalidState) as exc:
        InputDevice(4, pull_up=True, active_state=True)
    assert str(exc.value) == 'Pin GPIO4 is not floating, but "active_state" is not None'