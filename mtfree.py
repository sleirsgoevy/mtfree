#!/usr/bin/python3
import subprocess, sys, socket, json, os.path

if not os.path.exists("profile0"):
    if os.path.exists("README.md"):
        subprocess.call(("cat", "README.md"))
    os.mkdir("profile0")
    subprocess.call("firefox --new-instance --profile profile0 about:addons", shell=True)

subprocess.call(("cp", "-r", "profile0", "profile"))

xvfb = subprocess.Popen(("Xvfb", ":47"))
firefox = subprocess.Popen("DISPLAY=:47 firefox --new-instance --profile profile http://auth.wi-fi.ru", shell=True)

#subprocess.Popen("DISPLAY=:47 x11vnc", shell=True)
#subprocess.Popen("sleep 3; vncviewer 127.0.0.1", shell=True)

x = socket.socket()
x.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
x.bind(('127.0.0.1', 4747))
x.listen(1)

def read_data():
    y = x.accept()[0]
    f = y.makefile("rwb", 0)
    l = None
    while True:
        ln = f.readline()
        if ln.startswith(b"Content-Length: "):
            l = int(ln[16:].decode('utf-8'))
        elif ln.isspace(): break
    data = b''
    while len(data) < l:
        data += f.read(l-len(data))
    y.close()
    return json.loads(data.decode("utf-8"))

read_data()

def xdotool(data):
    subprocess.call("DISPLAY=:47 xdotool "+data, shell=True)

xdotool("key F11")

for i in range(3): read_data()

LOGIN_BTN = 'div.c-branding-button:nth-child(2)'
VIDEO_ELEM = 'div.c-video-layer:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > video:nth-child(1)'
INTERACTION_BUTTON = '.interaction_button'

def main():
    while True:
        it = read_data()
        if '://wi-fi.ru' in it['url'] or 'wi-fi.ru' not in it['url']: break
        for i in (LOGIN_BTN, VIDEO_ELEM, INTERACTION_BUTTON):
            if i in it:
                x, y, w, h, s = it[i]
                x += w // 2
                y += h // 2
                xdotool("mousemove %d %d click 1"%(x, y))

main()

xvfb.kill()

subprocess.call(("rm", "-r", "profile"))
