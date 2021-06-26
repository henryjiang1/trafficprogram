import cv2
import io
import socket
import struct
import time
import pickle
import zlib

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.226.1', 5000))
connection = client_socket.makefile('wb')

cap = cv2.VideoCapture(0)

cap.set(4, 240)

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    ret, frame = cap.read()
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    data = pickle.dumps(frame, 0)
    size = len(data)

    client_socket.sendall(struct.pack(">L", size) + data)

    curve_val = ''
    msg = client_socket.recv(8)
    curve_val += msg.decode('utf-8')
    curve_int = int(curve_val)

    sen = 1.3  # SENSITIVITY
    maxVal = 0.3  # MAX SPEED
    if curve_int > maxVal: curve_int = maxVal
    if curve_int < -maxVal: curve_int = -maxVal
    # print(curve_int)
    if curve_int > 0:
        sen = 1.7
        if curve_int < 0.05: curve_int = 0
    else:
        if curve_int > -0.08: curve_int = 0

    curve_val = str(curve_int * sen)
    #motor.move(0.20, -curve_int * sen, 0.05)

    with open('curveval.txt', "r+") as f:
        f.seek(0)
        f.truncate()
    with open("curveval.txt", "a+") as f:
        content = f.read()
        f.write(curve_val)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()