import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from PIL import Image

class LoginWindow(ctk.CTkFrame):
    def __init__(self, parent, login_callback):
        super().__init__(parent)
        self.parent = parent
        self.login_callback = login_callback
        
        # Configure grid
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_columnconfigure(1, weight=1)  # Make main frame expand
        self.grid_rowconfigure(0, weight=1)
        
        # Configure the main window
        self.parent.title("House of Assembly - Login")
        self.parent.attributes('-fullscreen', True)
        self.parent.bind('<Escape>', self.toggle_fullscreen)
        
        # Configure the frame
        self.pack(fill="both", expand=True)
        self.configure(fg_color="#1a237e")  # Deep blue background
        
        # Create main frames
        self.create_sidebar()
        self.create_main_frame()
        
    def create_sidebar(self):
        # Sidebar frame with deep blue color
        self.sidebar = ctk.CTkFrame(
            self,
            fg_color="#1a237e",
            corner_radius=0
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)
        
        # Header Section
        header_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(50, 20), sticky="ew")
        # Logo
        logo_image = ctk.CTkImage(
            light_image=Image.open("logo.png"),
            dark_image=Image.open("logo.png"),
            size=(120, 120)
        )
        ctk.CTkLabel(
            header_frame,
            text="",
            image=logo_image
        ).pack(pady=(0, 10))


        ctk.CTkLabel(
            header_frame,
            text="EKITI STATE",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        ).pack(pady=(20, 5))
        
        ctk.CTkLabel(
            header_frame,
            text="HOUSE OF ASSEMBLY",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        ).pack(pady=(20, 5))
        
        ctk.CTkLabel(
            header_frame,
            text="Official Access Portal",
            font=ctk.CTkFont(size=16),
            text_color="#90caf9"
        ).pack(pady=5)
        
        # Current Date/Time
        self.time_label = ctk.CTkLabel(
            self.sidebar,
            text="",
            font=ctk.CTkFont(size=14),
            text_color="#90caf9"
        )
        self.time_label.grid(row=1, column=0, pady=20)
        self.update_time()
        
        # Notice Section
        notice_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="#1565c0",
            corner_radius=10
        )
        notice_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        
        ctk.CTkLabel(
            notice_frame,
            text="OFFICIAL NOTICE",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            notice_frame,
            text="This is a secure government system.\nUnauthorized access is prohibited.",
            font=ctk.CTkFont(size=12),
            text_color="#e3f2fd"
        ).pack(pady=(0, 15))
        
        # Version at bottom
        ctk.CTkLabel(
            self.sidebar,
            text="System Version 2.1.0\nBuild 2024.01.25",
            font=ctk.CTkFont(size=12),
            text_color="#90caf9"
        ).grid(row=5, column=0, pady=20)
        
    def create_main_frame(self):
        # Main content frame
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color="#f5f5f5",
            corner_radius=0
        )
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        
        # Login form container
        form_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="white",
            corner_radius=15
        )
        form_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Welcome text
        ctk.CTkLabel(
            form_frame,
            text="Welcome to the Assembly Portal",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#1a237e"
        ).pack(padx=40, pady=(30, 5))
        
        ctk.CTkLabel(
            form_frame,
            text="Please authenticate your credentials",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack(pady=(0, 20))
        
        # User ID Entry
        ctk.CTkLabel(
            form_frame,
            text="OFFICIAL ID",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#1a237e"
        ).pack(padx=40, anchor="w")
        
        self.username_entry = ctk.CTkEntry(
            form_frame,
            width=300,
            height=40,
            placeholder_text="Enter your official ID"
        )
        self.username_entry.pack(padx=40, pady=(5, 15))
        
        # Password Entry
        ctk.CTkLabel(
            form_frame,
            text="PASSWORD",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#1a237e"
        ).pack(padx=40, anchor="w")
        
        self.password_entry = ctk.CTkEntry(
            form_frame,
            width=300,
            height=40,
            placeholder_text="Enter your password",
            show="•"
        )
        self.password_entry.pack(padx=40, pady=(5, 15))
        
        # Remember Device
        self.remember = ctk.CTkCheckBox(
            form_frame,
            text="Remember this device",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            fg_color="#1a237e"
        )
        self.remember.pack(padx=40, pady=(0, 15), anchor="w")
        
        # Login Button
        self.login_btn = ctk.CTkButton(
            form_frame,
            text="ACCESS SYSTEM",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1a237e",
            hover_color="#0d47a1",
            width=300,
            height=40,
            command=self.handle_login
        )
        self.login_btn.pack(padx=40, pady=(0, 20))
        
        # Support link
        ctk.CTkButton(
            form_frame,
            text="Contact Technical Support",
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            text_color="#1565c0",
            hover_color="#e3f2fd"
        ).pack(pady=(0, 30))
        
    def update_time(self):
        current_time = datetime.now().strftime("%d %B, %Y\n%I:%M:%S %p")
        self.time_label.configure(text=current_time)
        self.after(1000, self.update_time)
        
    def toggle_fullscreen(self, event=None):
        self.parent.attributes('-fullscreen', not self.parent.attributes('-fullscreen'))
        
    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username == "admin" and password == "admin":
            user_data = {
                "username": username,
                "role": "Speaker",
                "is_admin": True
            }
            self.login_callback(user_data)  # Pass user data to callback
        else:
            messagebox.showerror("Error", "Invalid credentials") 