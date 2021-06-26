import sys

from cv2curve import WebcamModule

sys.path.append('..')
#from cv2curve.MotorModule import Motor
from cv2curve.LaneDetectionModule import getLaneCurve
import cv2

##################################################
#motor = Motor()


##################################################
def main():
    img = WebcamModule.getImg()
    curveVal = getLaneCurve(img, 2)
    sen = 1.3  # SENSITIVITY
    maxVAl = 0.3  # MAX SPEED
    if curveVal > maxVAl: curveVal = maxVAl
    if curveVal < -maxVAl: curveVal = -maxVAl
    # print(curveVal)
    if curveVal > 0:
        sen = 1.7
        if curveVal < 0.05: curveVal = 0
    else:
        if curveVal > -0.08: curveVal = 0
    #motor.move(0.20, -curveVal * sen, 0.05)
    # cv2.waitKey(1)


if __name__ == '__main__':
    while True:
        main()