import socket
import argparse
from fcntl import ioctl
from struct import pack
from Car import Car
from ServerState import ServerState
from protocol import FLAGS, StatePacket


LO = "lo"
PORT = 5005
MAX_PORT = 65535
TIMEOUT = 2000


def init_socket(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    return sock


def update_state(data, state):
    # TODO: Parse the data and update the state
    state_list = StatePacket.unpack_state(data)
    if state_list[0] != FLAGS.STATUS_UPDATE:
        return
    print("Forward:" + str(state_list[StatePacket.FORWARD]))


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(ioctl(s.fileno(), 0x8915, pack('256s', ifname[:15]))[20:24])


def await_connection(sock):
    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print("received message:", data)
        if data == FLAGS.get_hello():
            sock.sendto(data, addr)
            return addr


def main():
    parser = argparse.ArgumentParser(prog='RCPi Server', description="RCPi server (this should be executed on the RPi")
    parser.add_argument("-p", "--port", action="store", type=int, default=PORT, choices=range(1025, MAX_PORT), help='UDP Port to listen on')
    parser.add_argument("-t", "--timeout", action="store", type=int, default=TIMEOUT, help='Time in milliseconds to enter recovery after last status update')
    parser.add_argument("-i", "--interface", action="store", type=str, default=LO, help='Network interface to bind the socket to')

    args = parser.parse_args()

    print("Using interface: " + args.interface)
    ip = get_ip_address(bytes(args.interface, 'utf8'))
    print("Listening on " + ip + ":" + str(args.port))

    sock = init_socket(ip, args.port)

    car = Car()
    state = ServerState()

    client_addr = await_connection(sock)
    timeout = args.timeout/1000
    sock.settimeout(timeout)

    while True:
        try:
            data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
            sock.sendto(FLAGS.get_ack(), addr)
            print("received message:", data)
            update_state(data, state)
            car.apply_state(state)
        except socket.timeout:
            print("Lost connection to client")
            car.stop()  # Connection has failed enter recovery
            sock.settimeout(None)
            client_addr = await_connection(sock)
            sock.settimeout(timeout)


if __name__ == "__main__":
    main()
