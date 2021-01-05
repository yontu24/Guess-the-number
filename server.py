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
global client_type
client_type = 0


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


def send_message(data, curr_client=0, _all=0):
	if _all == 0:
		curr_client.send(cPickle.dumps(data))
	else:
		for c in range(len(connections)):
			if curr_client == connections[c]:
				continue

			connections[c].send(cPickle.dumps(data))


def UTIL_handleClient(client):
	# global is_running
	global multiplayer_steps, chosen_number, score, last_score, leader#, client_type, 
	client_type = 0
	try:
		if multiplayer_steps == 0:
			data = 'WELCOME'
		elif multiplayer_steps == 1:
			data = 'WAIT'
		elif multiplayer_steps == 2:
			data = 'GUESS_NR'

		send_message(data, curr_client=client)

		last_data = ''

		while True:
			print('client_type', client_type)
			print('last_data', last_data)
			data = client.recv(1024)
			if not data:
				break

			if 'CORRECT' in last_data:
				send_message('GAME_OVER', curr_client=client)
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
					if client == leader:
						data = 'WAIT_RESULT'
					else:
						data = check_number(data, chosen_number)
						last_score = score

						# notific clientii
						if client_type == 2:
							send_message(data, _all=1)
							if not 'CORRECT' in data:
								continue

			send_message(data, curr_client=client)

			# instiintez clientii de scorul unui client care a terminat deja
			if client_type == 2:
				if 'CORRECT' in data:
					print(data)
					send_message('GAME_OVER', curr_client=client) # daca nu, o sa trimit FINISH
					send_message('NOTIFY' + '#' + str(score), _all=1)
			
			last_data = data
	finally:
		print('Client {} disconnected'.format(client))
		# if len(connections) > 1:
		# 	send_message('CL_DISCONN' + '#' + str(connections.index(client)) + '#' + str(len(connections)), _all=1)
		connections.remove(client)

		# cand va fi din nou un client vom reseta numarul ales de ultimul client conectat
		if len(connections) == 1:
			# send_message('FINISH' + '#' + str(score), curr_client=connections[0])
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

