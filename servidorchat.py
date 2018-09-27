import socket
import threading
import sys


class Servidor:  # classe servidor
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um socket TCP/IP
    conexoes = []

    def __init__(self):
        self.sock.bind(('0.0.0.0', 9000))  # liga o port ao socket
        self.sock.listen(1)  # escuta por conexoes

    def threader(self, conexao, endereco):  # define o metodo que lida com os threads do servidor
        while True:
            try:
                dados = conexao.recv(1024)  # recebe os dados em um buffer de 1024 bytes
                for c in self.conexoes:  # itera entre todos os usuarios conectados
                    c.send(dados)  # envia os dados para eles
                if not dados:  # se nao receber mais dados quebra o loop
                    # mostra o endereco e port que desconectou
                    print(str(endereco[0]) + ':' + str(endereco[1]) + ' Desconectado')
                    self.conexoes.remove(conexao)  # remove conexao da lista
                    conexao.close()  # fecha a conexao
                    break
            except ConnectionResetError:  # caso de uma conexao ser resetada
                print(str(endereco[0]) + ':' + str(endereco[1]) + ' Desconectado')
                self.conexoes.remove(conexao)
                conexao.close()
                break

    def run(self):
        while True:
            conexao, endereco = self.sock.accept()  # aceita a conexao
            sthread = threading.Thread(target=self.threader, args=(conexao, endereco))  # cria o thread
            sthread.daemon = True  # permite fechar o programa mesmo com threads abertos
            sthread.start()  # inicia o thread
            self.conexoes.append(conexao)  # adiciona a conexao a lista
            print(str(endereco[0]) + ':' + str(endereco[1]) + ' Conectado')  # mostra o endereco e port que conectou


class Cliente:  # classe cliente
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def enviarmensagem(self):
        while True:
            self.sock.send(bytes(input(""), 'utf-8'))  # converte os dados para bytes e os envia

    def __init__(self, endereco):
        self.sock.connect((endereco, 9000))

        cthread = threading.Thread(target=self.enviarmensagem)  # thread cliente
        cthread.daemon = True
        cthread.start()

        while True:
            dados = self.sock.recv(1024)
            if not dados:
                break
            else:
                print(str(dados, 'utf-8'))  # mostra os dados convertidos para string


if len(sys.argv) > 1:  # define se vai ser o cliente ou servidor.
    cliente = Cliente(sys.argv[1])
else:
    servidor = Servidor()
    servidor.run()
