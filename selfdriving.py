from cv2curve import LaneDetectionModule, MainRobotLane, utlis
from lanefinding import lanes
#from objectdetection import vehicle_detector2
#from sockets import imgclient, imgserver

import socket
import numpy as np
import cv2

vid = 'highway.mp4'

cap = cv2.VideoCapture(vid)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

frameCounter = 0

initialTrackbarVals = [150, 150, 50, 215]
utlis.initializeTrackbars(initialTrackbarVals)

while(cap.isOpened()):
    _, frame = cap.read()
    canny_image = lanes.canny(frame)
    cropped_image = lanes.region_of_interest(canny_image)
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    averaged_lines = lanes.average_slope_intercept(frame, lines)
    line_image = lanes.display_averaged_lines(frame, averaged_lines)
    #combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    #cv2.imshow('result', line_image)


    frameCounter += 1
    if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        frameCounter = 0

    line_image = cv2.resize(line_image, (480, 240))

    curve = LaneDetectionModule.getLaneCurve(line_image, display=2)
    print(curve)

    # objects_frame = vehicle_detector2.detect_objects(frame)
    # cv2.imshow('r', objects_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


