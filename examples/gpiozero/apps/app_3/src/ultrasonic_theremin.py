from gpiozero import DistanceSensor, TonalBuzzer, PWMOutputDevice
from gpiozero.tones import Tone
from time import sleep

class UltrasonicTheremin:
    def __init__(self, trigger, echo, buzzer, octaves=3):
        self.uds = DistanceSensor(trigger=trigger, echo=echo)
        self.buzzer = TonalBuzzer(buzzer, octaves=octaves)

    def distance_to_tone(self, distance_value):
        min_tone = self.buzzer.min_tone.midi
        max_tone = self.buzzer.max_tone.midi
        tone_range = max_tone - min_tone
        return min_tone + int(tone_range * distance_value)

    def play(self):
        while True:
            distance_value = self.uds.distance
            tone = self.distance_to_tone(distance_value)
            self.buzzer.play(Tone(midi=tone))
            sleep(0.01)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.buzzer.close()
        self.uds.close()