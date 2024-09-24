import socket

'''
Задание 2. Реализация UDP-сервера и UDP-клиента
КЛИЕНТ
'''

HOST = "127.0.0.1"
PORT = 5000

def start_udp_client(message):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    client.sendto(message.encode('utf-8'), (HOST, PORT))
    print(f'Message was send to {HOST}:{PORT}')

    data, _ = client.recvfrom(1024)
    print(f"Recieved message from server: {data.decode('utf-8')}")
    
    client.close()
    
# Запускаем клиента
if __name__ == "__main__":
    message = input('Input message: ')
    start_udp_client(message)