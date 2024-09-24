import socket

'''
Задание 2. Реализация UDP-сервера и UDP-клиента
СЕРВЕР
'''

HOST = "127.0.0.1"
PORT = 5000

def start_udp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((HOST, PORT))
    print(f"Server is awaiting a connecting to {HOST}:{PORT}")

    while True:
        data, adr = server.recvfrom(1024)
        print(f"Recieved message from client: {data.decode('utf-8')}")
        
        server.sendto(data, adr)
        print('Message was send')
        
        server.close()
        break

# Запускаем сервер
if __name__ == "__main__":
    start_udp_server()