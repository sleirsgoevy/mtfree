#!/usr/bin/python3
import subprocess, sys, os.path, urllib.request, _thread, time, marionette

#xvfb = subprocess.Popen(("Xvfb", ":47"))
xvfb = subprocess.Popen(("Xvfb", ":47", "-screen", "0", "1024x768x24"))

if '--debug' in sys.argv:
    x11vnc = subprocess.Popen(("x11vnc", "-display", ":47", "-N", "-noshm"))

def check_connection():
    if '--debug' in sys.argv:
        input()
        xvfb.kill()
        if '--keep-profile' not in sys.argv: subprocess.call(("rm", "-r", "profile"))
        exit()
    while True:
        time.sleep(3)
        try:
            with urllib.request.urlopen('http://ip-address.ru/show') as file:
                data = file.read().split(b'.')
        except: data = []
        if len(data) == 4 and all(set(i) <= set(range(48, 58)) for i in data):
            xvfb.kill()
            if '--keep-profile' not in sys.argv: subprocess.call(("rm", "-r", "profile"))
            exit()

def run_browser():
    while True:
        if '--keep-profile' not in sys.argv or not os.path.isdir("profile"):
            if os.path.exists("profile"):
                subprocess.call(("rm", "-r", "profile"))
            os.mkdir("profile")
            with open("profile/prefs.js", "w") as file:
                file.write('user_pref("app.normandy.first_run", false);\n')
                file.write('user_pref("datareporting.healthreport.service.firstRun", false);\n')
                file.write('user_pref("toolkit.telemetry.reportingpolicy.firstRun", false);\n')
        subprocess.call("DISPLAY=:47 firefox --new-instance --profile profile -marionette about:blank", shell=True)

BANNER_ELEM = '.click-area'
LOGIN_BTN = '.join' #'div.c-branding-button:nth-child(2)'
LOGIN_BTN_NEW = 'div.mt-col:nth-child(2) > button'
VIDEO_ELEM = '.content video' #at depth 3 #'div.c-video-layer:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > video:nth-child(1)'
INTERACTION_BUTTON = '.interaction_button'
INTERACTION_BUTTON_QUIZ = '.interaction_button_quiz'
INTERACTION_BUTTON_JOKE = '.interaction_button__joke'
INTERACTION_BUTTON_2 = '.Button'
CLOSE_BTN = '.mt-banner-fullscreen__button-close'
STATIC_AD = '.mt-banner-fullscreen__container-centered'

def main():
    rpc = marionette.RPC()
    rpc._version()
    rpc.newSession()
    rpc.navigate(url=('http://ip-address.ru/show' if '--direct' not in sys.argv else 'https://auth.wi-fi.ru'))
    tries = [[LOGIN_BTN, -1], [LOGIN_BTN_NEW, -1], [BANNER_ELEM, 5], [CLOSE_BTN, -1], [STATIC_AD, 5], [VIDEO_ELEM, 5], [INTERACTION_BUTTON, -1], [INTERACTION_BUTTON_QUIZ, -1], [INTERACTION_BUTTON_JOKE, -1], [INTERACTION_BUTTON_2, -1]]
    while True:
        url = rpc.getCurrentURL()
        for i in tries:
            if i[1] != 0:
                try: elem = next(iter(rpc.findElement(value=i[0], using='css selector')['value'].values()))
                except: continue
                print(i[0])
                try: rpc.elementClick(id=elem)
                except Exception as e: continue
                print(i[0])
                i[1] -= 1
                break

_thread.start_new_thread(main, ())
_thread.start_new_thread(run_browser, ())
check_connection()
