import re
import tkinter.messagebox as messagebox

def apply_colors(widget, bg_color, fg_color, highlight_bg_color=None, **kwargs):
    """
    Applies the color scheme to the approriate UI widgets.

    Parameters:
    - widget (tkinter.BaseWidget): The tkinter widget (e.g., Label, Button, Entry) to which the color scheme will be applied.
    - bg_color (str): The background color.
    - fg_color (str): The foreground color.
    - highlight_bg_color (str): The highlighted color.
    - kwargs: Any keyword arguments.
    """

    widget.configure(bg=bg_color, fg=fg_color, **kwargs)
    
    if highlight_bg_color:
        widget.configure(highlightbackground=highlight_bg_color, highlightcolor=highlight_bg_color)

def is_valid_username(username):
    """
    A valid username must be between 3-15 characters, and be alphanumeric.

    Parameters:
    - username (str): The username to verify.
    """
    if 3 <= len(username) <= 15 and username.isalnum():
        return True
    
    messagebox.showerror("Error", "Invalid username. It should be 4-15 characters long and contain no special characters.")
    return False

def is_valid_port(port):
    """
    Determines if the given port is valid.

    Parameters:
    - port (int or str): The port number to verify.
    """
    try:
        port = int(port)
        if 1 <= port <= 65535:
            return True
        else:
            messagebox.showerror("Error", "Invalid port number. It should be between 1 and 65535.")
            return False
    except ValueError:
        messagebox.showerror("Error", "Port number should be an integer.")
        return False

def is_valid_host_ip(ip):
    """
    Determines if the given IP address is valid.

    Parameters:
    - ip (str): The IP address to verify.
    """
    # Regular expression for matching IPv4 addresses.
    pattern = re.compile(r"^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$")
    if pattern.match(ip):
        return True
    else:
        messagebox.showerror("Error", "Invalid IP address format.")
        return False
