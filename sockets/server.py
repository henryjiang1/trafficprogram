import socket
import pickle
import numpy as np


HOST=''
PORT=5555

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(2)
print('Socket now listening')

conn,addr=s.accept()

while True:
    full_msg = b''
    msg = conn.recv(16)
    full_msg += msg.decode('utf-8')
    with open('../dict.txt', "r+") as f:
        f.seek(0)
        f.truncate()
    with open("../dict.txt", "a+") as f:
        content = f.read()
        f.write(full_msg)

