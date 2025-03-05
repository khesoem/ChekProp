from io import StringIO
from unittest.mock import patch
from gpiozero.pins.mock import MockFactory
from examples.gpiozero.apps.app_1.src.laser_tripwire import LaserTripwire  # Assuming the code is in src.laser_tripwire
from time import sleep
from gpiozero import Device
from hypothesis import given, settings
from hypothesis import strategies as st
from gpiozero.pins.mock import MockPWMPin


# 1. Extract Properties:
#    - The LaserTripwire class inherits from LightSensor.
#    - It's activated (detects an intruder) when it becomes dark.
#    - When dark, it triggers the 'when_dark' function, printing "INTRUDER".
#    - The constructor takes an ldr_pin (integer) as input.
#    - The underlying LightSensor behavior of dark/light is determined by the MockFactory when the code is running
#      against the mock factory.

# 2. Understanding Behavior (from the unit test):
#    - The unit test uses MockFactory to simulate the GPIO pin.
#    - It creates a LaserTripwire instance.
#    - `ltw._fire_deactivated()` simulates the LDR being blocked (dark).
#    - When dark, the "INTRUDER" message is printed to stdout.
#    - The test uses sleep(2) which might suggest that there is a delay with the behavior.

# 3. Property-Based Tests using Hypothesis:
#    - We need to test that when "dark" is simulated via the mock factory, the correct "INTRUDER" message is printed.
#    - The ldr_pin doesn't really matter since we're using a mock. However, we still generate integer values for it.

@settings(max_examples=20) # Increase max_examples for robust testing
@given(ldr_pin=st.integers(min_value=0, max_value=27)) # GPIO pins usually have limits, but MockFactory handles any value
def test_laser_tripwire_prints_intruder_on_dark(ldr_pin):
    Device.pin_factory = MockFactory(pin_class=MockPWMPin) #important to mock the pin factory, necessary to use property based tests

    with LaserTripwire(ldr_pin) as ltw:
        with patch('sys.stdout', new_callable=StringIO) as f:
            # Simulate darkness by firing the _fire_deactivated() method.
            ltw._fire_deactivated() # simulate the trigger event directly.
            assert f.getvalue() == 'INTRUDER\n'