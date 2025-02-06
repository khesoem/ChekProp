from gpiozero.pins.mock import MockFactory, MockPWMPin
from examples.gpiozero.apps.app_4.src.remote_buggy import RemoteBuggy

from gpiozero import *

def test_forward_positive_speed():
    # Create a MockFactory and use it as pin_factory on Device
    Device.pin_factory = MockFactory(pin_class=MockPWMPin)

    with RemoteBuggy(Motor(7, 8, enable=11, pwm=False),
                     Motor(9, 10, enable=12, pwm=False),
                     4, 17, 13, 21) as rb:
        rb.forward()
        assert all(speed > 0 for speed in rb.value)