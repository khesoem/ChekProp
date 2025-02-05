from gpiozero import LED, Button
from time import sleep
from random import uniform

class QuickReactionGame:
    def __init__(self, left_name, right_name, left_button_pin=14, right_button_pin=15, led_pin=4):
        self.led = LED(led_pin)
        self.right_button = Button(right_button_pin)
        self.left_button = Button(left_button_pin)
        self.left_name = left_name
        self.right_name = right_name
        self.make_player_buttons_invalid()

    def valid_pressed(self, button):
        if button == self.left_button:
            print(f"Winner: {self.left_name}")
        else:
            print(f"Winner: {self.right_name}")
        self.make_player_buttons_invalid()

    def invalid_pressed(self, button):
        pass

    def wait_for_players(self):
        self.right_button.when_pressed = self.valid_pressed
        self.left_button.when_pressed = self.valid_pressed

    def make_player_buttons_invalid(self):
        self.right_button.when_pressed = self.invalid_pressed
        self.left_button.when_pressed = self.invalid_pressed

    def start_round(self):
        self.make_player_buttons_invalid()
        self.led.on()
        sleep(uniform(5, 10))
        self.led.off()
        self.wait_for_players()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.led.close()
        self.right_button.close()
        self.left_button.close()
