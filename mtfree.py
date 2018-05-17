#!/usr/bin/python3
import subprocess, sys, socket, json, os.path, urllib.request, signal, _thread

if not os.path.exists("profile0"):
    if os.path.exists("README.md"):
        subprocess.call(("cat", "README.md"))
    if '-midori' in sys.argv:
        os.mkdir("profile")
        with open("profile/midori.txt", "w") as file: pass
        subprocess.call('HOME="$(pwd)/profile" midori', shell=True)
        os.rename("profile", "profile0")
    else:
        os.mkdir("profile0")
        subprocess.call(("firefox", "--new-instance", "--profile", "profile0", "about:addons"))

xvfb = subprocess.Popen(("Xvfb", ":47"))

#subprocess.Popen("DISPLAY=:47 x11vnc", shell=True)
#subprocess.Popen("sleep 3; vncviewer 127.0.0.1", shell=True)

import time

def check_connection():
    while True:
        time.sleep(3)
        with urllib.request.urlopen('http://ip-address.ru/show') as file:
            data = file.read().split(b'.')
        if len(data) == 4 and all(set(i) <= set(range(48, 58)) for i in data):
            xvfb.kill()
            subprocess.call(("rm", "-r", "profile"))
            exit()

def run_browser():
    while True:
        if os.path.exists("profile"):
            subprocess.call(("rm", "-r", "profile"))
        subprocess.call(("cp", "-r", "profile0", "profile"))
        if os.path.exists("profile/midori.txt"):
            subprocess.call('DISPLAY=:47 HOME="$(pwd)/profile" midori -e Fullscreen http://auth.wi-fi.ru', shell=True)
        else:
            subprocess.call("DISPLAY=:47 firefox --new-instance --profile profile http://auth.wi-fi.ru", shell=True)

x = socket.socket()
x.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
x.bind(('', 4747))
x.listen(1)

def read_data():
    while True:
        y = x.accept()[0]
        f = y.makefile("rwb", 0)
        if f.readline().startswith(b"OPTIONS "):
            y.sendall(b"HTTP/1.1 200 OK\r\n")
            while True:
                ln = f.readline()
                if ln.isspace(): break
                k, v = ln.split(b": ", 1)
                if k == b"Origin":
                    y.sendall(b"Access-Control-Allow-Origin: "+v)
                elif k == b"Access-Control-Request-Method":
                    y.sendall(b"Access-Control-Allow-Methods: "+v)
                elif k == b"Access-Control-Request-Headers":
                    y.sendall(b"Access-Control-Allow-Headers: "+v)
            y.sendall(b"Connection: close\r\n\r\n")
            y.close()
        else: break
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

def xdotool(data):
    subprocess.call("DISPLAY=:47 xdotool "+data, shell=True)

BANNER_ELEM = '.click-area'
LOGIN_BTN = 'div.c-branding-button:nth-child(2)'
VIDEO_ELEM = 'div.c-video-layer:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > video:nth-child(1)'
INTERACTION_BUTTON = '.interaction_button'
CLOSE_BTN = '.mt-banner-fullscreen__button-close'
STATIC_AD = '.mt-banner-fullscreen__container-centered'

def main():
    read_data()
    xdotool("key F11")
    for i in range(3): read_data()
    while True:
        it = read_data()
        if '://wi-fi.ru' in it['url'] or 'wi-fi.ru' not in it['url']: break
        for i in (BANNER_ELEM, LOGIN_BTN, CLOSE_BTN, VIDEO_ELEM, INTERACTION_BUTTON):
            if i in it:
                x, y, w, h, s = it[i]
                if '-v' in sys.argv: print(s)
                x += w // 2
                y += h // 2
                xdotool("mousemove %d %d click 1"%(x, y))
                break

_thread.start_new_thread(main, ())
_thread.start_new_thread(run_browser, ())
check_connection()
