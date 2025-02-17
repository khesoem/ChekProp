from gpiozero.pins.mock import MockFactory, MockPWMPin
from examples.gpiozero.apps.app_4.src.remote_buggy import RemoteBuggy
from gpiozero import *
from hypothesis import given, strategies as st
from hypothesis.errors import InvalidArgument
import pytest


# 1. Extracting Properties:
# The properties of the RemoteBuggy class are related to its control of a robot
# through button inputs. The Robot class (parent) controls the motors and hence the speed.
#  - Motor control: The buggy can move forward, backward, turn left, and turn right.
#  - Button Mapping: Each button press triggers a corresponding movement.
#  - Speed:  The speed of the motors is controlled by the robot methods.
#

# 2. Understanding Behavior (based on the provided unit test and class structure):
#   - The `RemoteBuggy` class inherits from `Robot`.
#   - It takes motor and button pin configurations in its constructor.
#   -  Button presses call `forward`, `backward`, `left`, and `right` methods which change the motor speeds.
#   -  The `__enter__` and `__exit__` methods are defined for resource management (closing the buttons and motors).  The robot `stop` method will stop the motors.
#

# 3. Property-Based Tests using Hypothesis:
#   - We'll test the motor behavior based on button presses and motor speeds through hypotheses, covering different combinations of button presses

# Create a mock factory for pin testing
@pytest.fixture(autouse=True)
def mock_pin_factory():
    Device.pin_factory = MockFactory(pin_class=MockPWMPin)

@given(
    left_motor_forward=st.floats(min_value=0, max_value=1),
    left_motor_backward=st.floats(min_value=0, max_value=1),
    right_motor_forward=st.floats(min_value=0, max_value=1),
    right_motor_backward=st.floats(min_value=0, max_value=1),
)
def test_forward_button_press_sets_motor_speeds(left_motor_forward, left_motor_backward, right_motor_forward, right_motor_backward):
    """Test that pressing the forward button sets both motors to a positive speed simultaneously."""

    with RemoteBuggy(
        Motor(7, 8, enable=11, pwm=False),
        Motor(9, 10, enable=12, pwm=False),
        4, 17, 13, 21
    ) as rb:
        # Simulate button press
        rb.forward_btn.pin.drive_high()
        rb.forward_btn.pin.drive_low()  # Simulate release, effectively a press

        assert all((speed > 0 for speed in rb.value)) # verify that the motor.value attribute is changed by the button press


@given(
    left_motor_forward=st.floats(min_value=0, max_value=1),
    left_motor_backward=st.floats(min_value=0, max_value=1),
    right_motor_forward=st.floats(min_value=0, max_value=1),
    right_motor_backward=st.floats(min_value=0, max_value=1),
)
def test_backward_button_press_sets_motor_speeds(left_motor_forward, left_motor_backward, right_motor_forward, right_motor_backward):
    """Test that pressing the backward button sets both motors to a negative speed simultaneously."""

    with RemoteBuggy(
        Motor(7, 8, enable=11, pwm=False),
        Motor(9, 10, enable=12, pwm=False),
        4, 17, 13, 21
    ) as rb:
          # Simulate button press
        rb.backward_btn.pin.drive_high()
        rb.backward_btn.pin.drive_low()  # Simulate release, effectively a press
        assert all((speed < 0 for speed in rb.value))

@given(
    left_motor_forward=st.floats(min_value=0, max_value=1),
    left_motor_backward=st.floats(min_value=0, max_value=1),
    right_motor_forward=st.floats(min_value=0, max_value=1),
    right_motor_backward=st.floats(min_value=0, max_value=1),
)

def test_left_button_press_sets_motor_speeds(left_motor_forward, left_motor_backward, right_motor_forward, right_motor_backward):
    """Test that pressing the left button causes the left motor to go backward and right to forward."""

    with RemoteBuggy(
        Motor(7, 8, enable=11, pwm=False),
        Motor(9, 10, enable=12, pwm=False),
        4, 17, 13, 21
    ) as rb:

        # Simulate button press
        rb.left_btn.pin.drive_high()
        rb.left_btn.pin.drive_low() # Simulate release, effectively a press


        assert rb.value[0] < 0  # left motor is backward
        assert rb.value[1] > 0  # right motor is forward


@given(
    left_motor_forward=st.floats(min_value=0, max_value=1),
    left_motor_backward=st.floats(min_value=0, max_value=1),
    right_motor_forward=st.floats(min_value=0, max_value=1),
    right_motor_backward=st.floats(min_value=0, max_value=1),
)
def test_right_button_press_sets_motor_speeds(left_motor_forward, left_motor_backward, right_motor_forward, right_motor_backward):
    """Test that pressing the right button causes the left motor to go forward and right to backward."""

    with RemoteBuggy(
        Motor(7, 8, enable=11, pwm=False),
        Motor(9, 10, enable=12, pwm=False),
        4, 17, 13, 21
    ) as rb:
         # Simulate button press
        rb.right_btn.pin.drive_high()
        rb.right_btn.pin.drive_low() # Simulate release, effectively a press

        assert rb.value[0] > 0  # left motor is forward
        assert rb.value[1] < 0  # right motor is backward


def test_no_button_press_stops_motors():
    """Test that after initialization of the buggy, initial motor speed should be zero."""

    with RemoteBuggy(
        Motor(7, 8, enable=11, pwm=False),
        Motor(9, 10, enable=12, pwm=False),
        4, 17, 13, 21
    ) as rb:
        assert rb.value == (0, 0)