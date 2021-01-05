import socket
import threading
import _pickle as cPickle
from _thread import *
import threading
from random import randint


host, port = "", 12345
chosen_number = -1
is_running = True


'''
variabila ce tine evidenta clientilor (socket list)
'''
connections = []


'''
exista niste pasi ce sunt parcursi in momentul in care
sunt mai multi clienti conectati:

0:
	al doilea client va trimite un numar catre server
	primul client asteapta pana cand numarul este perceput

1:
	numarul de ghicit este retinut de server
	primul client trebuie sa-l ghiceasca
	al doilea client (cel care a introdus) asteapta pana ce numarul este ghicit
	restul clientilor (daca vor exista) vor ghici numarul introdus de al doilea client

2:
	jocul se desfasoara => clientul care a trimis numarul de ghicit va astepta
'''
multiplayer_steps = 0


'''
variabila retine scorul pentru fiecare client
'''
score = 0
global last_score
last_score = 0


'''
Modul de a identifica clientul:
client1 -> fiecare client este instiintat individual in funcite de joc
client2 -> clientii sunt instiintati in functie de ce fac ceilalti clienti
'''
client_type = 0


'''
Starea curenta a jocului:
0 = single player
1 = multiplayer:
	- al doilea jucator care se conecteaza va alege mereu un numar
	- primul client sau ceilalti in afara de cel carea a ales numarul,
	va/vor trebui sa-l ghiceasca
2 = numarul a fost ghicit de un client -> joc terminat
'''
##global gamestate


'''
jucatorul care trimite catre server numarul de ghicit este numit leader
'''
global leader


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
	global multiplayer_steps, chosen_number, score, client_type, last_score, leader
	try:
		if multiplayer_steps == 0:
			data = 'WELCOME'
		elif multiplayer_steps == 1:
			data = 'WAIT'
		elif multiplayer_steps == 2:
			data = 'GUESS_NR'

		client.send(cPickle.dumps(data))

		last_data = ''

		while True:
			data = client.recv(1024)
			if not data:
				break

			if 'CORRECT' in last_data:
				data = 'GAME_OVER'
				client.send(cPickle.dumps(data))
				break

			data = cPickle.loads(data)
			print('received `{}`'.format(data))

			if client_type == 0:
				if 'client2' in str(data):
					client_type = 2
					data = data.split('#')[1]
				else:
					client_type = 1

			# am un singur client
			if len(connections) == 1:
				data = check_number(data, random_number)

				# clientul care a introdus numarul asteapta
				if last_data == 'WAIT_RESULT':
					data = data + '2' + '#' + str(last_score)
			else:
				if multiplayer_steps == 0:
					# al doilea client (sau ultimul) va trimite numarul catre server
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
						leader = client
						print('Numarul care trebuie ghicit:', chosen_number)
						data = 'WAIT_RESULT'
						multiplayer_steps = 2
					else:
						data = 'WAIT'
				else:
					if client == leader:#connections[-1]:
						data = 'WAIT_RESULT'
					else:
						data = check_number(data, chosen_number)
						last_score = score

						# notific clientii
						if client_type == 2:
							for c in range(0, connections):
								connections[c].send(cPickle.dumps(data))
							continue

			client.send(cPickle.dumps(data))

			# instiintez clientii de scorul unui client care a terminat deja
			if client_type == 2:
				if 'CORRECT' in data:
					for c in range(0, connections):
						# daca nu, o sa trimit FINISH
						data = 'GAME_OVER' if connections[c] == client else 'NOTIFY'
						connections[c].send(cPickle.dumps(data))
			
			last_data = data
	finally:
		print('Client {} disconnected'.format(client))
		connections.remove(client)

		# cand va fi din nou un client vom reseta numarul ales de ultimul client conectat
		if len(connections) == 1:
			# data = 'FINISH' + '#' + str(score)
			# connections[0].send(cPickle.dumps(data))
			chosen_number = -1
			multiplayer_steps = 0
			leader = -1

		score = 0
		client.close()


if __name__ == '__main__':
	#global random_number, is_running
	random_number = randint(0, 50)
	print('Numarul generat este', random_number)

	leader = -1

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	print("Socket binded to port", port)

	s.listen(2)
	print("Socket is listening...")

	while True:
		client, addr = s.accept()
		print('Client connected (', addr[0], ':', addr[1], ')')
		cThread = threading.Thread(target=UTIL_handleClient, args=(client,))
		cThread.daemon = True
		cThread.start()
		connections.append(client)

	# client, addr = s.accept()
	# print('Client connected (', addr[0], ':', addr[1], ')')
	# cThread = threading.Thread(target=UTIL_handleClient, args=(client,))
	# cThread.daemon = True
	# cThread.start()
	# connections.append(client)

	message = ''
	while not message == 'stop':
		message = input()

	s.close()

