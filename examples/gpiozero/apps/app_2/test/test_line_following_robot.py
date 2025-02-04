import pytest
from gpiozero import InputDevice, GPIODeviceError, PinInvalidState
from hypothesis import given, strategies as st
from unittest import mock
from gpiozero.pins.mock import MockFactory, MockPWMPin
from examples.gpiozero.apps.app_2.src.line_following_robot import LineFollowingRobot
import time

from gpiozero import *

def test_input_device_properties():
    # Create a MockFactory
    Device.pin_factory = MockFactory()

    with LineFollowingRobot(Motor(2, 3, enable=4, pwm=False),
                             Motor(5, 6, enable=7, pwm=False),
                             left_seonsor_pin=8, right_sensor_pin=9, speed=1) as lfr:

        time.sleep(1)
        lfr.left_sensor.pin.drive_high()
        time.sleep(1)
        assert lfr.right_motor.value == 1