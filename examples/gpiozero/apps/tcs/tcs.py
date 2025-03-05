import threading
from time import sleep
import random
import math

class Environment:
    def __init__(self, initial_temp: int = None):
        self.temp = initial_temp if initial_temp is not None else random.randint(20, 24)

    def fetch_temp(self):
        return self.temp

    def set_temp(self, temp):
        self.temp = temp

    def get_outside_air_temp(self):
        return random.randint(-1, 1)

class TempSensor:
    def __init__(self, env: Environment):
        self.env = env
        self.temp = self.env.fetch_temp()

    def start_temp_collection(self, total_time: float, sensor_interval: float):
        for i in range(math.floor(total_time / sensor_interval)):
            self.temp = self.env.fetch_temp()
            sleep(sensor_interval)

class PWMOutputDevice:
    def __init__(self):
        self.value = 0

    def on(self):
        self.value = 1

    def off(self):
        self.value = 0

class HCUnit:
    def __init__(self):
        self.cooler = PWMOutputDevice()
        self.heater = PWMOutputDevice()

    def activate_cooler(self):
        self.cooler.on()
        self.heater.off()

    def activate_heater(self):
        self.cooler.off()
        self.heater.on()

    def deactivate(self):
        self.cooler.off()
        self.heater.off()

class Controller:
    def __init__(self, temp_sensor: TempSensor, hc_unit: HCUnit):
        self.temp_sensor = temp_sensor
        self.hc_unit = hc_unit

    def control(self, total_time: float, control_interval: float):
        for i in range(math.floor(total_time / control_interval)):
            temperature = self.temp_sensor.temp
            if 21 <= temperature <= 23:
                self.hc_unit.deactivate()
            elif temperature > 23:
                self.hc_unit.activate_cooler()
            else:
                self.hc_unit.activate_heater()
            sleep(control_interval)

class SystemState:
    def __init__(self, temp: float, cooler_state: int, heater_state: int, outside_air_temp: int):
        self.temp = temp
        self.cooler_state = cooler_state
        self.heater_state = heater_state
        self.outside_air_temp = outside_air_temp

    def __str__(self):
        return f"Temp: {self.temp}, Cooler: {self.cooler_state}, Heater: {self.heater_state}, Outside Air Temp: {self.outside_air_temp}"


class MockRoom:
    def __init__(self, total_time: float, sensor_interval: float, control_interval: float, initial_temp: int = None):
        self.env = Environment(initial_temp=initial_temp)
        self.total_time = total_time
        self.sensor_interval = sensor_interval
        self.control_interval = control_interval
        self.temp_sensor = TempSensor(self.env)
        self.hc_unit = HCUnit()
        self.controller = Controller(self.temp_sensor, self.hc_unit)

    def execute_scenario(self):

        sensor_thread = threading.Thread(target=self.temp_sensor.start_temp_collection,
                                         args=(self.total_time, self.sensor_interval))
        control_thread = threading.Thread(target=self.controller.control,
                                          args=(self.total_time, self.control_interval))

        sensor_thread.start()
        control_thread.start()

        collected_states = []
        for i in range(self.total_time):
            cur_temp = self.env.fetch_temp()
            outside_air_temp = self.env.get_outside_air_temp()
            cooler_value = self.hc_unit.cooler.value
            heater_value = self.hc_unit.heater.value
            collected_states.append(SystemState(cur_temp, cooler_value, heater_value, outside_air_temp))
            self.env.set_temp(cur_temp + outside_air_temp + heater_value - cooler_value)
            sleep(1)

        sensor_thread.join()
        control_thread.join()

        return collected_states

if __name__ == '__main__':
    for s in MockRoom(10, 0.1, 0.3).execute_scenario():
        print(s)