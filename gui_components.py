"""
Provides the GUI components for the chat client application. 
It includes functions for displaying the login window and other related 
UI elements. It also interfaces with the utilities and socket_operations 
modules for various operations like applying color schemes, validating usernames, 
and handling socket operations.
"""

import tkinter as tk
import config
from utilities import apply_colors, is_valid_username
from socket_operations import connect_to_server, send_message, change_username, disconnect_and_exit

login_window = None
chat_window = None
COLORS = config.COLORS

def show_login_window():
    """Create and display the login window where the user can input their username, 
    server IP, and port number. This window serves as the initial interface before
    connecting to the chat server.

    Returns:
    - tkinter.Tk: The main login window object.
    """

    global login_window
    # Create the main window.
    login_window = tk.Tk()
    login_window.title("Chat Client")
    login_window.configure(background=COLORS["background"])

    # Get UI components.
    username_label, username_entry, server_ip_label, server_ip_entry, port_label, port_entry = create_settings_fields(login_window)

    # Create a connect button.
    connect_button = tk.Button(
        login_window, 
        text="Connect", 
        command=lambda: connect_to_server(
            username_entry.get(), 
            server_ip_entry.get(), 
            int(port_entry.get()), 
            show_chat_window
        )
    )
    connect_button.pack(padx=10, pady=10)

    apply_theme_to_settings(username_label, username_entry, server_ip_label, server_ip_entry, port_label, port_entry, button=connect_button)


    # Bind the Disconnect method to the Close event.
    login_window.protocol("WM_DELETE_WINDOW", lambda: disconnect_and_exit(login_window, chat_window))

    return login_window

def show_chat_window():
    """
    Hide the login window and display the main chat interface. This window is shown
    after a successful connection to the server and allows the user to send and receive
    messages.

    Returns:
    - tkinter.Text: The text widget in the chat window where messages are displayed.
    """

    # Hide the main window.
    login_window.withdraw()

    # Create the chat window.
    chat_window = tk.Toplevel()
    chat_window.title("Chat Window")
    chat_window.configure(background=COLORS["background"])

    # Create a text area to display messages.
    global chat_window_text
    chat_window_text = tk.Text(chat_window, bg='black', fg='white')
    chat_window_text.pack(padx=10, pady=10)

    # Create a text entry area for typing messages.
    global message_entry
    message_entry = tk.Entry(chat_window, width=50)
    message_entry.pack(padx=10, pady=10)

    # Create a send button.
    send_button = tk.Button(chat_window, text="Send", command = lambda: send_message(message_entry))
    send_button.pack(padx=10, pady=10)

    # Bind the Enter key to the send_message function.
    chat_window.bind('<Return>', lambda event: send_message(message_entry))

    # Bind the Disconnect method to the Close event.
    chat_window.protocol("WM_DELETE_WINDOW", lambda: disconnect_and_exit(login_window, chat_window))

    # Create a File menu.
    file_menu = tk.Menu(chat_window)
    chat_window.config(menu=file_menu)

    # Create a Settings submenu.
    settings_submenu = tk.Menu(file_menu)
    file_menu.add_cascade(label="File", menu=settings_submenu)
    settings_submenu.add_command(label="Change Username", command=show_settings_window)
    settings_submenu.add_separator()
    settings_submenu.add_command(label="Exit", command=lambda: disconnect_and_exit(login_window, chat_window))

    apply_colors(chat_window_text, COLORS["background"], COLORS["foreground"], COLORS["highlight_bg"])
    apply_colors(message_entry, COLORS["entry_bg"], COLORS["entry_fg"], COLORS["highlight_bg"])
    apply_colors(send_button, COLORS["btn_bg"], COLORS["btn_fg"], activebackground=COLORS["active_btn_bg"])

    return chat_window_text

def show_settings_window():
    """
    Display a settings window where the user can adjust their username. This window provides an interface 
    to change user settings without restarting the application.
    """

    # Create the settings window.
    settings_window = tk.Toplevel()
    settings_window.title("Settings")
    settings_window.configure(background=COLORS["background"])

    # Create the username label and entry.
    username_label = tk.Label(settings_window, text="Username:")
    username_label.pack(padx=10, pady=5, anchor=tk.W)

    username_entry = tk.Entry(settings_window)
    username_entry.insert(0, config.USERNAME) 
    username_entry.pack(padx=10, pady=5, fill=tk.X)

    # Create a save button to update the settings and close the window.
    save_button = tk.Button(settings_window, text="Save", command=lambda: save_settings(settings_window, username_entry.get()))
    save_button.pack(padx=10, pady=10)

    apply_theme_to_settings(username_label, username_entry, button=save_button)

def save_settings(settings_window, username):
    """
    Update the user's settings based on the input from the settings window. This 
    includes checking the validity of the new username, updating the global configuration
    and potentially sending a message to the server if the username is changed.

    Parameters:
    - settings_window (tkinter.Toplevel): The settings window that called this function.
    - username (str): The new username input by the user.
    - host_ip (str): The new server IP input by the user.
    - port (str): The new port number input by the user.
    """

    # If the username isn't the same, check if its valid.
    if(username != config.USERNAME):
        if not is_valid_username(username):
            return
        
        config.USERNAME = username
        change_username(username)

    # Close the settings window.
    settings_window.destroy()

def create_settings_fields(settings_window):
    """
    Create labels and entry fields for username, server IP, and port within the provided window.

    Parameters:
    - settings_window (tkinter.Toplevel): The window in which the components should be created.

    Returns:
    - tuple: A tuple containing the username_label, username_entry, server_ip_label, 
             server_ip_entry, port_label, and port_entry.
    """
    
    # Create labels and entry fields for username, server IP, and port.
    username_label = tk.Label(settings_window, text="Username:", bg='black', fg='white')
    username_label.pack(padx=10, pady=10)
    username_entry = tk.Entry(settings_window, width=30)
    username_entry.pack(padx=10, pady=5)
    username_entry.insert(tk.END, config.USERNAME)

    server_ip_label = tk.Label(settings_window, text="Server IP:", bg='black', fg='white')
    server_ip_label.pack(padx=10, pady=10)
    server_ip_entry = tk.Entry(settings_window, width=30)
    server_ip_entry.pack(padx=10, pady=5)
    server_ip_entry.insert(tk.END, config.HOST_IP)

    port_label = tk.Label(settings_window, text="Port:", bg='black', fg='white')
    port_label.pack(padx=10, pady=10)
    port_entry = tk.Entry(settings_window, width=30)
    port_entry.pack(padx=10, pady=5)
    port_entry.insert(tk.END, config.PORT)

    return username_label, username_entry, server_ip_label, server_ip_entry, port_label, port_entry

def apply_theme_to_settings(*widgets, button):
    """
    Apply the theme colors to the provided widgets and button.

    Parameters:
    - *widgets: A variable number of widgets (labels, entries, etc.).
    - button: The button widget (either "connect" or "save").
    """
    for widget in widgets[:-1]:  # applying theme for all widgets except the last one (button)
        if isinstance(widget, tk.Label):
            apply_colors(widget, COLORS["background"], COLORS["foreground"])
        elif isinstance(widget, tk.Entry):
            apply_colors(widget, COLORS["entry_bg"], COLORS["entry_fg"], COLORS["highlight_bg"])
    
    # Apply colors to the button
    apply_colors(button, COLORS["btn_bg"], COLORS["btn_fg"], activebackground=COLORS["active_btn_bg"])
