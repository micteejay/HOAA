import customtkinter as ctk
import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from login import LoginWindow
from dashboard import AssemblyDashboard
from data_manager import DataManager

class Application:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("House of Assembly")
        
        # Add on_login_success method to window for SignOut to use
        self.window.on_login_success = self.on_login_success
        
        # Set window size and position
        window_width = 1200
        window_height = 800
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Center the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.window.minsize(1000, 600)  # Set minimum window size
        
        # Configure grid
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        
        self.current_frame = None
        self.show_login()
        
        # Initialize data manager
        self.data_manager = DataManager()
        
    def show_login(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = LoginWindow(self.window, self.on_login_success)
        
    def show_dashboard(self, user_data):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = AssemblyDashboard(
            self.window,
            current_user=user_data,
            is_admin=user_data["is_admin"],
            data_manager=self.data_manager
        )
        
    def on_login_success(self, user_data):
        self.show_dashboard(user_data)
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()