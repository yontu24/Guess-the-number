import socket
import time
from _thread import *
import _pickle as cPickle
import threading

host = "127.0.0.1"
port = 12345

is_running = True

def recv_message(sock):
    global is_running
    while is_running:
        # data = str(sock.recv(1024).decode())
        data = sock.recv(1024)

        if not data:
            break

        data = cPickle.loads(data)

        print("Received: {}".format(data))


def read_input():
    msg = ''
    while msg == '':
        try:
            msg = input()
        except EOFError as e:
            print(e)    

    return msg


def Main():
    global is_running
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    # cThread = threading.Thread(target=recv_message, args=(s,))
    # cThread.daemon = True
    # cThread.start()

    try:
        while True:
            print('>>')
            message = read_input()

            if is_running is False:
                break

            if message == "stop":
                break

            s.send(cPickle.dumps(message))

            data = s.recv(1024)

            if not data:
                break

            data = cPickle.loads(data)

            print("Received: {}".format(data))

    finally:
        # time.sleep(1)
        s.close()

if __name__ == '__main__': 
	Main() 
