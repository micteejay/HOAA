import customtkinter as ctk
from datetime import datetime, timedelta
from tkinter import messagebox

class NewOrderDialog:
    def __init__(self, parent):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Create New Order")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'+{x}+{y}')
        
        self.create_dialog_content()
        
    def create_dialog_content(self):
        # Session Info
        session_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        session_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            session_frame,
            text="Session Information",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w")
        
        # Date picker (simplified for example)
        date_frame = ctk.CTkFrame(session_frame, fg_color="transparent")
        date_frame.pack(fill="x", pady=(10, 0))
        
        ctk.CTkLabel(
            date_frame,
            text="Date:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left")
        
        self.date_var = ctk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        date_entry = ctk.CTkEntry(
            date_frame,
            textvariable=self.date_var,
            width=120
        )
        date_entry.pack(side="left", padx=10)
        
        # Session type
        type_frame = ctk.CTkFrame(session_frame, fg_color="transparent")
        type_frame.pack(fill="x", pady=(10, 0))
        
        self.session_type = ctk.StringVar(value="Morning")
        
        ctk.CTkRadioButton(
            type_frame,
            text="Morning Session",
            variable=self.session_type,
            value="Morning"
        ).pack(side="left", padx=(0, 20))
        
        ctk.CTkRadioButton(
            type_frame,
            text="Afternoon Session",
            variable=self.session_type,
            value="Afternoon"
        ).pack(side="left")
        
        # Time selection
        time_frame = ctk.CTkFrame(session_frame, fg_color="transparent")
        time_frame.pack(fill="x", pady=(10, 0))
        
        ctk.CTkLabel(
            time_frame,
            text="Start Time:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left")
        
        self.time_var = ctk.StringVar(value="10:00")
        time_entry = ctk.CTkEntry(
            time_frame,
            textvariable=self.time_var,
            width=80
        )
        time_entry.pack(side="left", padx=10)
        
        # Buttons
        button_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            fg_color="#e11d48",
            hover_color="#be123c",
            width=100,
            command=self.dialog.destroy
        ).pack(side="right", padx=(10, 0))
        
        ctk.CTkButton(
            button_frame,
            text="Create Order",
            fg_color="#1a237e",
            hover_color="#283593",
            width=100,
            command=self.create_order
        ).pack(side="right")
        
    def create_order(self):
        try:
            date = datetime.strptime(self.date_var.get(), "%Y-%m-%d")
            time = datetime.strptime(self.time_var.get(), "%H:%M").time()
            session_type = self.session_type.get()
            
            order_data = {
                "date": date,
                "time": time,
                "session_type": session_type,
                "status": "Not Started",
                "items": []
            }
            
            self.result = order_data
            self.dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid date and time")

class AddItemDialog:
    def __init__(self, parent, current_time):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Add Program Item")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.current_time = current_time
        self.create_dialog_content()
        
    def create_dialog_content(self):
        # Title
        title_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            title_frame,
            text="Title:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w")
        
        self.title_var = ctk.StringVar()
        title_entry = ctk.CTkEntry(
            title_frame,
            textvariable=self.title_var,
            placeholder_text="Enter program title"
        )
        title_entry.pack(fill="x", pady=(5, 0))
        
        # Duration
        duration_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        duration_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            duration_frame,
            text="Duration (minutes):",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w")
        
        self.duration_var = ctk.StringVar(value="15")
        duration_entry = ctk.CTkEntry(
            duration_frame,
            textvariable=self.duration_var,
            width=80
        )
        duration_entry.pack(anchor="w", pady=(5, 0))
        
        # Buttons
        button_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            fg_color="#e11d48",
            hover_color="#be123c",
            width=100,
            command=self.dialog.destroy
        ).pack(side="right", padx=(10, 0))
        
        ctk.CTkButton(
            button_frame,
            text="Add Item",
            fg_color="#1a237e",
            hover_color="#283593",
            width=100,
            command=self.add_item
        ).pack(side="right")
        
    def add_item(self):
        try:
            duration = int(self.duration_var.get())
            title = self.title_var.get().strip()
            
            if not title:
                raise ValueError("Title cannot be empty")
                
            if duration <= 0:
                raise ValueError("Duration must be positive")
                
            end_time = (datetime.combine(datetime.today(), self.current_time) + 
                       timedelta(minutes=duration)).time()
                
            item_data = {
                "time": self.current_time.strftime("%I:%M %p"),
                "title": title,
                "status": "Pending",
                "duration": f"{duration} mins"
            }
            
            self.result = item_data
            self.dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))

class OrderOfDayContent(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configure grid
        self.grid(row=0, column=1, sticky="nsew")
        self.configure(fg_color="#f1f5f9")
        
        # Store order data
        self.order_data = None
        self.current_time = None
        
        # Store all orders
        self.orders = []
        self.selected_order = None
        
        self.create_header()
        self.create_content()
        
    def select_order(self, order):
        self.selected_order = order
        self.order_data = order
        self.current_time = order["time"]
        
        # Update button states
        self.status_button.configure(
            state="normal" if order["status"] == "Not Started" else "disabled",
            text="Start Session" if order["status"] == "Not Started" else (
                "End Session" if order["status"] == "In Progress" else "Session Ended"
            ),
            fg_color="#059669" if order["status"] == "Not Started" else "#e11d48"
        )
        
        self.new_item_button.configure(
            state="normal" if order["status"] != "Completed" else "disabled"
        )
        
        # Show order details
        self.show_order_details()
        
    def show_orders_list(self):
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        if not self.orders:
            self.show_empty_state()
            return
            
        # Create orders list
        for order in self.orders:
            self.create_order_card(order)
            
    def create_order_card(self, order):
        # Order card container with hover effect
        card = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=15)
        card.pack(fill="x", pady=(0, 15))
        
        # Add hover effect
        def on_enter(e):
            card.configure(fg_color="#f8fafc")
        
        def on_leave(e):
            card.configure(fg_color="white")
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        card.bind("<Button-1>", lambda e, o=order: self.select_order(o))
        
        # Card content
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=15)
        
        # Left side - Date and Session info
        info_frame = ctk.CTkFrame(content, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)
        
        date_label = ctk.CTkLabel(
            info_frame,
            text=order["date"].strftime("%A, %B %d, %Y"),
            font=ctk.CTkFont(size=16, weight="bold")
        )
        date_label.pack(anchor="w")
        
        session_text = f"{order['session_type']} Session • {order['time'].strftime('%I:%M %p')}"
        session_label = ctk.CTkLabel(
            info_frame,
            text=session_text,
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        session_label.pack(anchor="w")
        
        # Right side - Programs count and Status
        status_frame = ctk.CTkFrame(content, fg_color="transparent")
        status_frame.pack(side="right")
        
        # Programs count
        programs_count = len(order.get("items", []))
        completed_count = sum(1 for item in order.get("items", []) if item["status"] == "Completed")
        
        count_frame = ctk.CTkFrame(status_frame, fg_color="#f1f5f9", corner_radius=6)
        count_frame.pack(side="right", padx=(0, 10))
        
        ctk.CTkLabel(
            count_frame,
            text=f"📋 {completed_count}/{programs_count} Programs",
            font=ctk.CTkFont(size=12),
            text_color="#64748b"
        ).pack(padx=10, pady=4)
        
        # Status indicator
        status_colors = {
            "Not Started": ("#f1f5f9", "#64748b", "⭘"),
            "In Progress": ("#ecfdf5", "#059669", "🟢"),
            "Completed": ("#dcfce7", "#16a34a", "✓")
        }
        
        bg_color, text_color, icon = status_colors.get(order["status"])
        status_label = ctk.CTkFrame(
            status_frame,
            fg_color=bg_color,
            corner_radius=6
        )
        status_label.pack(side="right")
        
        ctk.CTkLabel(
            status_label,
            text=f"{icon} {order['status']}",
            font=ctk.CTkFont(size=12),
            text_color=text_color
        ).pack(padx=10, pady=4)
        
    def create_new_order(self):
        dialog = NewOrderDialog(self)
        self.wait_window(dialog.dialog)
        
        if hasattr(dialog, 'result'):
            # Add new order to the list
            self.orders.append(dialog.result)
            # Select the newly created order
            self.select_order(dialog.result)
    
    def update_session_info(self):
        if self.order_data:
            # Clear existing content
            for widget in self.content_frame.winfo_children():
                widget.destroy()
                
            # Recreate content with updated data
            self.create_session_info(self.content_frame)
            self.create_agenda_items(self.content_frame)
            
    def create_session_info(self, parent):
        if not self.order_data:
            return
            
        info_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=15)
        info_frame.pack(fill="x", pady=(0, 30))
        
        # Session details
        details_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        details_frame.pack(fill="x", padx=20, pady=20)
        
        # Left side - Date and Session
        left_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        left_frame.pack(side="left")
        
        ctk.CTkLabel(
            left_frame,
            text=self.order_data["date"].strftime("%A, %B %d, %Y"),
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w")
        
        session_text = f"{self.order_data['session_type']} Session • {self.order_data['time'].strftime('%I:%M %p')}"
        ctk.CTkLabel(
            left_frame,
            text=session_text,
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack(anchor="w")
        
        # Right side - Status
        status_colors = {
            "Not Started": ("#f1f5f9", "#64748b", "⭘"),
            "In Progress": ("#ecfdf5", "#059669", "🟢"),
            "Completed": ("#dcfce7", "#16a34a", "✓")
        }
        
        bg_color, text_color, icon = status_colors.get(self.order_data["status"])
        
        status_frame = ctk.CTkFrame(
            details_frame,
            fg_color=bg_color,
            corner_radius=8
        )
        status_frame.pack(side="right")
        
        ctk.CTkLabel(
            status_frame,
            text=f"{icon} {self.order_data['status']}",
            font=ctk.CTkFont(size=12),
            text_color=text_color
        ).pack(padx=12, pady=6)
        
    def create_agenda_items(self, parent):
        if self.order_data and self.order_data["items"]:
            # Create a container for all agenda items
            agenda_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=15)
            agenda_frame.pack(fill="x", pady=(0, 15))
            
            # Timeline container
            timeline_container = ctk.CTkFrame(agenda_frame, fg_color="transparent")
            timeline_container.pack(fill="x", padx=20, pady=15)
            
            # Main vertical timeline
            timeline = ctk.CTkFrame(timeline_container, fg_color="#e2e8f0", width=2)
            timeline.pack(side="left", fill="y", padx=(4, 0))
            
            # Programs container
            programs_container = ctk.CTkFrame(timeline_container, fg_color="transparent")
            programs_container.pack(side="left", fill="x", expand=True, padx=(20, 0))
            
            # Header with progress
            header_frame = ctk.CTkFrame(programs_container, fg_color="transparent")
            header_frame.pack(fill="x", pady=(0, 15))
            
            ctk.CTkLabel(
                header_frame,
                text="Programs",
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(side="left")
            
            # Progress info
            completed = sum(1 for item in self.order_data["items"] if item["status"] == "Completed")
            total = len(self.order_data["items"])
            
            progress_frame = ctk.CTkFrame(header_frame, fg_color="#f8fafc", corner_radius=6)
            progress_frame.pack(side="right")
            
            ctk.CTkLabel(
                progress_frame,
                text=f"{completed}/{total} Completed",
                font=ctk.CTkFont(size=12),
                text_color="#64748b"
            ).pack(padx=10, pady=4)
            
            # Create items
            for i, item in enumerate(self.order_data["items"]):
                # Item container
                item_frame = ctk.CTkFrame(programs_container, fg_color="transparent")
                item_frame.pack(fill="x", pady=(0, 15 if i < len(self.order_data["items"]) - 1 else 0))
                
                # Time bubble
                bubble_frame = ctk.CTkFrame(item_frame, width=10, height=10)
                bubble_frame.pack(side="left")
                bubble_frame.pack_propagate(False)
                
                bubble = ctk.CTkFrame(
                    bubble_frame,
                    width=10,
                    height=10,
                    corner_radius=5,
                    fg_color="#3949ab" if item["status"] != "Completed" else "#16a34a"
                )
                bubble.place(relx=0.5, rely=0.5, anchor="center")
                
                # Content container
                content = ctk.CTkFrame(item_frame, fg_color="#f8fafc", corner_radius=10)
                content.pack(side="left", fill="x", expand=True, padx=(15, 0))
                
                # Time and duration
                time_frame = ctk.CTkFrame(content, fg_color="transparent")
                time_frame.pack(fill="x", padx=15, pady=(10, 5))
                
                ctk.CTkLabel(
                    time_frame,
                    text=item["time"],
                    font=ctk.CTkFont(size=12),
                    text_color="#64748b"
                ).pack(side="left")
                
                ctk.CTkLabel(
                    time_frame,
                    text=f"• {item['duration']}",
                    font=ctk.CTkFont(size=12),
                    text_color="#64748b"
                ).pack(side="left", padx=(5, 0))
                
                # Title
                ctk.CTkLabel(
                    content,
                    text=item["title"],
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color="#000000"
                ).pack(fill="x", padx=15, pady=(0, 10))
                
                # Status indicator
                status_colors = {
                    "Completed": ("#dcfce7", "#16a34a", "✓"),
                    "In Progress": ("#dbeafe", "#2563eb", "▶"),
                    "Pending": ("#f1f5f9", "#64748b", "○")
                }
                
                status = item["status"]
                bg_color, text_color, icon = status_colors.get(status)
                
                status_button = ctk.CTkButton(
                    content,
                    text=f"{icon} {status}",
                    font=ctk.CTkFont(size=12),
                    text_color=text_color,
                    fg_color=bg_color,
                    hover_color=bg_color,
                    height=28,
                    command=lambda i=item: self.toggle_item_status(i)
                )
                status_button.pack(side="right", padx=15, pady=(0, 10))
        else:
            # Show empty state
            empty_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=15)
            empty_frame.pack(fill="x", pady=(0, 15))
            
            content = ctk.CTkFrame(empty_frame, fg_color="transparent")
            content.pack(fill="x", padx=20, pady=30)
            
            ctk.CTkLabel(
                content,
                text="No Programs Added",
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack()
            
            ctk.CTkLabel(
                content,
                text="Click '+ New Item' to add programs to the order",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            ).pack()

    def toggle_item_status(self, item):
        if self.order_data["status"] != "In Progress":
            return
            
        status_order = ["Pending", "In Progress", "Completed"]
        current_index = status_order.index(item["status"])
        item["status"] = status_order[(current_index + 1) % len(status_order)]
        
        self.update_session_info()

    def add_new_item(self):
        if not self.order_data:
            messagebox.showerror("Error", "Please create an order first")
            return
            
        dialog = AddItemDialog(self, self.current_time)
        self.wait_window(dialog.dialog)
        
        if hasattr(dialog, 'result'):
            # Initialize items list if it doesn't exist
            if "items" not in self.order_data:
                self.order_data["items"] = []
                
            self.order_data["items"].append(dialog.result)
            
            # Update current time for next item
            duration = int(dialog.result["duration"].split()[0])
            self.current_time = (datetime.combine(datetime.today(), self.current_time) + 
                               timedelta(minutes=duration)).time()
            
            # Update the display
            self.update_session_info()
            
    def toggle_session_status(self):
        if not self.order_data:
            messagebox.showerror("Error", "Please create an order first")
            return
            
        if not self.order_data.get("items"):
            messagebox.showerror("Error", "Please add at least one program before starting the session")
            return
            
        if self.order_data["status"] == "Not Started":
            self.order_data["status"] = "In Progress"
            self.status_button.configure(
                text="End Session",
                fg_color="#e11d48",
                hover_color="#be123c"
            )
        elif self.order_data["status"] == "In Progress":
            if messagebox.askyesno("Confirm", "Are you sure you want to end this session?"):
                self.order_data["status"] = "Completed"
                self.status_button.configure(
                    text="Session Ended",
                    state="disabled"
                )
                self.new_item_button.configure(state="disabled")
                self.new_order_button.configure(state="normal")
        
        self.update_session_info() 

    def show_empty_state(self):
        empty_frame = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=15)
        empty_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            empty_frame,
            text="No Orders Created",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(40, 10))
        
        ctk.CTkLabel(
            empty_frame,
            text="Click '+ New Order' to create a new order of the day",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack() 

    def handle_back(self):
        # Reset selected order
        self.selected_order = None
        self.order_data = None
        self.current_time = None
        
        # Reset button states
        self.status_button.configure(
            state="disabled",
            text="Start Session",
            fg_color="#059669"
        )
        self.new_item_button.configure(state="disabled")
        
        # Show orders list
        self.show_orders_list() 

    def create_header(self):
        header_frame = ctk.CTkFrame(
            self,
            fg_color="white",
            height=70,
            corner_radius=0
        )
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title with icon
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left", padx=30)
        
        ctk.CTkLabel(
            title_frame,
            text="📑",
            font=ctk.CTkFont(size=24)
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            title_frame,
            text="Order of the Day",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left")
        
        # Right side buttons
        buttons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        buttons_frame.pack(side="right", padx=30)
        
        # New Order button
        self.new_order_button = ctk.CTkButton(
            buttons_frame,
            text="+ New Order",
            font=ctk.CTkFont(size=12),
            fg_color="#1a237e",
            hover_color="#283593",
            height=35,
            command=self.create_new_order
        )
        self.new_order_button.pack(side="right", padx=5)
        
        # Add New Item button (disabled initially)
        self.new_item_button = ctk.CTkButton(
            buttons_frame,
            text="+ New Item",
            font=ctk.CTkFont(size=12),
            fg_color="#1a237e",
            hover_color="#283593",
            height=35,
            command=self.add_new_item,
            state="disabled"
        )
        self.new_item_button.pack(side="right", padx=5)
        
        # Start/End Session button (disabled initially)
        self.status_button = ctk.CTkButton(
            buttons_frame,
            text="Start Session",
            font=ctk.CTkFont(size=12),
            fg_color="#059669",
            hover_color="#047857",
            height=35,
            command=self.toggle_session_status,
            state="disabled"
        )
        self.status_button.pack(side="right", padx=5)

    def create_content(self):
        self.content_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Show empty state initially
        self.show_empty_state()

    def create_order_card(self, order):
        # Order card container with hover effect
        card = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=15)
        card.pack(fill="x", pady=(0, 15))
        
        # Add hover effect
        def on_enter(e):
            card.configure(fg_color="#f8fafc")
        
        def on_leave(e):
            card.configure(fg_color="white")
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        card.bind("<Button-1>", lambda e, o=order: self.select_order(o))
        
        # Card content
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=15)
        
        # Left side - Date and Session info
        info_frame = ctk.CTkFrame(content, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)
        
        date_label = ctk.CTkLabel(
            info_frame,
            text=order["date"].strftime("%A, %B %d, %Y"),
            font=ctk.CTkFont(size=16, weight="bold")
        )
        date_label.pack(anchor="w")
        
        session_text = f"{order['session_type']} Session • {order['time'].strftime('%I:%M %p')}"
        session_label = ctk.CTkLabel(
            info_frame,
            text=session_text,
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        session_label.pack(anchor="w")
        
        # Right side - Programs count and Status
        status_frame = ctk.CTkFrame(content, fg_color="transparent")
        status_frame.pack(side="right")
        
        # Programs count
        programs_count = len(order.get("items", []))
        completed_count = sum(1 for item in order.get("items", []) if item["status"] == "Completed")
        
        count_frame = ctk.CTkFrame(status_frame, fg_color="#f1f5f9", corner_radius=6)
        count_frame.pack(side="right", padx=(0, 10))
        
        ctk.CTkLabel(
            count_frame,
            text=f"📋 {completed_count}/{programs_count} Programs",
            font=ctk.CTkFont(size=12),
            text_color="#64748b"
        ).pack(padx=10, pady=4)
        
        # Status indicator
        status_colors = {
            "Not Started": ("#f1f5f9", "#64748b", "⭘"),
            "In Progress": ("#ecfdf5", "#059669", "🟢"),
            "Completed": ("#dcfce7", "#16a34a", "✓")
        }
        
        bg_color, text_color, icon = status_colors.get(order["status"])
        status_label = ctk.CTkFrame(
            status_frame,
            fg_color=bg_color,
            corner_radius=6
        )
        status_label.pack(side="right")
        
        ctk.CTkLabel(
            status_label,
            text=f"{icon} {order['status']}",
            font=ctk.CTkFont(size=12),
            text_color=text_color
        ).pack(padx=10, pady=4) 

    def show_order_details(self):
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Back button container
        back_container = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=15)
        back_container.pack(fill="x", pady=(0, 15))
        
        back_frame = ctk.CTkFrame(back_container, fg_color="transparent")
        back_frame.pack(fill="x", padx=20, pady=15)
        
        # Back button with icon
        back_button = ctk.CTkButton(
            back_frame,
            text="← Back to Orders List",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            text_color="#1e293b",
            hover_color="#f1f5f9",
            anchor="w",
            width=120,
            height=32,
            command=self.handle_back
        )
        back_button.pack(side="left")
        
        # Order status on the right
        status_colors = {
            "Not Started": ("#f1f5f9", "#64748b", "⭘"),
            "In Progress": ("#ecfdf5", "#059669", "🟢"),
            "Completed": ("#dcfce7", "#16a34a", "✓")
        }
        
        bg_color, text_color, icon = status_colors.get(self.order_data["status"])
        status_frame = ctk.CTkFrame(
            back_frame,
            fg_color=bg_color,
            corner_radius=6
        )
        status_frame.pack(side="right")
        
        ctk.CTkLabel(
            status_frame,
            text=f"{icon} {self.order_data['status']}",
            font=ctk.CTkFont(size=12),
            text_color=text_color
        ).pack(padx=10, pady=4)
        
        # Session info container
        info_container = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=15)
        info_container.pack(fill="x", pady=(0, 15))
        
        # Session details
        info_frame = ctk.CTkFrame(info_container, fg_color="transparent")
        info_frame.pack(fill="x", padx=20, pady=15)
        
        # Date and time
        date_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        date_frame.pack(fill="x")
        
        ctk.CTkLabel(
            date_frame,
            text=self.order_data["date"].strftime("%A, %B %d, %Y"),
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left")
        
        session_text = f"{self.order_data['session_type']} Session • {self.order_data['time'].strftime('%I:%M %p')}"
        ctk.CTkLabel(
            date_frame,
            text=session_text,
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack(side="right")
        
        # Programs list container
        programs_container = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=15)
        programs_container.pack(fill="both", expand=True)
        
        # Programs header
        header_frame = ctk.CTkFrame(programs_container, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            header_frame,
            text="Programs",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left")
        
        programs_count = len(self.order_data.get("items", []))
        completed_count = sum(1 for item in self.order_data.get("items", []) if item["status"] == "Completed")
        
        count_frame = ctk.CTkFrame(header_frame, fg_color="#f1f5f9", corner_radius=6)
        count_frame.pack(side="right")
        
        ctk.CTkLabel(
            count_frame,
            text=f"📋 {completed_count}/{programs_count} Completed",
            font=ctk.CTkFont(size=12),
            text_color="#64748b"
        ).pack(padx=10, pady=4)
        
        # Programs list
        if self.order_data.get("items"):
            for item in self.order_data["items"]:
                self.create_program_item(programs_container, item)
        else:
            self.show_empty_programs(programs_container)

    def create_program_item(self, parent, item):
        item_frame = ctk.CTkFrame(parent, fg_color="transparent")
        item_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Timeline dot
        dot_frame = ctk.CTkFrame(item_frame, width=12, height=12)
        dot_frame.pack(side="left")
        dot_frame.pack_propagate(False)
        
        dot_colors = {
            "Pending": "#64748b",
            "In Progress": "#3b82f6",
            "Completed": "#10b981"
        }
        
        dot = ctk.CTkFrame(
            dot_frame,
            width=8,
            height=8,
            corner_radius=4,
            fg_color=dot_colors[item["status"]]
        )
        dot.place(relx=0.5, rely=0.5, anchor="center")
        
        # Content container
        content = ctk.CTkFrame(item_frame, fg_color="#f8fafc", corner_radius=10)
        content.pack(side="left", fill="x", expand=True, padx=(15, 0))
        
        # Time and duration
        time_frame = ctk.CTkFrame(content, fg_color="transparent")
        time_frame.pack(fill="x", padx=15, pady=(10, 5))
        
        ctk.CTkLabel(
            time_frame,
            text=item["time"],
            font=ctk.CTkFont(size=12),
            text_color="#64748b"
        ).pack(side="left")
        
        ctk.CTkLabel(
            time_frame,
            text=f"• {item['duration']}",
            font=ctk.CTkFont(size=12),
            text_color="#64748b"
        ).pack(side="left", padx=(5, 0))
        
        # Title
        ctk.CTkLabel(
            content,
            text=item["title"],
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#000000"
        ).pack(fill="x", padx=15, pady=(0, 10))
        
        # Status button
        status_colors = {
            "Pending": ("#f1f5f9", "#64748b", "○"),
            "In Progress": ("#dbeafe", "#2563eb", "▶"),
            "Completed": ("#dcfce7", "#16a34a", "✓")
        }
        
        bg_color, text_color, icon = status_colors[item["status"]]
        status_button = ctk.CTkButton(
            content,
            text=f"{icon} {item['status']}",
            font=ctk.CTkFont(size=12),
            text_color=text_color,
            fg_color=bg_color,
            hover_color=bg_color,
            height=28,
            command=lambda: self.toggle_item_status(item)
        )
        status_button.pack(side="right", padx=15, pady=(0, 10))

    def show_empty_programs(self, parent):
        content = ctk.CTkFrame(parent, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=30)
        
        ctk.CTkLabel(
            content,
            text="No Programs Added",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack()
        
        ctk.CTkLabel(
            content,
            text="Click '+ New Item' to add programs to the order",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack() 