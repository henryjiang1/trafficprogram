import socket
import sys
import cv2
import pickle
import numpy as np
import struct
import zlib
from cv2curve import LaneDetectionModule, utlis
from lanefinding import lanes
#from objectdetection import vehicle_detector2
#from sockets import imgclient, imgserver



HOST=''
PORT=5000

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(2)
print('Socket now listening')

conn,addr=s.accept()

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))

initialTrackbarVals = [150, 150, 50, 215]
utlis.initializeTrackbars(initialTrackbarVals)

while True:
    while len(data) < payload_size:
        print("Recv: {}".format(len(data)))
        data += conn.recv(4096)

    print("Done Recv: {}".format(len(data)))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: {}".format(msg_size))
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    canny_image = lanes.canny(frame)
    cropped_image = lanes.region_of_interest(canny_image)
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    averaged_lines = lanes.average_slope_intercept(frame, lines)
    line_image = lanes.display_averaged_lines(frame, averaged_lines)
    #combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    #cv2.imshow('line img', line_image)

    line_image = cv2.resize(line_image, (480, 240))
    curve = LaneDetectionModule.getLaneCurve(line_image, display=2)

    # objects_frame = vehicle_detector2.detect_objects(frame)
    # cv2.imshow('objects', objects_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    conn.send(bytes(f"{curve}", "utf-8"))