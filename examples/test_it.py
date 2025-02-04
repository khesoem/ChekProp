import pytest
from gpiozero import InputDevice, GPIODeviceError, PinInvalidState
from hypothesis import given, strategies as st
from unittest import mock
from gpiozero.pins.mock import MockFactory, MockPWMPin
from examples.gpiozero.apps.app_2.src.line_following_robot import LineFollowingRobot

from gpiozero import *
from gpiozero.fonts import *

def test_itt():
    # Create a MockFactory
    assert True
    # Device.pin_factory = MockFactory()
    # pins = [Device.pin_factory.pin(n) for n in range(2, 10)]

    # lfr = LineFollowingRobot(Motor(2, 3, enable=4, pwm=False), Motor(5, 6, enable=7, pwm=False), left_seonsor_pin=8, right_sensor_pin=9, speed=0.65)

    # lfr.close()