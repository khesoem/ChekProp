from io import StringIO
from unittest.mock import patch

from gpiozero.pins.mock import MockFactory
from examples.gpiozero.apps.app_1.src.laser_tripwire import LaserTripwire
from time import sleep

from gpiozero import *

def test_prints_when_dark():
    # Create a MockFactory and use it as pin_factory on Device
    Device.pin_factory = MockFactory()

    with LaserTripwire(7) as ltw:
        with patch('sys.stdout', new_callable=StringIO) as f:
            sleep(2)
            ltw._fire_deactivated()
            assert f.getvalue() == "INTRUDER\n"