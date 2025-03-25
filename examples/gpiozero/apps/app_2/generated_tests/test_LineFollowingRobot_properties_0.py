from gpiozero.pins.mock import MockFactory, MockPWMPin
from examples.gpiozero.apps.app_2.src.line_following_robot import LineFollowingRobot
import time
from gpiozero import *
from hypothesis import given, strategies as st
from hypothesis import settings

# 1. Extract Properties:
#    * The robot responds to the LineSensor values (0 or 1) to control motor direction and speed.
#    * left_sensor = 0 and right_sensor = 0: both motors move forward.
#    * left_sensor = 0 and right_sensor = 1: left motor reverses.
#    * left_sensor = 1 and right_sensor = 0: right motor reverses.
#    * speed: is a float for motor speed, affecting the magnitude of the motor value.
#    * Stop method should clear resourses.

# 2. Understand behavior:
#    * The robot uses two LineSensor objects and two Motor objects.
#    * The motor_speed generator yields motor speed tuples.
#    * The speed determined by the motor value * self.speed
#    * Initial state causes forward movement
#    * The robots relies on real time delays.

# 3. Property-Based Tests 

@given(
    left_sensor_value=st.integers(min_value=0, max_value=1),
    right_sensor_value=st.integers(min_value=0, max_value=1),
    speed=st.floats(min_value=0.1, max_value=1.0)
)
@settings(deadline=10000, max_examples=20)
def test_motor_control_based_on_sensor_values(left_sensor_value, right_sensor_value, speed):
    print(f"left_sensor_value: {left_sensor_value}, right_sensor_value: {right_sensor_value}, speed: {speed}")
    Device.pin_factory = MockFactory()
    with LineFollowingRobot(Motor(2, 3, enable=4, pwm=False), Motor(5, 6, enable=7, pwm=False), left_seonsor_pin=8, right_sensor_pin=9, speed=speed) as lfr:
        if left_sensor_value > 0:
            lfr.left_sensor.pin.drive_high()
        if right_sensor_value > 0:
            lfr.right_sensor.pin.drive_high()
        time.sleep(0.1) # Simulate slight delay to trigger motor_speed updates

        print(f'lfr.left_motor.value: {lfr.left_motor.value}, lfr.right_motor.value: {lfr.right_motor.value}')
        if left_sensor_value == 0 and right_sensor_value == 0:
            assert lfr.right_motor.value == speed
            assert lfr.left_motor.value == speed
        elif left_sensor_value == 0 and right_sensor_value == 1:
            assert lfr.left_motor.value == -speed
        elif left_sensor_value == 1 and right_sensor_value == 0:
            assert lfr.right_motor.value == -speed
        else:
            assert lfr.left_motor.value != 0 or lfr.right_motor.value != 0

        lfr.stop()

# @settings(max_examples=10)
# def test_stop_method_clears_resources():
#     Device.pin_factory = MockFactory(pin_class=MockPWMPin)
#     with LineFollowingRobot(Motor(2, 3, enable=4, pwm=False), Motor(5, 6, enable=7, pwm=False), left_seonsor_pin=8, right_sensor_pin=9, speed=0.5) as lfr:
#         lfr.stop()
#         assert lfr.left_sensor.closed
#         assert lfr.right_sensor.closed