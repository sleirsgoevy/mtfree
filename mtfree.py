#!/usr/bin/python3
import subprocess, os.path, urllib.request, _thread, time, marionette

xvfb = subprocess.Popen(("Xvfb", ":47"))

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
        os.mkdir("profile")
        subprocess.call("DISPLAY=:47 firefox --new-instance --profile profile -marionette", shell=True)

BANNER_ELEM = '.click-area'
LOGIN_BTN = 'div.c-branding-button:nth-child(2)'
VIDEO_ELEM = 'div.c-video-layer:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > video:nth-child(1)'
INTERACTION_BUTTON = '.interaction_button'
INTERACTION_BUTTON_JOKE = '.interaction_button__joke'
CLOSE_BTN = '.mt-banner-fullscreen__button-close'
STATIC_AD = '.mt-banner-fullscreen__container-centered'

def main():
    rpc = marionette.RPC()
    rpc._version()
    rpc.newSession()
    rpc.navigate(url='http://ip-address.ru/show')
    tries = [[BANNER_ELEM, 5], [LOGIN_BTN, -1], [CLOSE_BTN, -1], [STATIC_AD, 5], [VIDEO_ELEM, 5], [INTERACTION_BUTTON, -1], [INTERACTION_BUTTON, -1]]
    while True:
        url = rpc.getCurrentURL()
        for i in tries:
            if i[1] != 0:
                try: elem = rpc.findElement(value=i[0], using='css selector')['value']['ELEMENT']
                except: continue
                try: rpc.elementClick(id=elem)
                except: continue
                print(i[0])
                i[1] -= 1
                break

_thread.start_new_thread(main, ())
_thread.start_new_thread(run_browser, ())
check_connection()
