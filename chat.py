import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox

class ChatContent(ctk.CTkFrame):
    def __init__(self, parent, current_user, is_admin=False):
        super().__init__(parent)
        
        # Store user info
        self.current_user = current_user
        self.is_admin = is_admin
        
        # Configure frame
        self.configure(fg_color="#f1f5f9")
        
        # Store chat data
        self.messages = []
        self.private_chats = {}  # {user_id: [messages]}
        self.active_chat = "House"  # Default to group chat
        self.online_users = ["Admin User", "John Smith", "Jane Doe"]  # Demo users
        
        # Create UI sections
        self.create_layout()
        
    def create_layout(self):
        # Main container with 3 columns
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Left sidebar - Chat list
        self.create_chat_list()
        
        # Middle - Chat messages
        self.create_chat_area()
        
        # Right sidebar - Online users
        self.create_online_users()
        
    def create_chat_list(self):
        sidebar = ctk.CTkFrame(self, fg_color="white", width=250)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 2))
        sidebar.grid_propagate(False)
        
        # Header
        header = ctk.CTkFrame(sidebar, fg_color="transparent", height=70)
        header.pack(fill="x", padx=20, pady=20)
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header,
            text="💬",
            font=ctk.CTkFont(size=24)
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            header,
            text="Chats",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left")
        
        # Search box
        search_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        search_box = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search chats...",
            height=35
        )
        search_box.pack(fill="x")
        
        # Chat list
        chats_frame = ctk.CTkScrollableFrame(
            sidebar,
            fg_color="transparent"
        )
        chats_frame.pack(fill="both", expand=True, padx=10)
        
        # House group chat
        self.create_chat_item(
            chats_frame,
            "House",
            "Group chat for all members",
            "🏛️",
            True
        )
        
        # Divider
        divider = ctk.CTkFrame(chats_frame, fg_color="#e2e8f0", height=1)
        divider.pack(fill="x", pady=10)
        
        # Private chats
        for user in self.online_users:
            if user != self.current_user:
                self.create_chat_item(
                    chats_frame,
                    user,
                    "Click to start chat",
                    "👤"
                )
                
    def create_chat_item(self, parent, title, subtitle, icon, is_active=False):
        chat = ctk.CTkFrame(
            parent,
            fg_color="#f8fafc" if is_active else "transparent",
            corner_radius=10
        )
        chat.pack(fill="x", pady=2)
        
        # Add hover effect
        chat.bind("<Enter>", lambda e: chat.configure(fg_color="#f1f5f9"))
        chat.bind("<Leave>", lambda e: chat.configure(
            fg_color="#f8fafc" if self.active_chat == title else "transparent"
        ))
        chat.bind("<Button-1>", lambda e: self.switch_chat(title))
        
        # Icon
        icon_label = ctk.CTkLabel(
            chat,
            text=icon,
            font=ctk.CTkFont(size=20)
        )
        icon_label.pack(side="left", padx=10, pady=10)
        
        # Text
        text_frame = ctk.CTkFrame(chat, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(
            text_frame,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#000000",
            anchor="w"
        ).pack(fill="x")
        
        ctk.CTkLabel(
            text_frame,
            text=subtitle,
            font=ctk.CTkFont(size=12),
            text_color="#000000",
            anchor="w"
        ).pack(fill="x") 

    def create_chat_area(self):
        # Main chat container
        chat_container = ctk.CTkFrame(self, fg_color="white")
        chat_container.grid(row=0, column=1, sticky="nsew")
        chat_container.grid_rowconfigure(1, weight=1)
        chat_container.grid_columnconfigure(0, weight=1)
        
        # Chat header
        header = ctk.CTkFrame(chat_container, fg_color="transparent", height=70)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        header.grid_propagate(False)
        
        self.chat_title = ctk.CTkLabel(
            header,
            text="House Chat",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#000000"
        )
        self.chat_title.pack(side="left")
        
        # Messages area
        self.messages_frame = ctk.CTkScrollableFrame(
            chat_container,
            fg_color="transparent"
        )
        self.messages_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # Message input area
        input_frame = ctk.CTkFrame(chat_container, fg_color="transparent", height=100)
        input_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        input_frame.grid_propagate(False)
        
        # Message textbox
        self.message_input = ctk.CTkTextbox(
            input_frame,
            height=60,
            font=ctk.CTkFont(size=14)
        )
        self.message_input.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Send button
        send_button = ctk.CTkButton(
            input_frame,
            text="Send",
            width=100,
            height=35,
            font=ctk.CTkFont(size=14),
            fg_color="#1a237e",
            hover_color="#283593",
            command=self.send_message
        )
        send_button.pack(side="right", pady=12)
        
        # Bind Enter key to send message
        self.message_input.bind("<Return>", lambda e: self.send_message())
        self.message_input.bind("<Shift-Return>", lambda e: "break")

    def create_online_users(self):
        sidebar = ctk.CTkFrame(self, fg_color="white", width=200)
        sidebar.grid(row=0, column=2, sticky="nsew", padx=(2, 0))
        sidebar.grid_propagate(False)
        
        # Header
        header = ctk.CTkFrame(sidebar, fg_color="transparent", height=70)
        header.pack(fill="x", padx=20, pady=20)
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header,
            text="👥",
            font=ctk.CTkFont(size=24)
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            header,
            text="Online",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#000000"
        ).pack(side="left")
        
        # Online users list
        users_frame = ctk.CTkScrollableFrame(
            sidebar,
            fg_color="transparent"
        )
        users_frame.pack(fill="both", expand=True, padx=10)
        
        for user in self.online_users:
            self.create_user_item(users_frame, user)

    def create_user_item(self, parent, username):
        user = ctk.CTkFrame(parent, fg_color="transparent", corner_radius=10)
        user.pack(fill="x", pady=2)
        
        # Add hover effect
        user.bind("<Enter>", lambda e: user.configure(fg_color="#f1f5f9"))
        user.bind("<Leave>", lambda e: user.configure(fg_color="transparent"))
        user.bind("<Button-1>", lambda e: self.switch_chat(username))
        
        # User icon
        icon_label = ctk.CTkLabel(
            user,
            text="👤",
            font=ctk.CTkFont(size=20)
        )
        icon_label.pack(side="left", padx=10, pady=10)
        
        # Username
        ctk.CTkLabel(
            user,
            text=username,
            font=ctk.CTkFont(size=14),
            text_color="#000000",
            anchor="w"
        ).pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Online indicator
        ctk.CTkFrame(
            user,
            width=8,
            height=8,
            fg_color="#10b981",
            corner_radius=4
        ).pack(side="right", padx=10)

    def switch_chat(self, chat_name):
        self.active_chat = chat_name
        self.chat_title.configure(
            text=f"House Chat" if chat_name == "House" else f"Chat with {chat_name}"
        )
        self.show_messages()
        
    def send_message(self):
        message = self.message_input.get("1.0", "end-1c").strip()
        if not message:
            return "break"
        
        # Create message data
        message_data = {
            "sender": self.current_user,
            "content": message,
            "timestamp": datetime.now(),
            "chat": self.active_chat
        }
        
        # Store message
        if self.active_chat == "House":
            self.messages.append(message_data)
        else:
            if self.active_chat not in self.private_chats:
                self.private_chats[self.active_chat] = []
            self.private_chats[self.active_chat].append(message_data)
        
        # Clear input and show messages
        self.message_input.delete("1.0", "end")
        self.show_messages()
        return "break"

    def show_messages(self):
        # Clear current messages
        for widget in self.messages_frame.winfo_children():
            widget.destroy()
        
        # Get messages for current chat
        messages = (
            self.messages if self.active_chat == "House"
            else self.private_chats.get(self.active_chat, [])
        )
        
        # Show messages
        for message in messages:
            self.create_message_bubble(message)
        
    def create_message_bubble(self, message):
        is_own = message["sender"] == self.current_user
        
        bubble = ctk.CTkFrame(
            self.messages_frame,
            fg_color="#1a237e" if is_own else "#ffffff",
            corner_radius=15
        )
        bubble.pack(
            fill="x",
            pady=5,
            padx=(100 if is_own else 10, 10 if is_own else 100),
            anchor="e" if is_own else "w"
        )
        
        if not is_own:
            ctk.CTkLabel(
                bubble,
                text=message["sender"],
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#000000"
            ).pack(anchor="w", padx=15, pady=(10, 0))
        
        ctk.CTkLabel(
            bubble,
            text=message["content"],
            font=ctk.CTkFont(size=14),
            text_color="#ffffff" if is_own else "#000000",
            wraplength=400,
            justify="left"
        ).pack(anchor="w", padx=15, pady=10)
        
        time_text = message["timestamp"].strftime("%I:%M %p")
        ctk.CTkLabel(
            bubble,
            text=time_text,
            font=ctk.CTkFont(size=10),
            text_color="#ffffff" if is_own else "#000000"
        ).pack(anchor="e", padx=15, pady=(0, 5)) 