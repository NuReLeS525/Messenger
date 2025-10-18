import socket

SERVER_IP = "10.40.1.103"
PORT = 6565

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((SERVER_IP, PORT))

message = input("Введите сообщение для сервера: ")
client_socket.sendall(message.encode('utf-8'))

client_socket.close()