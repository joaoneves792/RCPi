from threading import Lock
import socket
import os
import pygame
from XboxController import XboxController
from FF import FF
from ClientState import ClientState
from protocol import FLAGS


class KeyboardKeys:
    KEY_ESC = pygame.K_ESCAPE
    KEY_LEFT = (pygame.K_a, pygame.K_LEFT)
    KEY_RIGHT = (pygame.K_d, pygame.K_RIGHT)
    KEY_UP = (pygame.K_w, pygame.K_UP)
    KEY_DOWN = (pygame.K_s, pygame.K_DOWN)

    KEY_Y = pygame.K_y

    KEY_ONE = (pygame.K_1, pygame.K_KP1)
    KEY_FIVE = (pygame.K_5, pygame.K_KP5)
    KEY_TO_NUM = (KEY_ONE[0] - 1, KEY_ONE[1] - 1)


class Client:
    def __init__(self, server_ip, server_port, time_interval, xbox):
        self.xbox_controller_enabled = xbox
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_addr = (self.server_ip, self.server_port)
        self.time_interval = time_interval

        self.input_lock = Lock()
        self.xboxCont = None
        self.FF = None

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(2)

        if self.xbox_controller_enabled:
            self.FF = FF()

        self.init_pygame()

        self.state = None  # we create the state after the connection has been established

    def send_message(self, data):
        fail_count = 0
        while True:
            if fail_count > 3:
                self.establish_connection()
                return
            self.socket.sendto(data, self.server_addr)
            try:
                response, addr = self.socket.recvfrom(1024)
                print(response)
                if response == FLAGS.get_ack():
                    break
            except socket.timeout:
                fail_count += 1
                continue

    def handle_xbox_controller(self, control_id, value):
        with self.input_lock:
            if control_id == XboxController.XboxControls.RTRIGGER:
                self.state.apply_forwards(value/100)
                self.state.apply_backwards(0)
                if self.xbox_controller_enabled:
                    if value > 10:
                        self.FF.play_throttle()
                    else:
                        self.FF.stop_throttle()
            if control_id == XboxController.XboxControls.LTRIGGER:
                self.state.apply_backwards(value/100)
                self.state.apply_forwards(0)
                if self.xbox_controller_enabled:
                    if value > 10:
                        self.FF.play_brakes()
                    else:
                        self.FF.stop_brakes()
            if control_id == XboxController.XboxControls.LTHUMBX:
                if value > 0:
                    self.state.apply_right(value/100)
                    self.state.apply_left(0)
                else:
                    self.state.apply_left(-(value/100))
                    self.state.apply_right(0)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            self.on_key_press(event.key)
        elif event.type == pygame.KEYUP:
            self.on_key_release(event.key)
        elif event.type == pygame.QUIT:
            if self.xbox_controller_enabled:
                self.FF.shutdown()
            pygame.quit()
            quit()

    def on_key_press(self, key):
        if key == KeyboardKeys.KEY_ESC:
            pygame.quit()
            quit()

        if key == KeyboardKeys.KEY_LEFT[1]:
            self.state.apply_left(1)
            self.state.apply_right(0)
        elif key == KeyboardKeys.KEY_RIGHT[1]:
            self.state.apply_left(0)
            self.state.apply_right(1)
        elif key == KeyboardKeys.KEY_UP[1]:
            self.state.apply_forwards(1)
            self.state.apply_backwards(0)
        elif key == KeyboardKeys.KEY_DOWN[1]:
            self.state.apply_forwards(0)
            self.state.apply_backwards(1)

    def on_key_release(self, key):

        if key == KeyboardKeys.KEY_LEFT[1]:
            self.state.apply_left(0)
        elif key == KeyboardKeys.KEY_RIGHT[1]:
            self.state.apply_right(0)
        elif key == KeyboardKeys.KEY_UP[1]:
            self.state.apply_forwards(0)
        elif key == KeyboardKeys.KEY_DOWN[1]:
            self.state.apply_backwards(0)

    def init_pygame(self):

        if self.xbox_controller_enabled:
            os.environ["SDL_VIDEODRIVER"] = "dummy"
            pygame.init()
            # create a 1x1 pixel screen, its not used so it doesnt matter
            screen = pygame.display.set_mode((1, 1))
            pygame.joystick.init()
            # get the first joystick
            joy = pygame.joystick.Joystick(0)
            # init that joystick
            joy.init()
        else:
            pygame.init()
            pygame.display.init()
            screen = pygame.display.set_mode((100, 100))
            pygame.display.set_caption("RCPi")

        if self.xbox_controller_enabled:
            self.xboxCont = XboxController(self.handle_xbox_controller, deadzone=30, scale=100, invertYAxis=True, pygameEventCallBack=self.handle_events)
            self.xboxCont.start()
            self.FF = FF()

    def loop(self):
        if self.xbox_controller_enabled:
            self.FF.play_idle()

        self.establish_connection()

        print("Connection successful!")
        self.state = ClientState(self, self.time_interval)

        while True:     # if we are using the xbox controller than this loop is running there in a thread of its own,
                        # in any case we want the execution of the program to be stuck in this method
            pygame.display.update()
            if not self.xbox_controller_enabled:
                for event in pygame.event.get():
                    self.handle_events(event)

    def establish_connection(self):
        while True:
            try:
                print("Trying to establish connection to server...")
                self.socket.sendto(FLAGS.get_hello(), self.server_addr)
                response, addr = self.socket.recvfrom(1024)
                if response == FLAGS.get_hello():
                    break
            except socket.timeout:
                continue
