import socket
from _thread import *
import _pickle as cPickle
import threading
import sys


host, port = "127.0.0.1", 12345
is_running = True
first_msg = True


def recv_number(sock):
    global is_running
    while is_running:
        data = sock.recv(1024)
        if not data:
            break

        data = cPickle.loads(data)
        display_message(data)


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
    print('received `{}`'.format(data))
    if data == 'WELCOME':
        print('Bine ai venit. Ghiceste numarul :)')
    elif data == 'GREATER':
        print('Numarul este mai mare decat numarul ales.')
    elif 'GREATER2' in data:
        print('Numarul este mai mare decat numarul ales.')
        print('Celalalt client a ghicit numarul din', data.split('#')[1], 'incercari.')
    elif data == 'LOWER':
        print('Numarul este mai mic decat numarul ales.')
    elif 'LOWER2' in data:
        print('Numarul este mai mic decat numarul ales.')
        print('Celalalt client a ghicit numarul din', data.split('#')[1], 'incercari.')
    elif 'CORRECT' in data:
        print('Numarul este corect. Scorul tau:', data.split('#')[1])
        print('Introdu orice numar pentru a finaliza sesiunea.')
    elif data == 'GAME_OVER':
        print('Jocul s-a terminat. :)')
        is_running = False
    elif data == 'NEW':
        print('Introdu un numar intre [0, 50] ca celalalt jucator sa il ghiceasca.')
    elif data == 'WAIT':
        print('Asteapta pana cand liderul va introduce un numar.')
    elif data == 'WAIT_RESULT':
        print('Asteapta pana cand celalalt client va ghici numarul introdus de tine.')
    elif 'FINISH' in data:
        print('Celalalt client a ghicit numarul din', data.split('#')[1], 'incercari.')
        print('Continua si tu jocul pana ghicesti numarul.')
    elif data == 'GUESS_NR':
        print('Bine ai venit. Ghiceste numarul introdus de un client. :)')
    elif 'NOTIFY' in data:
        print('Unul dintre clienti a reusit sa termine jocul din', data.split('#')[1], 'incercari.')


def Main():
    global is_running, first_msg
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    cThread = threading.Thread(target=recv_number, args=(s,))
    cThread.daemon = True
    cThread.start()

    try:
        while True:
            if is_running == False:
                break
            
            number = 'no int'
            while number == 'no int' or not (0 <= number <= 50):
                number = read_input()

            if first_msg:
                number = 'client2' + '#' + str(number)
                first_msg = False

            s.send(cPickle.dumps(number))
    finally:
        s.close()

if __name__ == '__main__': 
	Main()

