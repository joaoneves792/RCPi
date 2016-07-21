import socket
import argparse
from Car import Car
from ServerState import ServerState
from protocol import FLAGS


IP = "127.0.0.1"
PORT = 5005
MAX_PORT = 65535
TIMEOUT = 2000


def init_socket(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    return sock


def unpack_state(data, state):
    # TODO: Parse the data and update the state
    pass


def main():
    parser = argparse.ArgumentParser(prog='RCPi Server', description="RCPi server (this should be executed on the RPi")
    parser.add_argument("-p", "--port", action="store", type=int, default=PORT, choices=range(1025, MAX_PORT), help='UDP Port to listen on')
    parser.add_argument("-t", "--timeout", action="store", type=int, default=TIMEOUT, help='Time in milliseconds to enter recovery after last status update')

    args = parser.parse_args()

    sock = init_socket(IP, args.port)

    car = Car()
    state = ServerState()

    client_addr = await_connection(sock)
    sock.settimeout(TIMEOUT)

    while True:
        try:
            data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
            sock.sendto(FLAGS.get_ack(), addr)
            print("received message:", data)
            unpack_state(data, state)
            car.apply_state(state)
        except socket.timeout:
            car.stop()  # Connection has failed enter recovery
            sock.settimeout(0)
            client_addr = await_connection(sock)
            sock.settimeout(TIMEOUT)


def await_connection(sock):
    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print("received message:", data)
        if data == FLAGS.get_hello():
            sock.sendto(data, addr)
            return addr


if __name__ == "__main__":
    main()
