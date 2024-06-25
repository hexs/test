import os
import urllib.request
from datetime import datetime

import numpy as np
import cv2


fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('output.avi', fourcc, 10.0, (640, 480))

path = 'VDO'
os.makedirs(path, exist_ok=True)
vidos_name = os.path.join(path, datetime.now().strftime("%y%m%d-%H%M%S.avi"))
out = cv2.VideoWriter(vidos_name, fourcc, 10.0, (640, 480))
# cv2.imwrite(f'img/{datetime.now().strftime("%S")}.png',img)
url = 'http://192.168.125.129:2000/old-image'
while True:
    req = urllib.request.urlopen(url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    frame = cv2.imdecode(arr, -1)

    out.write(frame)
    cv2.imshow('Original', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



