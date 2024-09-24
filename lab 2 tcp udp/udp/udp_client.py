import socket

'''
Задание 2. Реализация UDP-сервера и UDP-клиента
КЛИЕНТ
'''

HOST = "127.0.0.1"
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    message = "Hello, UDP Server!"
    s.sendto(message.encode(), (HOST, PORT))

    data, _ = s.recvfrom(1024)
    print(f"Получено: {data.decode()}")