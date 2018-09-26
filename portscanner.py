import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = 'google.com'


def portscanner(port):
    try:
        sock.connect((server, port))
        return True
    except:
        return False


for x in range(79, 82):
    if portscanner(x):
        print('port', x, 'esta aberto.')
    else:
        print('port', x, 'esta fechado.')
