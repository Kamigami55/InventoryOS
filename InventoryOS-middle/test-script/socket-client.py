# socket-client.py

import socket
HOST = 'inventory-os-camera.local'
PORT = 8001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

try:
    while True:
        cmd = raw_input("Please input msg:")
        s.send(cmd)
        data = s.recv(1024)
        print data

except KeyboardInterrupt:
    s.close()
