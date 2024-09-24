import socket

'''
Задание 2. Реализация UDP-сервера и UDP-клиента
СЕРВЕР
'''

HOST = "127.0.0.1"
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print(f"UDP-сервер запущен на {HOST}:{PORT}. Ожидание пакетов...")

    while True:
        data, addr = s.recvfrom(1024)
        print(f"Получено: {data.decode()} от {addr}")
        s.sendto(data, addr)
