from unittest.mock import patch
from io import StringIO

from gpiozero.pins.mock import MockFactory, MockPWMPin
from gpiozero import *

from examples.gpiozero.apps.app_5.src.quick_reaction_game import QuickReactionGame


def test_pressed_ineffective_before_led():
    # Create a MockFactory and use it as pin_factory on Device
    Device.pin_factory = MockFactory(pin_class=MockPWMPin)

    with QuickReactionGame(left_name="Bob", right_name="Alice") as qrg:
        with patch('sys.stdout', new_callable=StringIO) as f:
            qrg.left_button.pin.drive_low()
            assert f.getvalue() == ""