from . import escape_room_socket
import argparse

parser = argparse.ArgumentParser(prog="escape-room", description='escape room bot in slack')
parser.add_argument('-http', '--http', action='store_true')
parser.add_argument('-p', '--port')

args = parser.parse_args()

def main():
    if args.http:
        escape_room_socket.begin(args.http, args.port)
    else:
        escape_room_socket.begin()