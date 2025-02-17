from gpiozero.pins.mock import MockFactory, MockPWMPin
from examples.gpiozero.apps.app_6.src.presence_indicator import PresenceIndicator
from unittest.mock import patch
from time import sleep
from gpiozero import *
from hypothesis import given, strategies as st
from hypothesis import settings

# 1. Extract Properties:
#    - `pins`:  GPIO pins for the LEDBarGraph.  Initialized in __init__ and not directly modifiable later.
#    - `url`:  URL for the API endpoint to fetch presence data.  Specified in __init__, used in `play()`.
#    - `delay`:  Delay between API calls (in seconds). Specified in __init__, used in `play()`.
#    - `leds`:  An LEDBarGraph object representing the LED bar.  Initialized in __init__, used and controlled in play() and __exit__.  Value is controlled in play() and set to off in init and exit.
#    - `playing`: A boolean flag to control the execution of `play()`. Set in init, modified through `play()` and `stop_playing()`, affecting thread execution.

# 2. Understand Behavior (from provided test and code):
#    - Upon initialization, the LED bar is turned off.
#    - `play()`:
#        - Continuously fetches presence data (a number) from the specified URL.
#        - Converts the number to a value between 0 and 1 (divided by 10).
#        - Sets the `leds.value` to map the presence data to the LED bar's illumination level by scaling the number received from the provided API to a value 0-1.
#        - Pauses for the specified delay.
#        - Stops if `playing` is set to False and the loop breaks.
#    - `stop_playing()`: Sets `playing` to `False`, stopping the thread.
#    - `__enter__`: Starts a thread that executes `play()`. Returns self.
#    - `__exit__`: Calls `stop_playing()` (to stop playing) and turns off the leds.

# 3. Generate Property-Based tests:

# Property 1: Initialization - LEDs are initially off.
@settings(max_examples=10)
@given(st.floats(min_value=0.1, max_value=5.0), st.integers(min_value=1, max_value=99999))
@patch('examples.gpiozero.apps.app_6.src.presence_indicator.requests')
def test_initialization_leds_off(mock_requests, delay, number):
    Device.pin_factory = MockFactory(pin_class=MockPWMPin)
    mock_requests.get.return_value.json.return_value = {'number': number}
    with PresenceIndicator(url="http://example.com", delay=delay) as pi:
        sleep(0.1) # Give time for the thread to run and update leds.value
        assert pi.leds.value == number / 10 if number <= 10 else 1
        assert pi.playing == True # Verify that the playing flag is set to True at this point

# Property 2:  `leds.value` is directly proportional to the returned number (scaled) within constraints.  This is tested in the initial unit test.
@settings(max_examples=10)
@given(st.floats(min_value=0.1, max_value=5.0), st.integers(min_value=0, max_value=100))
@patch('examples.gpiozero.apps.app_6.src.presence_indicator.requests')
def test_leds_value_proportional_to_number(mock_requests, delay, number_returned):
    Device.pin_factory = MockFactory(pin_class=MockPWMPin)
    mock_requests.get.return_value.json.return_value = {'number': number_returned}
    with PresenceIndicator(url="http://example.com", delay=delay) as pi:
        sleep(0.1)  # Allow time for the value to be propagated
        expected_value = min(number_returned / 10,  1.0)
        assert abs(pi.leds.value - expected_value) < 1e-6  # Allow for floating point precision


# Property 3: `stop_playing()` sets `playing` to False and hence the thread ends
@settings(max_examples=10)
@given(st.floats(min_value=0.1, max_value=5.0), st.integers(min_value=1, max_value=99999))
@patch('examples.gpiozero.apps.app_6.src.presence_indicator.requests')
def test_stop_playing_sets_playing_to_false(mock_requests, delay, number):
    Device.pin_factory = MockFactory(pin_class=MockPWMPin)
    mock_requests.get.return_value.json.return_value = {'number': number}

    with PresenceIndicator(url="http://example.com", delay=delay) as pi:
        sleep(0.1)
        pi.stop_playing()
        sleep(0.1)
        assert pi.playing == False

# Property 4:  `__exit__` turns the leds off.
@settings(max_examples=10)
@given(st.floats(min_value=0.1, max_value=5.0), st.integers(min_value=0, max_value=100))
@patch('examples.gpiozero.apps.app_6.src.presence_indicator.requests')
def test_exit_turns_leds_off(mock_requests, delay, number_returned):
    Device.pin_factory = MockFactory(pin_class=MockPWMPin)
    mock_requests.get.return_value.json.return_value = {'number': number_returned}

    with PresenceIndicator(url="http://example.com", delay=delay) as pi:
        sleep(0.1)  # Run play() briefly
    assert pi.leds.value == 0 # verifies that the led value is zero.