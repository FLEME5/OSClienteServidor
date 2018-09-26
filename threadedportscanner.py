import socket
import threading
from queue import Queue

printLock = threading.Lock()

server = 'google.com'


def portscanner(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conectar = sock.connect((server, port))
        with printLock:
            print('port', port, 'esta aberto.')

        conectar.close()

    except:
        pass


def threader():
    while True:
        scanners = q.get()
        portscanner(scanners)
        q.task_done()


q = Queue()

for x in range(100):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

for scanner in range(1, 1001):
    q.put(scanner)

q.join()
