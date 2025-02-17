from gpiozero.pins.mock import MockFactory, MockPWMPin
from examples.gpiozero.apps.app_6.src.presence_indicator import PresenceIndicator
from unittest.mock import patch
from time import sleep

from gpiozero import *

def test_leds_value():
    # Create a MockFactory and use it as pin_factory on Device
    Device.pin_factory = MockFactory(pin_class=MockPWMPin)

    with patch('examples.gpiozero.apps.app_6.src.presence_indicator.requests') as MockRequests:
        MockRequests.get.return_value.json.return_value = {'number': 5}
        with PresenceIndicator([21, 20, 16, 12, 8, 25, 24, 23, 18, 14]) as pi:
            sleep(1)
            assert pi.leds.value == 0.5