from gpiozero import Robot, Button

class RemoteBuggy(Robot):
    def __init__(self, left_motor, right_motor, left_btn_pin, right_btn_pin, forward_btn_pin, backward_btn_pin):
        super().__init__(left_motor, right_motor)
        self.left_btn = Button(left_btn_pin)
        self.left_btn.when_pressed = self.left
        self.right_btn = Button(right_btn_pin)
        self.right_btn.when_pressed = self.right
        self.forward_btn = Button(forward_btn_pin)
        self.forward_btn.when_pressed = self.forward
        self.backward_btn = Button(backward_btn_pin)
        self.backward_btn.when_pressed = self.backward

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.left_btn.close()
        self.right_btn.close()
        self.forward_btn.close()
        self.backward_btn.close()
        self.stop()
        self.close()