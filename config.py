"""
Configuration settings for the chat client application.
"""

# Default server settings for the chat client.
HOST_IP = 'localhost'  # IP address of the chat server. Default is localhost for local testing.
PORT = 8000            # Port number on which the chat server is running.
USERNAME = "DefaultUser"  # Default username for a new user.

# Color scheme used for the GUI components of the chat client:
COLORS = {
    "background": "#2E3A45",      # Main background color.
    "foreground": "#EAEFF2",      # Main text color.
    "entry_bg": "#3C4B5B",        # Background color for text entry fields.
    "entry_fg": "#EAEFF2",        # Text color for text entry fields.
    "btn_bg": "#1E2A38",          # Background color for buttons.
    "btn_fg": "#EAEFF2",          # Text color for buttons.
    "highlight_bg": "#4A5A6A",    # Background color for highlighted UI elements.
    "active_btn_bg": "#4A5A6A",   # Background color for active buttons.
}
