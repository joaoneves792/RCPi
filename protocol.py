from struct import pack


class FLAGS:
    HELLO = 1
    ACK = 2
    STATUS_UPDATE = 3

    @staticmethod
    def get_hello():
        return pack("!B", FLAGS.HELLO)

    @staticmethod
    def get_ack():
        return pack("!B", FLAGS.ACK)
