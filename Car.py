from ServerState import ServerState
import RPi.GPIO as GPIO

class Car:
    def __init__(self):
        self.FORWARD = 1
        self.BACKWARDS = -1
        self.STOPPED = 0
        self.CENTERED = 0
        self.RIGHT = 1
        self.LEFT= -1

        self.STEER_RIGHT = 16  # Right
        self.STEER_LEFT = 18  # Left
        self.STEERING_ENABLE = 22

        self.POWER_FORWARD = 19  # Forwards
        self.POWER_BACKWARD = 21  # Backwards
        self.POWER_ENABLE = 23

        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(self.STEER_RIGHT, GPIO.OUT)
        GPIO.setup(self.STEER_LEFT, GPIO.OUT)
        GPIO.setup(self.STEERING_ENABLE, GPIO.OUT)

        GPIO.setup(self.POWER_FORWARD, GPIO.OUT)
        GPIO.setup(self.POWER_BACKWARD, GPIO.OUT)
        GPIO.setup(self.POWER_ENABLE, GPIO.OUT)

        self.steering = self.CENTERED
        self.power = self.STOPPED

    def move_forwards(self, throttle):
        if  self.power != self.FORWARD:
            self.power = self.FORWARD
            print("moving forward")
            GPIO.output(self.POWER_FORWARD, GPIO.HIGH)
            GPIO.output(self.POWER_BACKWARD, GPIO.LOW)
            GPIO.output(self.POWER_ENABLE, GPIO.HIGH)

    def move_backwards(self, brakes):
        if self.power != self.BACKWARDS:
            self.power = self.BACKWARDS
            print("moving backwards")
            GPIO.output(self.POWER_FORWARD, GPIO.LOW)
            GPIO.output(self.POWER_BACKWARD, GPIO.HIGH)
            GPIO.output(self.POWER_ENABLE, GPIO.HIGH)

    def stop(self):
        if self.power != self.STOPPED:
            self.power = self.STOPPED
            print("stopping")
            GPIO.output(self.POWER_FORWARD, GPIO.LOW)
            GPIO.output(self.POWER_BACKWARD, GPIO.LOW)
            GPIO.output(self.POWER_ENABLE, GPIO.LOW)

    def turn_left(self):
        if self.steering != self.LEFT:
            self.steering = self.LEFT
            print("turning left")
            GPIO.output(self.STEER_RIGHT,GPIO.LOW)
            GPIO.output(self.STEER_LEFT,GPIO.HIGH)
            GPIO.output(self.STEERING_ENABLE,GPIO.HIGH)

    def turn_right(self):
        if self.steering != self.RIGHT:
            self.steering = self.RIGHT
            print("turning right")
            GPIO.output(self.STEER_RIGHT,GPIO.HIGH)
            GPIO.output(self.STEER_LEFT,GPIO.LOW)
            GPIO.output(self.STEERING_ENABLE,GPIO.HIGH)

    def center_steering(self):
        if self.steering != self.CENTERED:
            self.steering = self.CENTERED
            print("centering steering")
            GPIO.output(self.STEER_RIGHT,GPIO.LOW)
            GPIO.output(self.STEER_LEFT,GPIO.LOW)
            GPIO.output(self.STEERING_ENABLE,GPIO.LOW)

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


