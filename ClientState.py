from threading import Lock, Timer
from protocol import StatePacket


class ClientState:
    def __init__(self, client, time_interval):
        self.client = client

        self.forward = 0
        self.backwards = 0
        self.left = 0
        self.right = 0

        self.state_lock = Lock()

        self.update_interval = time_interval
        self.timer = Timer(self.update_interval/1000, self.send_state)
        self.timer.start()

    def send_state(self):
        # TODO: Send entire state in a packet
        with self.state_lock:
            state_list = [0]*(2+1)  # the extra 1 stands for the status flag that gets filled when packing the list
            state_list[StatePacket.FORWARD] = self.forward
            state_list[StatePacket.LEFT] = self.left

            data = StatePacket.pack_state(state_list)
            self.client.send_message(data)

        self.timer = Timer(self.update_interval/1000, self.send_state)
        self.timer.start()

    def apply_forwards(self, amount):
        with self.state_lock:
            self.forward = amount

    def apply_backwards(self, amount):
        with self.state_lock:
            self.backwards = amount

    def apply_left(self, amount):
        with self.state_lock:
            self.left = amount
            self.right = 0

    def apply_right(self, amount):
        with self.state_lock:
            self.right = amount
            self.left = 0
