from gpiozero import Robot, LineSensor, Motor
from time import sleep

class LineFollowingRobot(Robot):
    def __init__(self, left, right, left_seonsor_pin=17, right_sensor_pin=27, speed=0.65):
        super().__init__(left, right)
        self.left_sensor = LineSensor(left_seonsor_pin)
        self.right_sensor = LineSensor(right_sensor_pin)
        self.speed = speed
        self.source = self.motor_speed()

    def motor_speed(self):
        left_mot = 0
        right_mot = 0
        while True:
            left_detect  = int(self.left_sensor.value)
            right_detect = int(self.right_sensor.value)
            # Stage 1
            if left_detect == 0 and right_detect == 0:
                left_mot = 1
                right_mot = 1
            # Stage 2
            if left_detect == 0 and right_detect == 1:
                left_mot = -1
            if left_detect == 1 and right_detect == 0:
                right_mot = -1
            # print(r, l)
            yield right_mot * self.speed, left_mot * self.speed

    def stop(self):
        self.robot.stop()
        self.left_sensor.close()
        self.right_sensor.close()
        super().stop()