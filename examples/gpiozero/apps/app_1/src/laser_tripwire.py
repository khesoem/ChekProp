from gpiozero.pins.mock import MockFactory
from gpiozero import Device

"""
A simple prototype on a breadboard to detect whether or not a beam of light is hitting the light-dependent resistor (LDR)
"""

# Import the LightSensor class from gpiozero
from gpiozero import LightSensor
def create_intruder_detector_laser_tripwire():
    Device.pin_factory = MockFactory()

    # Create an ‘ldr’ object for the GPIO pin to which you have connected the LDR
    ldr = LightSensor()
    # Use the when_dark method to trigger your print
    ldr.when_dark = lambda: print("INTRUDER")
    return ldr