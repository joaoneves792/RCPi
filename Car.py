from ServerState import ServerState


class Car:
    def __init__(self):
        self.FORWARD = 1
        self.BACKWARDS = -1
        self.STOPPED = 0
        self.CENTERED = 0
        self.RIGHT = 1
        self.LEFT= -1

        self.steering = self.CENTERED
        self.power = self.STOPPED

    def move_forwards(self, throttle):
        if  self.power != self.FORWARD:
            self.power = self.FORWARD
            print("moving forward")

    def move_backwards(self, brakes):
        if self.power != self.BACKWARDS:
            self.power = self.BACKWARDS
            print("moving backwards")

    def stop(self):
        if self.power != self.STOPPED:
            self.power = self.STOPPED
            print("stopping")

    def turn_left(self):
        if self.steering != self.LEFT:
            self.steering = self.LEFT
            print("turning left")

    def turn_right(self):
        if self.steering != self.RIGHT:
            self.steering = self.RIGHT
            print("turning right")

    def center_steering(self):
        if self.steering != self.CENTERED:
            self.steering = self.CENTERED
        print("centering steering")

    def apply_state(self, st):
        # Hack for pycharm to show proper auto-completion
        state = st  # type: ServerState

        if state.get_forward() > 0.5:
            self.move_forwards(state.get_forward())
        if state.get_backward() > 0.5:
            self.move_backwards(state.get_backward())
        if state.get_left() > 0.5:
            self.turn_left()
        if state.get_right() > 0.5:
            self.turn_right()
        if state.get_left() <= 0.5 and state.get_right() <= 0.5:
            self.center_steering()
        if state.get_forward() <= 0.5 and state.get_backward() <= 0.5:
            self.stop()


