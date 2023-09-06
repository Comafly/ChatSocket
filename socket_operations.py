import socket
import threading
import tkinter as tk
import tkinter.messagebox as messagebox

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_to_server(username, server_ip, server_port, show_chat_window_callback):
    """
    Connects to the chat server and initializes the chat window.

    Parameters:
    - username (str): The username of the client.
    - server_ip (str): IP address of the chat server.
    - server_port (int): Port number of the chat server.
    - show_chat_window_callback (function): Callback function to show the chat window.
    """

    USERNAME = username

    try:
        # Connect to the server.
        client_socket.connect((server_ip, server_port))

        # Send the username to the server.
        client_socket.send(username.encode('utf-8'))

        # Show the chat window
        chat_window_text = show_chat_window_callback()

        # Create a new thread to receive messages from the server, passing the chat_window_text widget.
        receive_thread = threading.Thread(target=receive_message, args=(chat_window_text,))
        receive_thread.start()

    except Exception as e:
        messagebox.showerror("Connection Failed", str(e))

def receive_message(chat_window_text):
    """
    Continuously listens for incoming messages from the chat server and updates the chat window.

    Parameters:
    - chat_window_text (tk.Text): Text widget of the chat window to display incoming messages.
    """

    while True:
        try:
            # Receive message from the server.
            message = client_socket.recv(1024).decode('utf-8')
            # Schedule GUI update on the main thread.
            chat_window_text.after(0, lambda: chat_window_text.insert(tk.END, message + '\n'))
        except:
            # Failed to receive message (likely disconnected).
            break

def send_message(message_entry):
    """
    Sends a message from the client to the chat server.

    Parameters:
    - message_entry (tk.Entry): Entry widget from which the message text is retrieved.
    """
    
    # Get the message from the text entry area.
    message = message_entry.get()
    if message:
        # Send the message to the server.
        client_socket.send(message.encode('utf-8'))
        # Clear the text entry area.
        message_entry.delete(0, tk.END)

def disconnect_and_exit(login_window, chat_window):
    """
    Sends a disconnect message to the server, closes the socket, and exits the application.

    Parameters:
    - login_window (tk.Tk or tk.Toplevel): The main login window of the chat client.
    - chat_window (tk.Toplevel): The chat window of the chat client.
    """

    try:
        disconnect_message = "DISCONNECTED"
        client_socket.send(disconnect_message.encode('utf-8'))
    except:
        pass 

    # Close the client socket.
    client_socket.close()

    # Check if chat_window exists and destroy it.
    try:
        chat_window.destroy()
    except NameError:
        pass

    # Exit the application.
    login_window.quit()
    login_window.destroy()

def change_username(new_username):
    """
    Sends a request to the server to change the client's username.

    Parameters:
    - new_username (str): The new username to be set for the client.
    """

    try:
        username_message = "CHANGE_USERNAME:"+new_username
        client_socket.send(username_message.encode('utf-8'))
    except:
        pass 