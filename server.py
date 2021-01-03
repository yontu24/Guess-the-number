import socket
import threading
import _pickle as cPickle
from _thread import *
import threading
from random import randint


host, port = "", 12345
random_number = 0
multiplayer = False
is_running = True

def UTIL_handleClient(c):
	global is_running
	try:
		while True:
			data = c.recv(1024)

			if not data:
				print("Am intrat")
				break

			data = cPickle.loads(data)
			print('received `{}`'.format(data))

			if multiplayer is False:
				data = data[::-1]
			else:
				data = data[::-1]
				data = "multi " + data

			c.send(cPickle.dumps(data))
	finally:
		print('Client {} disconnected'.format(c))
		c.close()
		is_running = False


if __name__ == '__main__':
	#global random_number, multiplayer, is_running
	random_number = randint(0, 50)
	print('Numarul generat este', random_number)

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	print("Socket binded to port", port)

	s.listen(2)
	print("Socket is listening...")

	client1, addr = s.accept()
	print('Client 1 connected (', addr[0], ':', addr[1], ')')
	cThread = threading.Thread(target=UTIL_handleClient, args=(client1,))
	cThread.daemon = True
	cThread.start()

	client2, addr = s.accept()
	multiplayer = True
	print('Client 2 connected (', addr[0], ':', addr[1], ')')
	cThread = threading.Thread(target=UTIL_handleClient, args=(client2,))
	cThread.daemon = True
	cThread.start()

#	s.close()
