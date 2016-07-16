class ServerState:
    def __init__(self, f=0, b=0, l=0, r=0):
        self.forward = f
        self.backward = b
        self.left = l
        self.right = r

    def set_forward(self, amount):
        self.forward = amount

    def set_backward(self, amount):
        self.backward = amount

    def set_left(self, amount):
        self.left = amount

    def set_right(self, amount):
        self.right = amount

    def get_forward(self):
        return self.forward

    def get_backward(self):
        return self.backward

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

