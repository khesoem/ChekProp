from gpiozero import LightSensor

class LaserTripwire(LightSensor):
    """
    A simple prototype on a breadboard to detect whether a beam of light is hitting the light-dependent resistor (LDR)
    """
    def __init__(self, ldr_pin):
        super().__init__(ldr_pin)
        self.when_dark = lambda: print("INTRUDER")