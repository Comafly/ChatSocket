"""
Provides the main entry point for the chat client application. 
It utilizes the GUI components defined in the 'gui_components' module to 
display the login window and initiate the main event loop.

Usage:
    Run this script to start the chat client application.
"""

import gui_components

# Start the chat client application by displaying the login window.
if __name__ == "__main__":
    login_win = gui_components.show_login_window()
    login_win.mainloop()
