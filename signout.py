import customtkinter as ctk
from tkinter import messagebox
from login import LoginWindow

class SignOut:
    @staticmethod
    def handle_signout(dashboard, parent):
        """
        Handle the sign out process
        
        Args:
            dashboard: The current dashboard instance to be destroyed
            parent: The parent window (Application instance)
        """
        if messagebox.askyesno("Confirm Sign Out", "Are you sure you want to sign out?"):
            # Get the root window
            root = dashboard.winfo_toplevel()
            
            # Destroy current dashboard
            dashboard.destroy()
            
            # Create new login window directly
            LoginWindow(root, root.on_login_success) 