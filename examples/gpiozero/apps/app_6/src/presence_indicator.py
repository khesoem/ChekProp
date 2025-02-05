from gpiozero import LEDBarGraph
from time import sleep

class PresenceIndicator:
	def __init__(self, pins=None, data_provider=None, delay=60):
		self.leds = LEDBarGraph(21, 20, 16, 12, 8, 25, 24, 23, 18, 14)
		self.leds.off()
		self.data_provider = data_provider
		self.delay = delay

	def play(self):
		while True:
			r = self.data_provider.get()
			data = r.json()
			people = data['number']
			print(people)
			self.leds.off()
			self.leds.value = people / 10
			sleep(self.delay)