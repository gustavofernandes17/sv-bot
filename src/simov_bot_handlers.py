import cv2
import urllib.request
import numpy as np
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE    


stream = urllib.request.urlopen('http://192.168.43.144:81/stream')

def start_recording():
    bytesa = b''# MAKE IT BYTES
    while True:
        bytesa += stream.read(1024)
        a = bytesa.find(b'\xff\xd8')
        b = bytesa.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytesa[a:b+2]
            bytesa = bytesa[b+2:]
            i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            cv2.imshow('i', i)
            if cv2.waitKey(1) == 27:
                exit(0)

start_recording()