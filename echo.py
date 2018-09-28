import socket
from _thread import *

# cria um socket tcp/ip
host = ''
port = 9001
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#  liga a port ao socket
try:
    sock.bind((host, port))
except socket.error as e:
    print(str(e))

# escuta ate 5 conexoes.
sock.listen(5)
print('Esperando conexao.')


def thread_client(conectar):
    conectar.send(str.encode('Digite as informacoes.'))
    mensagem = ''

    while True:
        data = conectar.recv(2048)
        mensagem = mensagem+data.decode('utf-8')
        for string in data.decode('utf-8'):
            if string == '\n':

                resposta = 'Resposta do servidor: ' + mensagem
                mensagem = ''
                conectar.sendall(str.encode(resposta))

        if not data:  # se nao tiver dados sai do loop
            break
    conectar.close()  # fecha conexao.


while True:
    conectar, endereco = sock.accept()
    print('Conectado a: '+endereco[0]+':'+str(endereco[1]))   # exibe o ip que se conectou

    start_new_thread(thread_client, (conectar, ))
