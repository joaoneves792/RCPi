import socket
import argparse

IP = "127.0.0.1"
PORT = 5005
MAX_PORT = 65535
TIMEOUT = 2000


def init_socket(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    return sock


def main():
    parser = argparse.ArgumentParser(prog='RCPi Server', description="RCPi server (this should be executed on the RPi")
    parser.add_argument("-p", "--port", action="store", type=int, default=PORT, choices=range(1025, MAX_PORT), help='UDP Port to listen for commands')
    parser.add_argument("-t", "--timeout", action="store", type=int, default=TIMEOUT, help='Timeout in milliseconds between received commands')

    args = parser.parse_args()

    sock = init_socket(IP, args.port)

    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print("received message:", data)
        sock.sendto(data, addr)


if __name__ == "__main__":
    main()