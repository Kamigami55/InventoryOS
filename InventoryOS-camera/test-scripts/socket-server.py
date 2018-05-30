# socket-server.py

import socket, errno

HOST = 'inventory-os-camera.local'
PORT = 8001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

print 'Server start at: %s:%s' %(HOST, PORT)
print 'wait for connection...'

while True:
    conn, addr = s.accept()
    print 'Connected by ', addr

    while True:
        try:
            data = conn.recv(1024)
            print data
            conn.send("server received you message.")
        except socket.error, e:
            if isinstance(e.args, tuple):
                print "errno is %d" % e[0]
                if e[0] == errno.EPIPE:
                   # remote peer disconnected
                   print "Detected remote disconnect"
                else:
                   # determine and handle different error
                   pass
            else:
                print "socket error ", e
            conn.close()
            break
        except IOError, e:
            # Hmmm, Can IOError actually be raised by the socket module?
            print "Got IOError: ", e
            break

    conn.close()
