from ServerState import ServerState

# TODO: Implement these functions so that the motors get activated/deactivated when we call them


class Car:
    def __init__(self):
        self.state = 0

    def move_forwards(self, throttle):
        pass

    def move_backwards(self, brakes):
        pass

    def stop(self):
        pass

    def turn_left(self):
        pass

    def turn_right(self):
        pass

    def center_steering(self):
        pass

    def apply_state(self, st):
        # Hack for pycharm to show proper auto-completion
        state = st  # type: ServerState

        # Example
        if state.get_forward() > 0.5:
            self.move_forwards(state.get_forward())


