"""
This module contains the implementation of the PCS system.
The PCS system consists of two cylinders, each with a sensor attached to it.
One of the cylinders is vertical and the other is horizontal.
The vertical cylinder can move up and down, while the horizontal cylinder can move left and right.
Each cylinder should move between locations 0 and 2. Going beyond these locations will break the cylinder.
The system has two controllers, one for each cylinder.
Controller A is responsible for controlling the horizontal cylinder, while Controller B is responsible for controlling the vertical cylinder.
Location 0 is the starting location for both cylinders, which is top-left in the system.
When the vertical cylinder is at bottom, the horizontal cylinder should not move.
The movement should follow this pattern: vertical cylinder moves down, vertical cylinder moves up, horizontal cylinder moves right, vertical cylinder moves down, vertical cylinder moves up, horizontal cylinder moves left.
"""

sleep_factor = 0.1

import math
import threading
from time import sleep

class Sensor:
    def __init__(self, location: int):
        self.location = location

class Cylinder:
    def __init__(self, sensor: Sensor):
        self.motion = 0
        self.sensor = sensor
        self.just_stopped = False

    def trigger_motion(self):
        if self.is_at_start():
            self.motion = 1
        elif self.is_at_end():
            self.motion = -1

    def move(self):
        self.sensor.location = self.sensor.location + self.motion
        self.just_stopped = False

    def start_working(self, total_time: float, cylinder_interval: float):
        for i in range(math.floor(total_time / cylinder_interval)):
            if self.motion != 0:
                self.move()
                if self.is_on_border():
                    self.motion = 0 # Stop movement
                    self.just_stopped = True
            sleep(cylinder_interval * sleep_factor)

    def is_on_border(self):
        return self.is_at_end() or self.is_at_start()

    def is_at_end(self):
        return self.sensor.location == 2

    def is_at_start(self):
        return self.sensor.location == 0

class ControllerA:
    """
    Controller A is responsible for controlling the horizontal cylinder
    """
    def __init__(self, cylinder_a: Cylinder, cylinder_b: Cylinder):
        self.controlling_cylinder = cylinder_a
        self.other_cylinder = cylinder_b

    def start_working(self, total_time: float, control_interval: float):
        for i in range(math.floor(total_time / control_interval)):
            if self.other_cylinder.just_stopped and self.other_cylinder.is_at_start():
                self.controlling_cylinder.trigger_motion()
                self.other_cylinder.just_stopped = False
            sleep(control_interval * sleep_factor)

class ControllerB:
    """
    Controller B is responsible for controlling the vertical cylinder
    """
    def __init__(self, cylinder_a: Cylinder, cylinder_b: Cylinder):
        self.controlling_cylinder = cylinder_b
        self.other_cylinder = cylinder_a

    def start_working(self, total_time: float, control_interval: float):
        just_started = True
        for i in range(math.floor(total_time / control_interval)):
            if self.other_cylinder.just_stopped or self.controlling_cylinder.is_at_end() or just_started:
                self.controlling_cylinder.trigger_motion()
                self.other_cylinder.just_stopped = False
            just_started = False
            sleep(control_interval * sleep_factor)

class SystemState:
    def __init__(self, cylinder_a_loc: int, cylinder_a_motion: int, cylinder_b_location: int, cylinder_b_motion: int):
        self.cylinder_a_loc = cylinder_a_loc
        self.cylinder_a_motion = cylinder_a_motion
        self.cylinder_b_location = cylinder_b_location
        self.cylinder_b_motion = cylinder_b_motion

    def __str__(self):
        return f"Cylinder A: {self.cylinder_a_loc} ({self.cylinder_a_motion}), Cylinder B: {self.cylinder_b_location} ({self.cylinder_b_motion})"

class MockSystem:
    def __init__(self, total_time: float, cylinder_interval: float, controller_interval: float, mock_interval: float):
        self.cylinder_a = Cylinder(Sensor(0))
        self.cylinder_b = Cylinder(Sensor(0))
        self.controller_a = ControllerA(self.cylinder_a, self.cylinder_b)
        self.controller_b = ControllerB(self.cylinder_a, self.cylinder_b)
        self.total_time = total_time
        self.cylinder_interval = cylinder_interval
        self.controller_interval = controller_interval
        self.mock_interval = mock_interval

    def collect_state(self):
        return SystemState(self.cylinder_a.sensor.location, self.cylinder_a.motion,
                           self.cylinder_b.sensor.location, self.cylinder_b.motion)

    def execute_scenario(self):
        cylinder_a_thread = threading.Thread(target=self.cylinder_a.start_working,
                                         args=(self.total_time, self.cylinder_interval))
        control_a_thread = threading.Thread(target=self.controller_a.start_working,
                                          args=(self.total_time, self.controller_interval))
        cylinder_b_thread = threading.Thread(target=self.cylinder_b.start_working,
                                             args=(self.total_time, self.cylinder_interval))
        control_b_thread = threading.Thread(target=self.controller_b.start_working,
                                            args=(self.total_time, self.controller_interval))

        cylinder_a_thread.start()
        control_a_thread.start()
        cylinder_b_thread.start()
        control_b_thread.start()

        collected_states = []
        for i in range(math.ceil(self.total_time / self.mock_interval) + 1):
            collected_states.append(self.collect_state())
            sleep(self.mock_interval * sleep_factor)

        cylinder_a_thread.join()
        control_a_thread.join()
        cylinder_b_thread.join()
        control_b_thread.join()

        return collected_states

if __name__ == "__main__":
    for s in MockSystem(20, 1, 1, 0.5).execute_scenario():
        print(s)