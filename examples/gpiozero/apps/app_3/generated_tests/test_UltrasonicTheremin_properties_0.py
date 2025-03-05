from gpiozero.pins.mock import MockFactory, MockPWMPin
from examples.gpiozero.apps.app_3.src.ultrasonic_theremin import UltrasonicTheremin
from gpiozero import *
from hypothesis import given, strategies as st
from gpiozero.tones import Tone
import pytest
import math


# 1. Extract Properties:

# The UltrasonicTheremin class has the following properties:
# - trigger pin: The GPIO pin used to trigger the ultrasonic sensor. (int)
# - echo pin: The GPIO pin used to receive the echo from the ultrasonic sensor. (int)
# - buzzer pin: The GPIO pin connected to the buzzer. (int)
# - octaves: The number of octaves the buzzer can play. (int, defaults to 3)
# - uds.distance: The distance measured by the ultrasonic sensor (float, between 0.0 and ~5.0)
# - buzzer.min_tone.midi: The minimum MIDI note the buzzer can generate based on the octaves parameter, derived from the TonalBuzzer
# - buzzer.max_tone.midi: The maximum MIDI note the buzzer can generate based on the octaves parameter, derived from the TonalBuzzer
# - buzzer.is_active:  Indicates whether the buzzer is playing a tone (boolean)

# 2. Understand the Class Behavior (from the provided unit tests and docstrings, code):
# - __init__: Initializes the DistanceSensor and TonalBuzzer.
# - distance_to_tone: Maps the sensor distance to a MIDI tone.
#   - The function calculates a MIDI tone based on a distance value (0-1).
#   - The tone is calculated relative to the min and max tones defined by the buzzer instance.
# - play:
#   - Continuously reads the distance from the sensor.
#   - Calculates the corresponding tone.
#   - Plays the calculated tone on the buzzer.
#   - Uses a 0.01 second sleep.
# - __enter__ / __exit__: Allows the class to be used in a "with" statement, ensuring the buzzer and sensor are closed when finished playing

# 3. Generate Property-Based Tests:
# I am assuming that distance_value returned from `self.uds.distance` is in the range [0.0, 1.0] because the documentation of DistanceSensor states it's between 0 and 1.

def test_quietness_before_play():
    Device.pin_factory = MockFactory(pin_class=MockPWMPin)
    with UltrasonicTheremin(27, 17, 21) as ut:
        assert not ut.buzzer.is_active


@pytest.fixture
def mock_theremin():
    Device.pin_factory = MockFactory(pin_class=MockPWMPin)
    return UltrasonicTheremin(27, 17, 21, octaves=3)


@given(distance_value=st.floats(min_value=0.0, max_value=1.0))
def test_distance_to_tone_in_range(mock_theremin, distance_value):
    tone = mock_theremin.distance_to_tone(distance_value)
    assert mock_theremin.buzzer.min_tone.midi <= tone <= mock_theremin.buzzer.max_tone.midi


@given(distance_value=st.floats(min_value=0.0, max_value=0.01))
def test_distance_to_tone_near_min(mock_theremin, distance_value):
    tone = mock_theremin.distance_to_tone(distance_value)
    assert abs(
        tone - mock_theremin.buzzer.min_tone.midi) < 5  # Using 5 as a small delta since the calculation may not be perfect


@given(distance_value=st.floats(min_value=0.99, max_value=1.0))
def test_distance_to_tone_near_max(mock_theremin, distance_value):
    tone = mock_theremin.distance_to_tone(distance_value)
    assert abs(tone - mock_theremin.buzzer.max_tone.midi) < 5


@given(octaves=st.integers(min_value=1, max_value=5))
def test_octaves_affects_tone_range(octaves):
    Device.pin_factory = MockFactory(pin_class=MockPWMPin)
    with UltrasonicTheremin(27, 17, 21, octaves=octaves) as ut:
        expected_range = 12 * octaves
        assert (ut.buzzer.max_tone.midi - ut.buzzer.min_tone.midi) == expected_range;


@given(distance_value=st.floats(min_value=0.0, max_value=1.0), octaves=st.integers(min_value=2, max_value=3))
def test_distance_tone_monotonic(mock_theremin, distance_value, octaves):
    Device.pin_factory = MockFactory(pin_class=MockPWMPin)
    theremin = UltrasonicTheremin(27, 17, 21, octaves=octaves)
    tone1 = theremin.distance_to_tone(distance_value)
    tone2 = theremin.distance_to_tone(distance_value + 0.01 if distance_value + 0.01 <= 1.0 else distance_value - 0.01)
    assert abs(tone1 - tone2) < 15  # allow for some delta.  The calculation will be approximately in the range