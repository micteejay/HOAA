import customtkinter as ctk
from tkinter import messagebox
from access_control import AccessControl

class ScrollableDialog:
    def __init__(self, parent, title, width=600, height=700):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry(f"{width}x{height}")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Make dialog scrollable
        self.main_frame = ctk.CTkScrollableFrame(
            self.dialog,
            fg_color="transparent"
        )
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

class AttendanceDialog(ScrollableDialog):
    def __init__(self, parent):
        super().__init__(parent, "Manage Attendance", width=800, height=600)
        self.parent = parent
        self.data_manager = parent.data_manager
        self.create_dialog_content()
        
    def create_dialog_content(self):
        # Title
        ctk.CTkLabel(
            self.main_frame,
            text="Session Attendance",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(0, 20))
        
        # Session selector
        selector_frame = ctk.CTkFrame(self.main_frame, fg_color="white", corner_radius=15)
        selector_frame.pack(fill="x", pady=(0, 20))
        
        # Get sessions from data manager
        sessions = self.data_manager.get_upcoming_sessions()
        
        if sessions:
            # Create session dropdown
            self.session_var = ctk.StringVar(value=sessions[0]["title"])
            
            ctk.CTkLabel(
                selector_frame,
                text="Select Session:",
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(side="left", padx=20, pady=15)
            
            self.session_menu = ctk.CTkOptionMenu(
                selector_frame,
                values=[s["title"] for s in sessions],
                variable=self.session_var,
                font=ctk.CTkFont(size=14),
                fg_color="#1a237e",
                button_color="#283593",
                button_hover_color="#1e40af",
                command=self.show_attendance
            )
            self.session_menu.pack(side="left", padx=20, pady=15)
            
        # Attendance list
        self.attendance_frame = ctk.CTkFrame(self.main_frame, fg_color="white", corner_radius=15)
        self.attendance_frame.pack(fill="both", expand=True, pady=20)
        
        # Show initial attendance list
        self.show_attendance()
        
    def show_attendance(self, *args):
        # Clear current attendance list
        for widget in self.attendance_frame.winfo_children():
            widget.destroy()
            
        # Create headers
        headers = ctk.CTkFrame(self.attendance_frame, fg_color="transparent")
        headers.pack(fill="x", padx=20, pady=15)
        
        for header in ["Member", "Status", "Time", "Actions"]:
            ctk.CTkLabel(
                headers,
                text=header,
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(side="left", expand=True) 

class AdminAccessControlDialog(ScrollableDialog):
    def __init__(self, parent):
        super().__init__(parent, "Manage Access Levels", width=800, height=700)
        self.parent = parent
        self.data_manager = parent.data_manager
        self.create_dialog_content()
        
    def create_dialog_content(self):
        # Title
        ctk.CTkLabel(
            self.main_frame,
            text="Configure Access Levels",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(0, 20))
        
        # All available pages
        self.all_pages = [
            "Dashboard", "Order Paper", "Order of the Day", "Petitions",
            "Chat", "Voting", "Motions", "Documents", "Admin",
            "Vote Results", "System Logs", "User Management", "Backup & Restore"
        ]
        
        # Create sections for each access level
        for level, data in AccessControl.ACCESS_LEVELS.items():
            self.create_access_level_section(level, data)
            
        # Save button
        ctk.CTkButton(
            self.main_frame,
            text="Save Changes",
            font=ctk.CTkFont(size=14),
            fg_color="#1a237e",
            hover_color="#283593",
            command=self.save_changes
        ).pack(pady=20)
        
    def create_access_level_section(self, level, data):
        # Section frame
        section = ctk.CTkFrame(self.main_frame, fg_color="white", corner_radius=15)
        section.pack(fill="x", pady=10, padx=5)
        
        # Header
        header = ctk.CTkFrame(section, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            header,
            text=level,
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left")
        
        # Roles text
        roles_text = ", ".join(data["roles"])
        ctk.CTkLabel(
            header,
            text=f"Roles: {roles_text}",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(side="right")
        
        # Pages selection
        pages_frame = ctk.CTkFrame(section, fg_color="transparent")
        pages_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Create checkboxes for each page
        self.page_vars = {}
        for i, page in enumerate(self.all_pages):
            row = i // 3
            col = i % 3
            
            if not hasattr(self, f'vars_{level}'):
                setattr(self, f'vars_{level}', {})
            
            var = ctk.BooleanVar(value=page in data.get("pages", []))
            getattr(self, f'vars_{level}')[page] = var
            
            checkbox = ctk.CTkCheckBox(
                pages_frame,
                text=page,
                variable=var,
                font=ctk.CTkFont(size=12),
                fg_color="#1a237e",
                hover_color="#283593"
            )
            checkbox.grid(row=row, column=col, padx=10, pady=5, sticky="w")
            
        # Configure grid columns
        for i in range(3):
            pages_frame.grid_columnconfigure(i, weight=1)
            
    def save_changes(self):
        # Collect new settings
        new_settings = {}
        for level in AccessControl.ACCESS_LEVELS.keys():
            new_settings[level] = {
                "roles": AccessControl.ACCESS_LEVELS[level]["roles"],
                "pages": [
                    page for page in self.all_pages
                    if getattr(self, f'vars_{level}')[page].get()
                ]
            }
            
            # Preserve any additional settings like permissions
            if "permissions" in AccessControl.ACCESS_LEVELS[level]:
                new_settings[level]["permissions"] = AccessControl.ACCESS_LEVELS[level]["permissions"]
        
        # Update AccessControl
        AccessControl.ACCESS_LEVELS.update(new_settings)
        
        # Save to configuration file
        self.data_manager.save_access_levels(new_settings)
        
        messagebox.showinfo("Success", "Access levels updated successfully")
        self.dialog.destroy() 

class ManageUserAccessDialog(ScrollableDialog):
    def __init__(self, parent, user_data):
        super().__init__(parent, f"Manage Access - {user_data['username']}")
        self.parent = parent
        self.data_manager = parent.data_manager
        self.user_data = user_data
        self.create_dialog_content()
        
    def create_dialog_content(self):
        # User info header
        info_frame = ctk.CTkFrame(self.main_frame, fg_color="white", corner_radius=15)
        info_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            info_frame,
            text=f"User: {self.user_data['username']}",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        ctk.CTkLabel(
            info_frame,
            text=f"Role: {self.user_data['role']}",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(0, 10))
        
        # Page access selection
        access_frame = ctk.CTkFrame(self.main_frame, fg_color="white", corner_radius=15)
        access_frame.pack(fill="both", expand=True)
        
        # Available pages
        pages_frame = ctk.CTkFrame(access_frame, fg_color="transparent")
        pages_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.available_pages = [
            "Dashboard", "Order Paper", "Order of the Day", "Petitions",
            "Chat", "Voting", "Motions", "Documents", "Admin",
            "Vote Results", "System Logs", "User Management", "Backup & Restore"
        ]
        
        # Create checkboxes for each page
        self.page_vars = {}
        for i, page in enumerate(self.available_pages):
            row = i // 3
            col = i % 3
            
            var = ctk.BooleanVar(value=page in self.user_data.get('permitted_pages', []))
            self.page_vars[page] = var
            
            checkbox = ctk.CTkCheckBox(
                pages_frame,
                text=page,
                variable=var,
                font=ctk.CTkFont(size=12),
                fg_color="#1a237e",
                hover_color="#283593"
            )
            checkbox.grid(row=row, column=col, padx=10, pady=5, sticky="w")
            
        # Configure grid columns
        for i in range(3):
            pages_frame.grid_columnconfigure(i, weight=1)
            
        # Save button
        ctk.CTkButton(
            self.main_frame,
            text="Save Changes",
            font=ctk.CTkFont(size=14),
            fg_color="#1a237e",
            hover_color="#283593",
            command=self.save_changes
        ).pack(pady=20)
        
    def save_changes(self):
        # Get selected pages
        permitted_pages = [
            page for page, var in self.page_vars.items()
            if var.get()
        ]
        
        # Update user's permitted pages
        self.data_manager.update_user_access(
            self.user_data['username'],
            permitted_pages
        )
        
        messagebox.showinfo("Success", "User access updated successfully")
        self.dialog.destroy() 