# Import required modules
import socket
import threading

HOST = '127.0.0.1'
PORT = 1234 # You can use any port between 0 to 65535
LISTENER_LIMIT = 5
active_clients = [] # List of all currently connected users

# Function to listen for upcoming messages from a client
# def listen_for_messages(client, username):

#     while 1:

#         message = client.recv(2048).decode('utf-8')
#         if message != '':
            
#             final_msg = username + '~' + message
#             send_messages_to_all(final_msg)

#         else:
#             print(f"The message send from client {username} is empty")

def listen_for_messages(client, username):
    while True:
        try:
            # First receive header
            header = client.recv(1024).decode('utf-8')
            if header.startswith("VIDEO~"):
                _, filename, filesize = header.split("~")
                filesize = int(filesize)

                # Receive the video file
                video_data = b''
                while len(video_data) < filesize:
                    packet = client.recv(4096)
                    if not packet:
                        break
                    video_data += packet

                # Send video to all clients
                for user in active_clients:
                    user_client = user[1]
                    try:
                        # Send header first
                        user_client.sendall(f"VIDEO~{username}~{filename}~{filesize}".encode('utf-8'))
                        # Then send binary data
                        user_client.sendall(video_data)
                    except Exception as e:
                        print(f"Error sending video to {user[0]}: {e}")

            else:
                # It's a text message
                message = header
                if message != '':
                    final_msg = username + '~' + message
                    send_messages_to_all(final_msg)
                else:
                    print(f"The message from client {username} is empty")

        except Exception as e:
            print(f"Error: {e}")
            break



# Function to send message to a single client
def send_message_to_client(client, message):

    client.sendall(message.encode())

# Function to send any new message to all the clients that
# are currently connected to this server
def send_messages_to_all(message):
    
    for user in active_clients:

        send_message_to_client(user[1], message)

# Function to handle client
def client_handler(client):
    
    # Server will listen for client message that will
    # Contain the username
    while 1:

        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = "SERVER~" + f"{username} added to the chat"
            send_messages_to_all(prompt_message)
            break
        else:
            print("Client username is empty")

    threading.Thread(target=listen_for_messages, args=(client, username, )).start()

# Main function
def main():

    # Creating the socket class object
    # AF_INET: we are going to use IPv4 addresses
    # SOCK_STREAM: we are using TCP packets for communication
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Creating a try catch block
    try:
        # Provide the server with an address in the form of
        # host IP and port
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    # Set server limit
    server.listen(LISTENER_LIMIT)

    # This while loop will keep listening to client connections
    while 1:

        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")

        threading.Thread(target=client_handler, args=(client, )).start()


if __name__ == '__main__':
    main()