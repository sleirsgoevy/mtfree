import socket, json

class RPC:
    def __init__(self):
        while True:
            try: self.sock = socket.create_connection(('127.0.0.1', 2828))
            except socket.error: pass
            else: break
    def _read(self, l):
        ans = b''
        while len(ans) < l:
            ans += self.sock.recv(l-len(ans))
        return ans.decode('utf-8')
    def __getattr__(self, attr):
        attr = 'WebDriver:'+attr[:1].upper()+attr[1:]
        def func(**args):
            if attr != 'WebDriver:_version':
                j = json.dumps([0, 0, attr, args])
                self.sock.sendall(("%d:%s"%(len(j), j)).encode('utf-8'))
            l = ''
            while l[-1:] != ':': l += self._read(1)
            ans = json.loads(self._read(int(l[:-1])))
            if isinstance(ans, list):
                if ans[2] != None:
                    raise Exception(ans[2])
                return ans[3]
            return ans
        return func
