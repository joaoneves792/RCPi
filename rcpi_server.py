import socket
import argparse
from threading import Timer
from Car import Car
from ServerState import ServerState


IP = "127.0.0.1"
PORT = 5005
MAX_PORT = 65535
TIMEOUT = 2000
IM_ALIVE_INTERVAL = 500

imalive = None

def init_socket(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    return sock


def unpack_state(data, state):
    # TODO: Parse the data and update the state
    pass


def main():
    parser = argparse.ArgumentParser(prog='RCPi Server', description="RCPi server (this should be executed on the RPi")
    parser.add_argument("-p", "--port", action="store", type=int, default=PORT, choices=range(1025, MAX_PORT), help='UDP Port to listen for commands')
    parser.add_argument("-t", "--time", action="store", type=int, default=IM_ALIVE_INTERVAL, help='Time in milliseconds between sending im alive messages')

    args = parser.parse_args()

    sock = init_socket(IP, args.port)

    car = Car()
    state = ServerState()

    client_addr = await_connection(sock)
    sock.settimeout(TIMEOUT)
    imalive = Timer(args.time/1000, send_im_alive(sock, client_addr))
    imalive.start()

    while True:
        try:
            data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
            print("received message:", data)
            unpack_state(data, state)
            car.apply_state(state)
        except socket.timeout:
            imalive.cancel()
            sock.settimeout(0)
            client_addr = await_connection(sock)
            sock.settimeout(TIMEOUT)
            imalive = Timer(args.time/1000, send_im_alive(sock, client_addr))
            imalive.start()


def send_im_alive(sock, addr):
    sock.sendto("IMALIVE".encode(), addr)
    imalive = Timer(args.time/1000, send_im_alive(sock, client_addr))
    imalive.start()


def await_connection(sock):
    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print("received message:", data)
        if data.decode() == "HELLO":
            sock.sendto(data, addr)
            return addr


if __name__ == "__main__":
    main()
