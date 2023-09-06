"""
A simple chat server that allows multiple clients to connect, chat, and manage usernames. 
The server broadcasts messages from one client to all other connected clients.
"""

import socket
import threading

# Server configuration.
HOST_IP = 'localhost'
PORT = 8000
MAX_CLIENTS = 10

# Dictionary to store connected clients with their unique ID and username.
client_data = {}
lock = threading.Lock()

def handle_client(client_socket, client_address):
    """
    Manage the client's connection, receiving messages and handling specific commands.
    
    Parameters:
    - client_socket (socket): The socket object for the client.
    - client_address (tuple): A tuple containing the client's IP address and port number.
    """

    initial_username = client_socket.recv(1024).decode('utf-8')
    unique_id = client_address[1]  # Use the client's port as a unique ID for simplicity.
    
    with lock:
        client_data[client_socket] = (unique_id, initial_username)
    
    print(f"{initial_username} ({unique_id}) connected from {client_address}")
    
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            
            if not message:
                break

            # Fetching the latest username from client_data
            _, current_username = client_data[client_socket]

            # Check for change username command.
            if message.startswith("CHANGE_USERNAME:"):
                new_username = message.split(":", 1)[1]
                with lock:
                    client_data[client_socket] = (unique_id, new_username)
                print(f"{current_username} ({unique_id}) changed their username to {new_username}")
                continue

            # Check for disconnection message.
            if message == "DISCONNECTED":
                print(f"{current_username} ({unique_id}) from {client_address} has disconnected.")
                with lock:
                    del client_data[client_socket]
                break

            formatted_message = f"{current_username} ({unique_id}): {message}"
            print(f"Received message from {client_address}: {formatted_message}")
            broadcast(formatted_message)

        except socket.error:
            print(f"Client {client_address} has disconnected abruptly.")
        
        except:
            break

def broadcast(message):
    """
    Send the provided message to all currently connected clients.

    Parameters:
    - message (str): The message to broadcast.
    """

    with lock:
        # Send the message to all connected clients.
        for client in list(client_data.keys()):
            try:
                client.send(message.encode('utf-8'))
            except:
                # If sending fails, client is likely disconnected.
                client.close()
                del client_data[client]

def start_server():
    """
    Start the chat server, listen for incoming client connections and spawn new threads to handle them.
    """

    # Create a socket object.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port.
    server_socket.bind((HOST_IP, PORT))

    # Listen for incoming connections.
    server_socket.listen(MAX_CLIENTS)
    print("Server started. Waiting for connections...")

    while True:
        # Accept a client connection.
        client_socket, client_address = server_socket.accept()
        print(f"Client connected: {client_address}")

        # Create a new thread to handle the client.
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()


if __name__ == "__main__":
    start_server()