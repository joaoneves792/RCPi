import argparse
from Client import Client

PORT = 5005
MAX_PORT = 65535
TIMEOUT = 2000


def main():
    parser = argparse.ArgumentParser(prog='RCPi Client', description="RCPi client (this should be executed on the PC with the human interface")
    parser.add_argument("-a", "--ip", action="store", type=str, help="IP adress of the RPi where the server is running")
    parser.add_argument("-p", "--port", action="store", type=int, default=PORT, choices=range(1025, MAX_PORT), help='UDP Port to send the commands')
    parser.add_argument("-t", "--timeout", action="store", type=int, default=TIMEOUT, help='Timeout in milliseconds between receiving acknowledgments')
    parser.add_argument("-x", "--xbox", action="store_true", help='If present then try to use an XBOX 360 controller as input')

    args = parser.parse_args()

    client = Client(args.ip, args.port, args.xbox)
    client.loop()


if __name__ == "__main__":
    main()
