import socket
from _thread import *

host = ''
port = 9001
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.bind((host, port))
except socket.error as e:
    print(str(e))

# escuta ate 5 conexoes.
sock.listen(5)
print('Esperando conexao.')


def thread_client(conectar):
    conectar.send(str.encode('Digite as informacoes.'))
    inputusuario = ''

    while True:
        data = conectar.recv(2048)
        inputusuario = inputusuario+data.decode('utf-8')
        for string in data.decode('utf-8'):
            if string == '\n':
                resposta = 'Resposta do servidor: ' + inputusuario
                inputusuario = ''
                conectar.sendall(str.encode(resposta))

        if not data:
            break
    conectar.close()  # fecha conexao.


while True:
    conectar, endereco = sock.accept()
    print('Conectado a: '+endereco[0]+':'+str(endereco[1]))

    start_new_thread(thread_client, (conectar, ))
