import socket
import threading
from _thread import *
import threading


host = ""
port = 12345

connections = []


def UTIL_handleClient(c):
	try:
		while True:
			data = c.recv(1024)
			if data == b'':
				raise RuntimeError("socket connection broken")

			data = data.decode()
			print('received `{}`'.format(data))
			data = data[::-1]

			c.send(data.encode())
	finally:
		c.close()
		connections.remove(c)


def Main(): 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	print("Socket binded to port", port)

	s.listen(2)
	print("Socket is listening...")
	while True: 
		c, addr = s.accept()
		cThread = threading.Thread(target=UTIL_handleClient, args=(c,))
		cThread.daemon = True
		cThread.start()
		connections.append(c)
		print('Connected to :', addr[0], ':', addr[1])
	s.close() 


if __name__ == '__main__': 
	Main()
    
