from gpiozero.pins.mock import MockFactory, MockPWMPin
from examples.gpiozero.apps.app_3.src.ultrasonic_theremin import UltrasonicTheremin

from gpiozero import *

def test_quietness_before_play():
    # Create a MockFactory and use it as pin_factory on Device
    Device.pin_factory = MockFactory(pin_class=MockPWMPin)

    with UltrasonicTheremin(27, 17, 21) as ut:
        assert not ut.buzzer.is_active