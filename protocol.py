from struct import pack, unpack


# TODO: Complete the StatePacket class

class StatePacket:
    # Constants that map indexes in the state_list to their meaning
    FORWARD = 1
    LEFT = 2
    BACKWARD = 3

    FMT_STR = "!B2f"

    @staticmethod
    def pack_state(state_list):
        return pack(StatePacket.FMT_STR, FLAGS.STATUS_UPDATE, state_list[StatePacket.FORWARD], state_list[StatePacket.LEFT])

    @staticmethod
    def unpack_state(data):
        return unpack(StatePacket.FMT_STR, data)


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


