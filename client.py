import socket
from _thread import *
import _pickle as cPickle
import threading
import sys


host, port = "127.0.0.1", 12345
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
    try:
        while msg == '':
            msg = int(input('>>'), 10)
    except (ValueError, TypeError):
        return 'no int'
    return msg


def display_message(data):
    global is_running
    if data == 'WELCOME':
        print('Bine ai venit. Ghiceste numarul :)')
    elif data == 'GREATER':
        print('Numarul este mai mare decat numarul ales.')
    elif data == 'LOWER':
        print('Numarul este mai mic decat numarul ales.')
    elif 'CORRECT' in data:
        print('Numarul este corect. Scorul tau:', data.split('#')[1])
        is_running = False
    elif data == 'NEW':
        print('Introdu un numar intre [0, 50] ca celalalt jucator sa il ghiceasca.')
    elif data == 'WAIT':
        print('Asteapta pana cand celalalt client va introduce un numar.')
    elif data == 'WAIT_RESULT':
        print('Asteapta pana cand celalalt client va ghici numarul introdus de tine.')
    elif 'FINISH' in data:
        print('Celalalt client a ghicit numarul din', data.split('#')[1], 'incercari.')
        print('Continua si tu jocul pana ghicesti numarul.')


def Main():
    global is_running
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    # cThread = threading.Thread(target=recv_message, args=(s,))
    # cThread.daemon = True
    # cThread.start()

    try:
        while True:
            # read
            data = s.recv(1024)
            if not data:
                break

            data = cPickle.loads(data)
            # print("Received: {}".format(data))
            display_message(data)

            if is_running is False:
                break

            # write
            message = 'no int'
            while message == 'no int':
                message = read_input()

            if message == "stop":
                break

            s.send(cPickle.dumps(message))
    finally:
        s.close()

if __name__ == '__main__': 
	Main()

