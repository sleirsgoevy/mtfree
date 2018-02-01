import subprocess, socket, signal, types, os

auth_ok = False

@types.MethodType(signal.signal, signal.SIGALRM)
def onChildExit():
    if not auth_ok:
        print('fail')
        exit(1)

PROFILE_PATH = os.getcwd() + '/MT_FREE'

popen = subprocess.Popen(('firefox', '--profile', PROFILE_PATH, 'http://ip-address.ru'))

sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 1320))
sock.listen(1)
sock.accept()[0].sendall(b"HTTP/1.0 200 OK\r\nContent-Type: text/html\r\nContent-Length: 31\r\nConnection: close\r\n\r\n<script>window.close()</script>")
sock.close()
auth_ok = True
print('ok')
