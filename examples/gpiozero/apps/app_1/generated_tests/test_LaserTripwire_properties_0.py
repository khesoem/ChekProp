from hypothesis import given
from hypothesis import strategies as st
from gpiozero.pins.mock import MockFactory
from gpiozero import Device, LightSensor
from examples.gpiozero.apps.app_1.src.laser_tripwire import LaserTripwire
from unittest.mock import patch
from io import StringIO
from time import sleep

@given(st.booleans())
def test_prints_intruder_when_dark(is_dark):
    """
    Property: When the light sensor is 'dark', the 'INTRUDER' message is printed.
    This test checks that the 'INTRUDER' message is printed when the sensor detects darkness.  The
    `LightSensor` in `LaserTripwire` triggers the `when_dark` callback, which prints the
    'INTRUDER' message.
    """
    # Create a MockFactory and use it as pin_factory on Device
    Device.pin_factory = MockFactory()
    with LaserTripwire(7) as ltw:
        with patch('sys.stdout', new_callable=StringIO) as f:
            # Set the sensor to dark if is_dark is True.
            if is_dark:
                ltw._fire_deactivated()  # simulate a dark state based on the unit tests

            sleep(0.1)  # Allow time for the print to happen

            if is_dark:
                assert "INTRUDER" in f.getvalue()
            else:
                assert "INTRUDER" not in f.getvalue() # ensure the event is not triggered when the input is not dark

@given(st.booleans())
def test_does_not_print_intruder_when_light(is_light):
    """
    Property: When the light sensor is 'light', the 'INTRUDER' message is not printed.
    """
    Device.pin_factory = MockFactory()
    with LaserTripwire(7) as ltw:
        with patch('sys.stdout', new_callable=StringIO) as f:

            # Set the sensor to light (default state, no activation)
            if is_light:
                pass # do nothing as the mock library initialized to light state

            sleep(0.1)

            if is_light:
                assert "INTRUDER" not in f.getvalue()
            else:
                assert "INTRUDER" in f.getvalue() # when in dark state it print