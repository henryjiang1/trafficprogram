from adafruit_motorkit import MotorKit
from time import sleep
kit = MotorKit()

class Motor():
    def __init__(self, motor1, motor2, motor3, motor4):
        self.motor1 = kit.motor1
        self.motor2 = kit.motor2
        self.motor3 = kit.motor3
        self.motor4 = kit.motor4

        self.mySpeed=0

    def move(self,speed=0.5,turn=0,t=0):
        turn *=0.7
        leftSpeed = speed-turn
        rightSpeed = speed+turn
        if leftSpeed>1: leftSpeed =1
        elif leftSpeed<-1: leftSpeed = -1
        if rightSpeed>1: rightSpeed =1
        elif rightSpeed<-1: rightSpeed = -1
        #print(leftSpeed,rightSpeed)

        self.motor1.throttle = leftSpeed
        self.motor2.throttle = leftSpeed
        self.motor3.throttle = rightSpeed
        self.motor4.throttle = rightSpeed

        sleep(t)
    def stop(self,t=0):
        self.motor1.throttle = 0
        self.motor2.throttle = 0
        self.motor3.throttle = 0
        self.motor4.throttle = 0
        self.mySpeed = 0
        sleep(t)
def main():
    motor.move(0.5,0,2)
    motor.stop(2)
    motor.move(-0.5,0,2)
    motor.stop(2)
    motor.move(0,0.5,2)
    motor.stop(2)
    motor.move(0,-0.5,2)
    motor.stop(2)
if __name__ == '__main__':
    motor= Motor()
    main()