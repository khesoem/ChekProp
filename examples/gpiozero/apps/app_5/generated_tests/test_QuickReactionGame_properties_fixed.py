from hypothesis import given, strategies as st
from hypothesis.errors import InvalidArgument
from unittest.mock import patch
from io import StringIO
from gpiozero.pins.mock import MockFactory, MockPWMPin
from gpiozero import Device
from examples.gpiozero.apps.app_5.src.quick_reaction_game import QuickReactionGame
import pytest

# 1. Extract Properties:
#    - left_name, right_name: Player names (strings).  These affect the output.
#    - left_button_pin, right_button_pin, led_pin: GPIO pins (integers).  These are instantiation parameters, but their values themselves don't *directly* impact observable behavior, only setup.
#    - led: An LED object. Turns on/off.
#    - left_button, right_button: Button objects. Trigger actions on press.
#    - Game state: Active/Inactive (related to when the buttons are 'listening'). Controlled by when_pressed callbacks.
#    - Output:  Prints winner to stdout.

# 2. Understand Behavior (from unit tests and code):
#    - Before start_round, button presses are ignored (invalid_pressed is called).
#    - start_round turns on the LED, waits, then turns off the LED and starts waiting for button presses.  The wait time is random, which prevents determinism in the tests.
#    - When a button *is* valid:
#        - The `valid_pressed` method is called.
#        - The winner's name is printed to stdout.
#        - Button presses should be set to invalid (as in before start_round).


# 3. Property-Based Tests:  These address key properties.

@pytest.fixture
def mock_qrg():
    Device.pin_factory = MockFactory(pin_class=MockPWMPin)  # Crucial for mocking
    return QuickReactionGame(left_name='Bob', right_name='Alice')

# def test_player_names_printed_on_win(mock_qrg):
#     with patch('sys.stdout', new_callable=StringIO) as f:
#         mock_qrg.valid_pressed(mock_qrg.left_button)
#         assert "Winner: Bob" in f.getvalue()
#     with patch('sys.stdout', new_callable=StringIO) as f:
#         mock_qrg.valid_pressed(mock_qrg.right_button)
#         assert "Winner: Alice" in f.getvalue()
#
# def test_buttons_invalid_before_start_round(mock_qrg):
#     with patch('sys.stdout', new_callable=StringIO) as f:
#         mock_qrg.left_button.pin.drive_low() #Simulate button press
#         assert f.getvalue() == ''

@pytest.mark.parametrize("button", ["left", "right"])
def test_buttons_invalid_after_valid_press(mock_qrg, button):
    with patch('sys.stdout', new_callable=StringIO) as f:
        if button == "left":
           mock_qrg.valid_pressed(mock_qrg.left_button)
        else:
           mock_qrg.valid_pressed(mock_qrg.right_button)
        assert "Winner:" in f.getvalue()
        f.seek(0)
        f.truncate(0) # Reset stdout
        if button == "left":
            mock_qrg.left_button.pin.drive_low()
        else:
            mock_qrg.right_button.pin.drive_low()
        assert f.getvalue() == "" # Ensure no output on subsequent invalid press

# def test_led_on_off_in_start_round(mock_qrg):
#   mock_qrg.start_round()
#   assert mock_qrg.led.is_lit  is False #LED is off after the round ends
#
# def test_start_round_sets_buttons_valid(mock_qrg): # Test to check start_round sets button's valid press functions
#     mock_qrg.start_round()
#     assert mock_qrg.left_button.when_pressed == mock_qrg.valid_pressed
#     assert mock_qrg.right_button.when_pressed == mock_qrg.valid_pressed