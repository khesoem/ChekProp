from threading import Thread

from gpiozero import LEDBarGraph
from time import sleep
import requests

class PresenceIndicator:
	def __init__(self, pins=None, url="", delay=1):
		self.leds = LEDBarGraph(21, 20, 16, 12, 8, 25, 24, 23, 18, 14)
		self.leds.off()
		self.url = url
		self.delay = delay
		self.playing = False

	def play(self):
		self.playing = True
		while True:
			if not self.playing:
				break
			r = requests.get(self.url)
			data = r.json()
			people = data['number']
			print(people)
			self.leds.off()
			self.leds.value = people / 10
			sleep(self.delay)

	def stop_playing(self):
		self.playing = False

	def __enter__(self):
		self.thread = Thread(target=self.play)
		self.thread.start()
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.stop_playing()
		self.leds.close()