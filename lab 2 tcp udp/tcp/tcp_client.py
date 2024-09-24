import socket

'''
Задание 1. Реализация TCP-сервера и TCP-клиента
КЛИЕНТ
'''

HOST = '127.0.0.1'
PORT = 5000

def start_client(message):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    client.connect((HOST, PORT))
    print(f'Client is connected {HOST}:{PORT}')
    
    client.sendall(message.encode('utf-8'))
    
    data = client.recv(1024)
    print(f"Recieved message from server: {data.decode('utf-8')}")

    client.close()
        
        
if __name__ == "__main__":
    message = input('Input message: ')
    start_client(message)