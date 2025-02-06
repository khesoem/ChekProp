from gpiozero import LightSensor

"""
A simple prototype on a breadboard to detect whether or not a beam of light is hitting the light-dependent resistor (LDR)
"""

class LaserTripwire(LightSensor):
    def __init__(self, ldr_pin):
        super().__init__(ldr_pin)
        self.when_dark = lambda: print("INTRUDER")