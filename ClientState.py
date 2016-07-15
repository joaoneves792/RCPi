from threading import Lock, Timer

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
            self.client.send_message(str(self.forward))

            self.timer = Timer(self.update_interval/1000, self.send_state)
            self.timer.start()

    def apply_forwards(self, ammount):
        with self.state_lock:
            self.forward = ammount

    def apply_backwards(self, ammount):
        with self.state_lock:
            self.backwards = ammount

    def apply_left(self, ammount):
        with self.state_lock:
            self.left = ammount
            self.right = 0

    def apply_right(self, ammount):
        with self.state_lock:
            self.right = ammount
            self.left = 0
