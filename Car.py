from ServerState import ServerState

# TODO: Implement these functions so that the motors get activated/deactivated when we call them


class Car:
    def __init__(self):
        self.state = 0

    def move_forwards(self, throttle):
        print("moving forward")

    def move_backwards(self, brakes):
        print("moving backwards")

    def stop(self):
        print("stopping")

    def turn_left(self):
        print("turning left")

    def turn_right(self):
        print("turning right")

    def center_steering(self):
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


