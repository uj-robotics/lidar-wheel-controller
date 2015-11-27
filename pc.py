__author__ = 'Rafał'
import socket
import time
import json

""" prosty nadajnik na szybko """

ip = "192.168.0.127"
port = 5678

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((ip, port))


def send_message(message):
    msg_json = json.dumps(message).encode()
    header = "!" + str(len(msg_json)) + "!"
    msg = b''.join([header.encode(), msg_json])
    s.send(msg)

send_message({'left_motor': 255, 'right_motor': 255})
time.sleep(3)
send_message({'left_motor': -255, 'right_motor': -255})
time.sleep(3)
send_message({'left_motor': 0, 'right_motor': 0})

s.close()