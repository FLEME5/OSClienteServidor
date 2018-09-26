#!/usr/bin/python

import socket
import threading

# Cria um socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# liga o port ao socket
sock.bind(('0.0.0.0', 9000))
# escuta ate ter 5 conexoes
sock.listen(1)

conexoes = []


def threader(conexao, endereco):  # define o metodo que lida com os threads
    global conexoes
    while True:
        dados = conexao.recv(4096)  # recebe os dados em um buffer de 4096 bytes
        for c in conexoes:  # envia os dados para todos os usuarios conectados
            c.send(bytes(dados))  # converte de string para bytes
        if not dados:  # se nao receber mais dados quebra o loop
            conexoes.remove(conexao)
            conexao.close()  # e fecha a conexao
            break


while True:
    conexao, endereco = sock.accept()  # aceita a conexao
    cthread = threading.Thread(target=threader, args=(conexao, endereco))  # cria o thread
    cthread.daemon = True  # permite fechar o programa mesmo com threads abertos
    cthread.start()  # inicia o thread
    conexoes.append(conexao)
    print(conexoes)
