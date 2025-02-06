import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from datepicker import DatePicker

class TimePickerDialog(ctk.CTkToplevel):
    def __init__(self, parent, selected_time=None):
        super().__init__(parent)
        self.title("Select Time")
        self.geometry("250x300")
        self.resizable(False, False)
        
        # Center dialog
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')
        
        self.callback = None
        self.selected_time = selected_time or datetime.now()
        
        self.create_time_picker()
        
    def create_time_picker(self):
        # Create main container
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Hour selector
        hour_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        hour_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            hour_frame,
            text="Hour:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w")
        
        self.hour_var = ctk.StringVar(value=str(self.selected_time.hour).zfill(2))
        hours = [str(i).zfill(2) for i in range(24)]
        
        hour_menu = ctk.CTkOptionMenu(
            hour_frame,
            values=hours,
            variable=self.hour_var,
            width=200
        )
        hour_menu.pack(fill="x")
        
        # Minute selector
        minute_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        minute_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            minute_frame,
            text="Minute:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w")
        
        self.minute_var = ctk.StringVar(value=str(self.selected_time.minute).zfill(2))
        minutes = [str(i).zfill(2) for i in range(60)]
        
        minute_menu = ctk.CTkOptionMenu(
            minute_frame,
            values=minutes,
            variable=self.minute_var,
            width=200
        )
        minute_menu.pack(fill="x")
        
        # Buttons
        buttons = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons.pack(fill="x", pady=(20, 0))
        
        ctk.CTkButton(
            buttons,
            text="Select",
            command=self.select_time
        ).pack(side="left", expand=True, padx=5)
        
        ctk.CTkButton(
            buttons,
            text="Cancel",
            command=self.cancel
        ).pack(side="left", expand=True, padx=5)
        
    def select_time(self):
        hour = int(self.hour_var.get())
        minute = int(self.minute_var.get())
        selected_time = self.selected_time.replace(hour=hour, minute=minute)
        
        if self.callback:
            self.callback(selected_time)
        self.destroy()
        
    def cancel(self):
        self.destroy()
        
    def get_time(self, callback):
        self.callback = callback
        self.grab_set()
        self.wait_window()

class ScheduleSessionDialog:
    def __init__(self, parent):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Schedule Session")
        self.dialog.geometry("500x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Store parent reference and data manager
        self.parent = parent
        self.data_manager = parent.data_manager  # Get data_manager directly
        
        # Center dialog
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'+{x}+{y}')
        
        self.create_dialog_content()
        
    def create_dialog_content(self):
        # Title
        ctk.CTkLabel(
            self.dialog,
            text="Session Details",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)
        
        # Form container
        form = ctk.CTkFrame(self.dialog, fg_color="transparent")
        form.pack(fill="x", padx=20)
        
        # Session Title
        ctk.CTkLabel(
            form,
            text="Session Title:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w")
        
        self.title_var = ctk.StringVar()
        ctk.CTkEntry(
            form,
            textvariable=self.title_var,
            height=35
        ).pack(fill="x", pady=(5, 15))
        
        # Date and Time
        date_time = ctk.CTkFrame(form, fg_color="transparent")
        date_time.pack(fill="x")
        
        # Date picker
        date_frame = ctk.CTkFrame(date_time, fg_color="transparent")
        date_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(
            date_frame,
            text="Date:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w")
        
        date_input = ctk.CTkFrame(date_frame, fg_color="transparent")
        date_input.pack(fill="x", pady=(5, 15))
        
        self.date_var = ctk.StringVar()
        self.date_entry = ctk.CTkEntry(
            date_input,
            textvariable=self.date_var,
            height=35,
            placeholder_text="YYYY-MM-DD"
        )
        self.date_entry.pack(side="left", fill="x", expand=True)
        
        # Date picker button
        ctk.CTkButton(
            date_input,
            text="📅",
            width=40,
            command=self.show_date_picker
        ).pack(side="left", padx=(5, 0))
        
        # Time input
        time_frame = ctk.CTkFrame(date_time, fg_color="transparent")
        time_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            time_frame,
            text="Time:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w")
        
        time_input = ctk.CTkFrame(time_frame, fg_color="transparent")
        time_input.pack(fill="x", pady=(5, 15))
        
        self.time_var = ctk.StringVar()
        self.time_entry = ctk.CTkEntry(
            time_input,
            textvariable=self.time_var,
            height=35,
            placeholder_text="HH:MM"
        )
        self.time_entry.pack(side="left", fill="x", expand=True)
        
        # Time picker button
        ctk.CTkButton(
            time_input,
            text="🕒",
            width=40,
            command=self.show_time_picker
        ).pack(side="left", padx=(5, 0))
        
        # Session Type
        ctk.CTkLabel(
            form,
            text="Session Type:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w")
        
        self.session_type = ctk.StringVar(value="Regular")
        types_frame = ctk.CTkFrame(form, fg_color="transparent")
        types_frame.pack(fill="x", pady=(5, 15))
        
        session_types = ["Regular", "Special", "Emergency", "Committee"]
        for stype in session_types:
            ctk.CTkRadioButton(
                types_frame,
                text=stype,
                variable=self.session_type,
                value=stype,
                font=ctk.CTkFont(size=12)
            ).pack(side="left", padx=10)
        
        # Agenda Items
        ctk.CTkLabel(
            form,
            text="Agenda Items:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w")
        
        self.agenda_text = ctk.CTkTextbox(
            form,
            height=150
        )
        self.agenda_text.pack(fill="x", pady=(5, 20))
        
        # Buttons
        buttons = ctk.CTkFrame(self.dialog, fg_color="transparent")
        buttons.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(
            buttons,
            text="Schedule",
            font=ctk.CTkFont(size=14),
            fg_color="#1a237e",
            hover_color="#283593",
            command=self.schedule_session
        ).pack(side="left", expand=True, padx=5)
        
        ctk.CTkButton(
            buttons,
            text="Cancel",
            font=ctk.CTkFont(size=14),
            fg_color="#dc2626",
            hover_color="#b91c1c",
            command=self.dialog.destroy
        ).pack(side="left", expand=True, padx=5)
        
    def show_date_picker(self):
        def on_date_selected(date):
            self.date_var.set(date.strftime("%Y-%m-%d"))
            
        current_date = None
        try:
            if self.date_var.get():
                current_date = datetime.strptime(self.date_var.get(), "%Y-%m-%d")
        except:
            current_date = None
            
        date_picker = DatePicker(self.dialog, selected_date=current_date)
        date_picker.get_date(on_date_selected)
        
    def show_time_picker(self):
        def on_time_selected(time):
            self.time_var.set(time.strftime("%H:%M"))
            
        current_time = None
        try:
            if self.time_var.get():
                current_time = datetime.strptime(self.time_var.get(), "%H:%M")
        except:
            current_time = None
            
        time_picker = TimePickerDialog(self.dialog, selected_time=current_time)
        time_picker.get_time(on_time_selected)
        
    def schedule_session(self):
        # Validate inputs
        if not self.title_var.get().strip():
            messagebox.showerror("Error", "Please enter a session title")
            return
            
        try:
            date = datetime.strptime(self.date_var.get(), "%Y-%m-%d")
            time = datetime.strptime(self.time_var.get(), "%H:%M")
        except ValueError:
            messagebox.showerror("Error", "Invalid date or time format")
            return
            
        if not self.agenda_text.get("1.0", "end-1c").strip():
            messagebox.showerror("Error", "Please enter agenda items")
            return
            
        # Save session details
        try:
            session_data = {
                "title": self.title_var.get().strip(),
                "date": self.date_var.get(),
                "time": self.time_var.get(),
                "type": self.session_type.get(),
                "agenda": self.agenda_text.get("1.0", "end-1c").strip()
            }
            
            # Add session through data manager
            session_id = self.data_manager.add_session(session_data)  # Use data_manager directly
            
            # Update dashboard if available
            if hasattr(self.parent, "update_dashboard"):
                self.parent.update_dashboard()
                
            messagebox.showinfo("Success", "Session scheduled successfully")
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to schedule session: {str(e)}") 