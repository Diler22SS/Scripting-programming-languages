import socket

'''
Задание 1. Реализация TCP-сервера и TCP-клиента
КЛИЕНТ
'''

HOST = '127.0.0.1'
PORT = 5000

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    
    server.listen(1)
    print(f'Server is awaiting a connecting to {HOST}:{PORT}')
    
    while True:
        client, client_adr = server.accept()
        print(f'Client is connected {client_adr}')
        
        data = client.recv(1024)
        if data:
            print(f'Recieved message from client: {data.decode('utf-8')}')

            client.sendall(data)
            print('Message was send')
            
            server.close()
            break
        
        
        
if __name__ == "__main__":
    start_server()