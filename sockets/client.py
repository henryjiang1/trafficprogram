import socket
import time
import pickle
from mpu6050 import mpu6050

mpu = mpu6050(0x68)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.226.1', 5555))

while True:
    gyro_data = mpu.get_gyro_data()
    angle = gyro_data['y']

    #bluetooth stuff here

    data = {"gyro": f"{angle}", "ble": ""}
    msg = pickle.dumps(data)

    client_socket.send(bytes(msg, "utf-8"))

