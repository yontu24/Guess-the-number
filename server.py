import socket
import threading
import _pickle as cPickle
from _thread import *
import threading
from random import randint


host, port = "", 12345
chosen_number = -1
is_running = True
connections = []
multiplayer_steps = 0
score = 0
client_type = 0


def check_number(data, chosen_nr):
	global score
	score = score + 1
	data = int(data)
	if data < chosen_nr:
		data = 'LOWER'
	elif data > chosen_nr:
		data = 'GREATER'
	else:
		data = 'CORRECT' + '#' + str(score)
	return data


def UTIL_handleClient(client):
	# global is_running
	global multiplayer_steps, chosen_number, score, client_type
	try:
		data = 'WELCOME'
		client.send(cPickle.dumps(data))

		while True:
			data = client.recv(1024)
			if not data:
				break

			data = cPickle.loads(data)
			print('received `{}`'.format(data))

			if client_type == 0:
				if 'client2' in data:
					client_type = 2
					data = data.split('#')[1]
				else:
					client_type = 1

			# am un singur client
			if len(connections) == 1:
				data = check_number(data, random_number)
			# am doi clienti
			else:
				if multiplayer_steps == 0:
					# al doilea client va trimite numarul catre server
					if client == connections[-1]:
						# resetam scorul (jocul se desfasoara in 2)
						score = 0
						data = 'NEW'
						multiplayer_steps = 1
					else:
						data = 'WAIT'
				elif multiplayer_steps == 1:
					if client == connections[-1]:
						chosen_number = int(data)
						print('Numarul care trebuie ghicit:', chosen_number)
						data = 'WAIT_RESULT'
						multiplayer_steps = 2
					else:
						data = 'WAIT'
				else:
					if client == connections[-1]:
						data = 'WAIT_RESULT'
					else:
						data = check_number(data, chosen_number)

						# notific ambii clienti
						if client_type == 2:
							for c in connections:
								c.send(cPickle.dumps(data))
							continue

			client.send(cPickle.dumps(data))
	finally:
		print('Client {} disconnected'.format(client))
		connections.remove(client)

		# cand va fi din nou un client vom reseta numarul ales de ultimul client conectat
		if len(connections) == 1:
			# data = 'FINISH' + '#' + str(score)
			# connections[0].send(cPickle.dumps(data))
			chosen_number = -1
			multiplayer_steps = 0

		score = 0
		client.close()


if __name__ == '__main__':
	#global random_number, is_running
	random_number = randint(0, 50)
	print('Numarul generat este', random_number)

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	print("Socket binded to port", port)

	s.listen(2)
	print("Socket is listening...")

	client, addr = s.accept()
	print('Client connected (', addr[0], ':', addr[1], ')')
	cThread = threading.Thread(target=UTIL_handleClient, args=(client,))
	cThread.daemon = True
	cThread.start()
	connections.append(client)

	client, addr = s.accept()
	print('Client connected (', addr[0], ':', addr[1], ')')
	cThread = threading.Thread(target=UTIL_handleClient, args=(client,))
	cThread.daemon = True
	cThread.start()
	connections.append(client)

	message = ''
	while not message == 'stop':
		message = input()

	s.close()

