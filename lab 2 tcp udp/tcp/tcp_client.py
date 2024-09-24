import socket

'''
Задание 1. Реализация TCP-сервера и TCP-клиента
КЛИЕНТ
'''

HOST = '127.0.0.1'
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected")
    while True:
        print("Sending data")
        msg = input("you: ")
        s.sendall(msg.encode())
        print("Recieving data")
        data = s.recv(1024)
        print('Echoing: ', repr(data))