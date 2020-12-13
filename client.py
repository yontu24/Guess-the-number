import socket
import time
from _thread import *
import threading

host = "127.0.0.1"
port = 12345

def recv_message(sock):
    while True:
        data = str(sock.recv(1024).decode())
        print("Received: {}".format(data))

def Main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    cThread = threading.Thread(target=recv_message, args=(s,))
    cThread.daemon = True
    cThread.start()

    try:
        while True :
            print('>>')
            message = input()
            s.send(message.encode())

            if message == "stop":
                break
    finally:
        time.sleep(1)
        s.close()

if __name__ == '__main__': 
	Main() 
