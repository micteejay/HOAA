import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime
import json
import os
import csv
import shutil
from dialogs import AttendanceDialog, ScrollableDialog, AdminAccessControlDialog, ManageUserAccessDialog
from schedule_session import ScheduleSessionDialog

class AdminContent(ctk.CTkFrame):
    def __init__(self, parent, current_user, is_admin=False):
        super().__init__(parent)
        
        if not is_admin:
            self.show_access_denied()
            return
            
        # Store user info and parent reference
        self.parent = parent
        self.current_user = current_user
        self.is_admin = is_admin
        self.data_manager = parent.data_manager
        
        # Configure frame
        self.configure(fg_color="#f1f5f9")
        
        # Use grid instead of pack
        self.grid(row=0, column=1, sticky="nsew")
        
        # Create UI sections
        self.create_header()
        
        # Create scrollable content area
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.scrollable_frame.pack(fill="both", expand=True)
        
        # Create content in scrollable frame
        self.create_content()
        
    def show_access_denied(self):
        self.configure(fg_color="#f1f5f9")
        
        # Create centered message
        message_frame = ctk.CTkFrame(self, fg_color="transparent")
        message_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(
            message_frame,
            text="⚠️",
            font=ctk.CTkFont(size=48)
        ).pack()
        
        ctk.CTkLabel(
            message_frame,
            text="Access Denied",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#dc2626"
        ).pack(pady=(10, 5))
        
        ctk.CTkLabel(
            message_frame,
            text="You don't have permission to access this page",
            font=ctk.CTkFont(size=14),
            text_color="#000000"
        ).pack()
        
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
            text="⚙️",
            font=ctk.CTkFont(size=24)
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            title_frame,
            text="Admin Dashboard",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#000000"
        ).pack(side="left")
        
    def create_content(self):
        content_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Create sections grid
        sections = [
            {
                "title": "User Management",
                "icon": "👥",
                "color": "#818cf8",
                "items": [
                    ("Add New User", self.add_user),
                    ("Manage Roles", self.manage_roles),
                    ("View All Users", self.view_users)
                ]
            },
            {
                "title": "Session Management",
                "icon": "📅",
                "color": "#e0e7ff",
                "items": [
                    ("Schedule Session", self.schedule_session),
                    ("Manage Attendance", self.manage_attendance),
                    ("Session Reports", self.view_reports)
                ]
            },
            {
                "title": "Pending Approvals",
                "icon": "⏳",
                "color": "#fef3c7",
                "items": [
                    ("Review Motions", self.review_motions),
                    ("Review Votes", self.review_votes)
                ]
            },
            {
                "title": "Document Control",
                "icon": "📄",
                "color": "#34d399",
                "items": [
                    ("Review Documents", self.review_documents),
                    ("Archive Management", self.manage_archives),
                    ("Access Control", self.manage_doc_access)
                ]
            },
            {
                "title": "System Settings",
                "icon": "⚙️",
                "color": "#f59e0b",
                "items": [
                    ("General Settings", self.general_settings),
                    ("Backup & Restore", self.backup_restore),
                    ("System Logs", self.view_logs)
                ]
            }
        ]
        
        for i, section in enumerate(sections):
            row = i // 2
            col = i % 2
            
            self.create_admin_section(content_frame, section, row, col)
            content_frame.grid_columnconfigure(col, weight=1)
            
    def create_admin_section(self, parent, section, row, col):
        section_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=15)
        section_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Header with icon
        header = ctk.CTkFrame(section_frame, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=15)
        
        icon_frame = ctk.CTkFrame(
            header,
            fg_color=section["color"],
            width=40,
            height=40,
            corner_radius=8
        )
        icon_frame.pack(side="left")
        icon_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            icon_frame,
            text=section["icon"],
            font=ctk.CTkFont(size=20)
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(
            header,
            text=section["title"],
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#000000"
        ).pack(side="left", padx=(15, 0))
        
        # Action buttons
        for text, command in section["items"]:
            button = ctk.CTkButton(
                section_frame,
                text=text,
                font=ctk.CTkFont(size=12),
                fg_color="transparent",
                text_color="#000000",
                hover_color="#f1f5f9",
                anchor="w",
                height=35,
                command=command
            )
            button.pack(fill="x", padx=20, pady=5) 

    # User Management Functions
    def add_user(self):
        dialog = AddUserDialog(self)
        self.wait_window(dialog.dialog)
        
    def manage_roles(self):
        dialog = ManageRolesDialog(self)
        self.wait_window(dialog.dialog)
        
    def view_users(self):
        dialog = ViewUsersDialog(self)
        self.wait_window(dialog.dialog)

    # Session Management Functions
    def schedule_session(self):
        dialog = ScheduleSessionDialog(self)
        dialog.parent = self  # Pass self as parent which now has data_manager
        self.wait_window(dialog.dialog)
        
    def manage_attendance(self):
        dialog = AttendanceDialog(self)
        self.wait_window(dialog.dialog)
        
    def view_reports(self):
        dialog = SessionReportsDialog(self)
        self.wait_window(dialog.dialog)

    # Document Control Functions
    def review_documents(self):
        dialog = ReviewDocumentsDialog(self)
        self.wait_window(dialog.dialog)
        
    def manage_archives(self):
        dialog = ArchiveManagementDialog(self)
        self.wait_window(dialog.dialog)
        
    def manage_doc_access(self):
        dialog = DocumentAccessDialog(self)
        self.wait_window(dialog.dialog)

    # System Settings Functions
    def general_settings(self):
        dialog = GeneralSettingsDialog(self)
        self.wait_window(dialog.dialog)
        
    def backup_restore(self):
        dialog = BackupRestoreDialog(self)
        self.wait_window(dialog.dialog)
        
    def view_logs(self):
        dialog = SystemLogsDialog(self)
        self.wait_window(dialog.dialog)

    def review_motions(self):
        dialog = ReviewMotionsDialog(self)
        self.wait_window(dialog.dialog)

    def review_votes(self):
        dialog = ReviewVotesDialog(self)
        self.wait_window(dialog.dialog)

    def manage_access_levels(self):
        dialog = AdminAccessControlDialog(self)
        self.wait_window(dialog.dialog)

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

class AddUserDialog(ScrollableDialog):
    def __init__(self, parent):
        super().__init__(parent, "Add New User")
        self.parent = parent
        self.data_manager = parent.data_manager
        
        # Personal Information Section
        self.create_section_header("Personal Information")
        
        # Full Name
        self.create_field("Full Name:", "full_name")
        
        # Email
        self.create_field("Email:", "email")
        
        # Phone
        self.create_field("Phone:", "phone")
        
        # Position Selection
        self.create_position_selector()
        
        # Account Settings Section
        self.create_section_header("Account Settings")
        
        # Username
        self.create_field("Username:", "username")
        
        # Password
        self.create_field("Password:", "password", show="•")
        
        # Page Access Selection
        self.create_page_access_selector()
        
        # Buttons
        self.create_buttons()
        
    def create_page_access_selector(self):
        # Available pages section
        self.create_section_header("Page Access")
        
        pages_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        pages_frame.pack(fill="x", pady=(0, 15))
        
        # All available pages
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
            
            var = ctk.BooleanVar(value=False)
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
        
    def create_position_selector(self):
        positions = [
            "Speaker",
            "Deputy Speaker",
            "Majority Leader",
            "Deputy Majority Leader",
            "Minority Leader",
            "Deputy Minority Leader",
            "Majority Whip",
            "Deputy Majority Whip",
            "Minority Whip",
            "Deputy Minority Whip",
            "Committee Chair",
            "Deputy Committee Chair",
            "Clerk",
            "Deputy Clerk",
            "Sergeant-at-Arms",
            "Deputy Sergeant-at-Arms",
            "Legal Adviser",
            "Deputy Legal Adviser",
            "Public Relations Officer",
            "Deputy Public Relations Officer",
            "ICT Officer"
        ]
        
        # Position Label
        ctk.CTkLabel(
            self.main_frame,
            text="Position:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", pady=(10, 5))
        
        # Position Dropdown
        self.position_var = ctk.StringVar(value=positions[0])
        position_menu = ctk.CTkOptionMenu(
            self.main_frame,
            values=positions,
            variable=self.position_var,
            width=300,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="#1a237e",
            button_color="#283593",
            button_hover_color="#1e40af"
        )
        position_menu.pack(fill="x", pady=(0, 15))
        
    def create_access_selector(self):
        access_levels = {
            "Full Access": [
                "Speaker",
                "Clerk"
            ],
            "Administrative": [
                "Deputy Speaker",
                "Deputy Clerk",
                "ICT Officer"
            ],
            "Legislative": [
                "Majority Leader",
                "Deputy Majority Leader",
                "Minority Leader",
                "Deputy Minority Leader"
            ],
            "Committee": [
                "Committee Chair",
                "Deputy Committee Chair"
            ],
            "Support": [
                "Legal Adviser",
                "Deputy Legal Adviser",
                "Public Relations Officer",
                "Deputy Public Relations Officer"
            ],
            "Security": [
                "Sergeant-at-Arms",
                "Deputy Sergeant-at-Arms"
            ]
        }
        
        # Access Level Label
        ctk.CTkLabel(
            self.main_frame,
            text="Access Level:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", pady=(10, 5))
        
        # Access Level Frame
        access_frame = ctk.CTkFrame(self.main_frame, fg_color="white", corner_radius=10)
        access_frame.pack(fill="x", pady=(0, 15))
        
        # Create checkboxes for access levels
        self.access_vars = {}
        for level in access_levels.keys():
            var = ctk.BooleanVar(value=False)
            self.access_vars[level] = var
            
            checkbox = ctk.CTkCheckBox(
                access_frame,
                text=level,
                variable=var,
                font=ctk.CTkFont(size=14),
                fg_color="#1a237e",
                hover_color="#283593"
            )
            checkbox.pack(anchor="w", padx=20, pady=5)
        
    def create_section_header(self, text):
        ctk.CTkLabel(
            self.main_frame,
            text=text,
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", pady=(20, 10))
        
    def create_field(self, label, var_name, show=None):
        # Label
        ctk.CTkLabel(
            self.main_frame,
            text=label,
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", pady=(10, 5))
        
        # Entry
        entry = ctk.CTkEntry(
            self.main_frame,
            height=40,
            show=show
        )
        entry.pack(fill="x", pady=(0, 10))
        setattr(self, var_name, entry)
        
    def create_role_selector(self):
        # Role Selection
        ctk.CTkLabel(
            self.main_frame,
            text="Role:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", pady=(10, 5))
        
        self.role_var = ctk.StringVar(value="Member")
        roles = ["Member", "Admin", "Staff"]
        
        role_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        role_frame.pack(fill="x", pady=(0, 20))
        
        for role in roles:
            ctk.CTkRadioButton(
                role_frame,
                text=role,
                variable=self.role_var,
                value=role,
                font=ctk.CTkFont(size=14)
            ).pack(side="left", padx=20)
            
    def create_buttons(self):
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(20, 0))
        
        # Cancel Button
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            font=ctk.CTkFont(size=14),
            fg_color="#dc2626",
            hover_color="#b91c1c",
            command=self.dialog.destroy
        ).pack(side="right", padx=5)
        
        # Save Button
        ctk.CTkButton(
            button_frame,
            text="Save",
            font=ctk.CTkFont(size=14),
            fg_color="#1a237e",
            hover_color="#283593",
            command=self.save_user
        ).pack(side="right", padx=5)
        
    def save_user(self):
        # Add your save logic here
        pass

class ManageRolesDialog:
    def __init__(self, parent):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Manage Roles")
        self.dialog.geometry("800x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'+{x}+{y}')
        
        # Load users
        self.load_users()
        self.create_dialog_content()
        
    def load_users(self):
        try:
            with open("data/users.json", 'r') as f:
                self.users = json.load(f)
        except:
            self.users = []
            
    def create_dialog_content(self):
        # Create main container
        main_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header = ctk.CTkFrame(main_frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            header,
            text="User Roles",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#000000"
        ).pack(side="left")
        
        # Users list
        list_frame = ctk.CTkScrollableFrame(main_frame, fg_color="white", corner_radius=10)
        list_frame.pack(fill="both", expand=True)
        
        # Column headers
        headers_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        headers_frame.pack(fill="x", padx=15, pady=10)
        
        headers = ["Name", "Username", "Current Role", "New Role", ""]
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                headers_frame,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#000000"
            ).pack(side="left", expand=True)
            
        # User rows
        for user in self.users:
            self.create_user_row(list_frame, user)
            
    def create_user_row(self, parent, user):
        row = ctk.CTkFrame(parent, fg_color="transparent", height=50)
        row.pack(fill="x", padx=15, pady=5)
        row.pack_propagate(False)
        
        # Name
        ctk.CTkLabel(
            row,
            text=user["name"],
            font=ctk.CTkFont(size=12),
            text_color="#000000"
        ).pack(side="left", expand=True)
        
        # Username
        ctk.CTkLabel(
            row,
            text=user["username"],
            font=ctk.CTkFont(size=12),
            text_color="#000000"
        ).pack(side="left", expand=True)
        
        # Current Role
        current_role = ctk.CTkFrame(row, fg_color="#e0e7ff", corner_radius=15)
        current_role.pack(side="left", expand=True)
        
        ctk.CTkLabel(
            current_role,
            text=user["role"],
            font=ctk.CTkFont(size=12),
            text_color="#1e40af"
        ).pack(padx=10, pady=5)
        
        # New Role Selection
        roles = ["Member", "Admin", "Clerk", "Speaker"]
        role_var = ctk.StringVar(value=user["role"])
        
        role_menu = ctk.CTkOptionMenu(
            row,
            values=roles,
            variable=role_var,
            font=ctk.CTkFont(size=12),
            fg_color="#1a237e",
            button_color="#283593",
            button_hover_color="#1e40af",
            width=120,
            command=lambda u=user, r=role_var: self.update_role(u, r)
        ).pack(side="left", expand=True)
        
    def update_role(self, user, role_var):
        try:
            new_role = role_var.get()
            if new_role != user["role"]:
                # Update user's role
                user["role"] = new_role
                
                # Save changes
                with open("data/users.json", 'w') as f:
                    json.dump(self.users, f, indent=4)
                    
                messagebox.showinfo(
                    "Success", 
                    f"Role updated for {user['name']} to {new_role}"
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update role: {str(e)}")

class ViewUsersDialog(ScrollableDialog):
    def __init__(self, parent):
        super().__init__(parent, "View Users", width=1000, height=700)
        self.parent = parent
        self.data_manager = parent.data_manager
        
        # Load users
        self.load_users()
        self.create_dialog_content()
        
    def load_users(self):
        try:
            with open("data/users.json", 'r') as f:
                self.users = json.load(f)
        except:
            self.users = []
            
    def create_dialog_content(self):
        # Create main container
        main_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header with search
        header = ctk.CTkFrame(main_frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            header,
            text="All Users",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#000000"
        ).pack(side="left")
        
        # Search box
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self.filter_users)
        
        search_frame = ctk.CTkFrame(header, fg_color="#f1f5f9", corner_radius=20)
        search_frame.pack(side="right")
        
        ctk.CTkLabel(
            search_frame,
            text="🔍",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=(10, 0))
        
        ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Search users...",
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            border_width=0,
            width=200
        ).pack(side="left", padx=10, pady=5)
        
        # Users list
        self.list_frame = ctk.CTkScrollableFrame(main_frame, fg_color="white", corner_radius=10)
        self.list_frame.pack(fill="both", expand=True)
        
        self.show_users()
        
    def show_users(self, users=None):
        # Clear current list
        for widget in self.list_frame.winfo_children():
            widget.destroy()
            
        # Show users
        users = users or self.users
        for user in users:
            self.create_user_card(user)
            
    def create_user_card(self, user):
        card = ctk.CTkFrame(self.list_frame, fg_color="white", corner_radius=15)
        card.pack(fill="x", pady=(0, 15))
        
        # User info
        info_frame = ctk.CTkFrame(card, fg_color="#f8fafc", corner_radius=10)
        info_frame.pack(fill="x")
        
        # Header with name and role
        header = ctk.CTkFrame(info_frame, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=10)
        
        name_frame = ctk.CTkFrame(header, fg_color="transparent")
        name_frame.pack(side="left")
        
        ctk.CTkLabel(
            name_frame,
            text=user["name"],
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#000000"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            name_frame,
            text=user["position"] or "No position set",
            font=ctk.CTkFont(size=12),
            text_color="#64748b"
        ).pack(anchor="w")
        
        role_frame = ctk.CTkFrame(header, fg_color="#e0e7ff", corner_radius=15)
        role_frame.pack(side="right")
        
        ctk.CTkLabel(
            role_frame,
            text=user["role"],
            font=ctk.CTkFont(size=12),
            text_color="#1e40af"
        ).pack(padx=10, pady=5)
        
        # Contact info
        contact = ctk.CTkFrame(info_frame, fg_color="transparent")
        contact.pack(fill="x", padx=15, pady=(0, 10))
        
        if user.get("email"):
            email_frame = ctk.CTkFrame(contact, fg_color="transparent")
            email_frame.pack(side="left", padx=(0, 20))
            
            ctk.CTkLabel(
                email_frame,
                text="✉️",
                font=ctk.CTkFont(size=12)
            ).pack(side="left", padx=(0, 5))
            
            ctk.CTkLabel(
                email_frame,
                text=user["email"],
                font=ctk.CTkFont(size=12),
                text_color="#64748b"
            ).pack(side="left")
            
        if user.get("phone"):
            phone_frame = ctk.CTkFrame(contact, fg_color="transparent")
            phone_frame.pack(side="left")
            
            ctk.CTkLabel(
                phone_frame,
                text="📱",
                font=ctk.CTkFont(size=12)
            ).pack(side="left", padx=(0, 5))
            
            ctk.CTkLabel(
                phone_frame,
                text=user["phone"],
                font=ctk.CTkFont(size=12),
                text_color="#64748b"
            ).pack(side="left")
            
        # Create buttons frame
        buttons_frame = ctk.CTkFrame(card, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(
            buttons_frame,  # Changed from buttons to buttons_frame
            text="Manage Access",
            font=ctk.CTkFont(size=12),
            fg_color="#1a237e",
            hover_color="#283593",
            command=lambda: self.manage_user_access(user)
        ).pack(side="left", padx=5)
        
    def manage_user_access(self, user):
        dialog = ManageUserAccessDialog(self.parent, user)
        self.wait_window(dialog.dialog)
            
    def filter_users(self, *args):
        search_term = self.search_var.get().lower()
        if not search_term:
            self.show_users()
            return
            
        filtered_users = [
            user for user in self.users
            if search_term in user["name"].lower() or
               search_term in user["username"].lower() or
               search_term in user.get("email", "").lower() or
               search_term in user.get("position", "").lower()
        ]
        
        self.show_users(filtered_users) 

class SessionReportsDialog(ScrollableDialog):
    def __init__(self, parent):
        super().__init__(parent, "Session Reports", width=1000, height=700)
        self.parent = parent
        self.data_manager = parent.data_manager
        
        # Get sessions data
        self.sessions = self.data_manager.get_sessions()
        
        self.create_dialog_content()
            
    def create_dialog_content(self):
        # Title
        ctk.CTkLabel(
            self.main_frame,
            text="Session Reports & Analytics",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(0, 20))
        
        # Create tabs
        tabview = ctk.CTkTabview(self.main_frame)
        tabview.pack(fill="both", expand=True)
        
        # Add tabs
        summary_tab = tabview.add("Summary")
        attendance_tab = tabview.add("Attendance")
        analytics_tab = tabview.add("Analytics")
        
        # Create content for each tab
        self.create_summary_tab(summary_tab)
        self.create_attendance_tab(attendance_tab)
        self.create_analytics_tab(analytics_tab)
        
    def create_summary_tab(self, parent):
        # Sessions list
        sessions_frame = ctk.CTkScrollableFrame(
            parent,
            fg_color="transparent"
        )
        sessions_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        if not self.sessions:
            self.show_empty_state(sessions_frame)
            return
            
        # Sort sessions by date
        sorted_sessions = sorted(
            self.sessions,
            key=lambda x: datetime.strptime(str(x["date"]), "%Y-%m-%d"),
            reverse=True
        )
        
        for session in sorted_sessions:
            self.create_session_card(sessions_frame, session)
            
    def create_session_card(self, parent, session):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=15)
        card.pack(fill="x", pady=(0, 15))
        
        # Session info
        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(fill="x", padx=20, pady=15)
        
        # Date and type
        header = ctk.CTkFrame(info, fg_color="transparent")
        header.pack(fill="x")
        
        session_date = datetime.strptime(session["date"], "%Y-%m-%d")
        date_str = session_date.strftime("%B %d, %Y")
        
        ctk.CTkLabel(
            header,
            text=date_str,
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left")
        
        type_frame = ctk.CTkFrame(
            header,
            fg_color="#e0e7ff",
            corner_radius=6
        )
        type_frame.pack(side="right")
        
        ctk.CTkLabel(
            type_frame,
            text=session["type"],
            font=ctk.CTkFont(size=12),
            text_color="#3730a3"
        ).pack(padx=10, pady=4)
        
    def show_empty_state(self, parent):
        empty_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=15)
        empty_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            empty_frame,
            text="There are no sessions to display",
            font=ctk.CTkFont(size=14),
            text_color="gray"
                ).pack()

    def create_attendance_tab(self, parent):
        # Create main container
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Filters
        filters_frame = ctk.CTkFrame(container, fg_color="white", corner_radius=10)
        filters_frame.pack(fill="x", pady=(0, 20))
        
        # Date range
        date_frame = ctk.CTkFrame(filters_frame, fg_color="transparent")
        date_frame.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(
            date_frame,
            text="Date Range:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#000000"
        ).pack(side="left")
        
        self.start_date = ctk.StringVar()
        ctk.CTkEntry(
            date_frame,
            textvariable=self.start_date,
            placeholder_text="Start Date (YYYY-MM-DD)",
            width=150
        ).pack(side="left", padx=10)
        
        self.end_date = ctk.StringVar()
        ctk.CTkEntry(
            date_frame,
            textvariable=self.end_date,
            placeholder_text="End Date (YYYY-MM-DD)",
            width=150
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            date_frame,
            text="Apply Filter",
            font=ctk.CTkFont(size=12),
            fg_color="#1a237e",
            hover_color="#283593",
            width=100,
            command=self.filter_attendance
        ).pack(side="right")
        
        # Attendance table
        self.table_frame = ctk.CTkScrollableFrame(container, fg_color="white", corner_radius=10)
        self.table_frame.pack(fill="both", expand=True)
        
        self.show_attendance_table()
        
    def show_attendance_table(self, start_date=None, end_date=None):
        # Clear current table
        for widget in self.table_frame.winfo_children():
            widget.destroy()
            
        # Headers
        headers = ["Member", "Total Sessions", "Present", "Late", "Absent", "Excused", "Attendance Rate"]
        header_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent", height=40)
        header_frame.pack(fill="x", padx=15, pady=10)
        header_frame.pack_propagate(False)
        
        for header in headers:
            ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#000000"
            ).pack(side="left", expand=True)
            
        # Calculate attendance for each member
        for user in self.users:
            if user["role"] != "Admin":  # Skip admins
                stats = self.calculate_member_attendance(user, start_date, end_date)
                self.create_attendance_row(stats)
                
    def calculate_member_attendance(self, user, start_date=None, end_date=None):
        stats = {
            "name": user["name"],
            "total": 0,
            "present": 0,
            "late": 0,
            "absent": 0,
            "excused": 0
        }
        
        for session in self.sessions:
            session_date = datetime.fromisoformat(session["datetime"]).date()
            
            # Apply date filter if specified
            if start_date and end_date:
                start = datetime.strptime(start_date, "%Y-%m-%d").date()
                end = datetime.strptime(end_date, "%Y-%m-%d").date()
                if not (start <= session_date <= end):
                    continue
                    
            stats["total"] += 1
            
            try:
                with open(f"data/attendance_{session['datetime']}.json", 'r') as f:
                    attendance = json.load(f)
                    if user["username"] in attendance:
                        status = attendance[user["username"]]["status"]
                        stats[status.lower()] += 1
            except:
                stats["absent"] += 1
                
        # Calculate attendance rate
        stats["rate"] = (stats["present"] + stats["late"]) / stats["total"] * 100 if stats["total"] > 0 else 0
        
        return stats
        
    def create_attendance_row(self, stats):
        row = ctk.CTkFrame(self.table_frame, fg_color="transparent", height=40)
        row.pack(fill="x", padx=15, pady=5)
        row.pack_propagate(False)
        
        # Member name
        ctk.CTkLabel(
            row,
            text=stats["name"],
            font=ctk.CTkFont(size=12),
            text_color="#000000"
        ).pack(side="left", expand=True)
        
        # Stats
        for key in ["total", "present", "late", "absent", "excused"]:
            ctk.CTkLabel(
                row,
                text=str(stats[key]),
                font=ctk.CTkFont(size=12),
                text_color="#000000"
            ).pack(side="left", expand=True)
            
        # Attendance rate
        rate_frame = ctk.CTkFrame(row, fg_color="#e0e7ff", corner_radius=15)
        rate_frame.pack(side="left", expand=True)
        
        ctk.CTkLabel(
            rate_frame,
            text=f"{stats['rate']:.1f}%",
            font=ctk.CTkFont(size=12),
            text_color="#1e40af"
        ).pack(padx=10, pady=5)
        
    def filter_attendance(self):
        try:
            start_date = self.start_date.get().strip()
            end_date = self.end_date.get().strip()
            
            if not (start_date and end_date):
                raise ValueError("Please enter both start and end dates")
                
            # Validate date format
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
            
            self.show_attendance_table(start_date, end_date)
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            
    def export_summary(self):
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Export Session Summary"
            )
            
            if file_path:
                with open(file_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Title", "Date", "Type", "Present", "Late", "Absent", "Excused"])
                    
                    for session in self.sessions:
                        session_date = datetime.fromisoformat(session["datetime"])
                        stats = {"Present": 0, "Late": 0, "Absent": 0, "Excused": 0}
                        
                        try:
                            with open(f"data/attendance_{session['datetime']}.json", 'r') as af:
                                attendance = json.load(af)
                                for record in attendance.values():
                                    stats[record["status"]] += 1
                        except:
                            pass
                            
                        writer.writerow([
                            session["title"],
                            session_date.strftime("%Y-%m-%d %H:%M"),
                            session["type"],
                            stats["Present"],
                            stats["Late"],
                            stats["Absent"],
                            stats["Excused"]
                        ])
                        
                messagebox.showinfo("Success", "Session summary exported successfully")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export summary: {str(e)}")
            
    def export_attendance(self):
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Export Attendance Report"
            )
            
            if file_path:
                with open(file_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        "Member", "Total Sessions", "Present", "Late", 
                        "Absent", "Excused", "Attendance Rate"
                    ])
                    
                    for user in self.users:
                        if user["role"] != "Admin":
                            stats = self.calculate_member_attendance(user)
                            writer.writerow([
                                stats["name"],
                                stats["total"],
                                stats["present"],
                                stats["late"],
                                stats["absent"],
                                stats["excused"],
                                f"{stats['rate']:.1f}%"
                            ])
                            
                messagebox.showinfo("Success", "Attendance report exported successfully")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export attendance: {str(e)}") 

class ReviewDocumentsDialog:
    def __init__(self, parent):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Review Documents")
        self.dialog.geometry("1000x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'+{x}+{y}')
        
        self.load_documents()
        self.create_dialog_content()
        
    def load_documents(self):
        self.documents = []
        base_dir = "documents"
        
        for category in ["Bills", "Laws", "Reports", "Minutes", "Hansards", "Circulars", "Others"]:
            category_path = os.path.join(base_dir, category)
            if os.path.exists(category_path):
                for doc in os.listdir(category_path):
                    self.documents.append({
                        "name": doc,
                        "category": category,
                        "path": os.path.join(category_path, doc),
                        "status": "Pending Review"
                    })
                    
    def create_dialog_content(self):
        # Create main container
        main_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header with filters
        header = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=10)
        header.pack(fill="x", pady=(0, 20))
        
        filter_frame = ctk.CTkFrame(header, fg_color="transparent")
        filter_frame.pack(fill="x", padx=15, pady=15)
        
        # Category filter
        ctk.CTkLabel(
            filter_frame,
            text="Category:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#000000"
        ).pack(side="left")
        
        self.category_var = ctk.StringVar(value="All")
        categories = ["All", "Bills", "Laws", "Reports", "Minutes", "Hansards", "Circulars", "Others"]
        
        category_menu = ctk.CTkOptionMenu(
            filter_frame,
            values=categories,
            variable=self.category_var,
            font=ctk.CTkFont(size=12),
            fg_color="#1a237e",
            button_color="#283593",
            button_hover_color="#1e40af",
            width=150,
            command=self.filter_documents
        )
        category_menu.pack(side="left", padx=10)
        
        # Status filter
        ctk.CTkLabel(
            filter_frame,
            text="Status:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#000000"
        ).pack(side="left", padx=(20, 0))
        
        self.status_var = ctk.StringVar(value="All")
        statuses = ["All", "Pending Review", "Approved", "Rejected"]
        
        status_menu = ctk.CTkOptionMenu(
            filter_frame,
            values=statuses,
            variable=self.status_var,
            font=ctk.CTkFont(size=12),
            fg_color="#1a237e",
            button_color="#283593",
            button_hover_color="#1e40af",
            width=150,
            command=self.filter_documents
        )
        status_menu.pack(side="left", padx=10)
        
        # Documents list
        self.list_frame = ctk.CTkScrollableFrame(main_frame, fg_color="white", corner_radius=10)
        self.list_frame.pack(fill="both", expand=True)
        
        self.show_documents()
        
    def show_documents(self, filtered_docs=None):
        # Clear current list
        for widget in self.list_frame.winfo_children():
            widget.destroy()
            
        # Show documents
        docs = filtered_docs if filtered_docs is not None else self.documents
        for doc in docs:
            self.create_document_card(doc)
            
    def create_document_card(self, doc):
        card = ctk.CTkFrame(self.list_frame, fg_color="transparent")
        card.pack(fill="x", padx=15, pady=10)
        
        # Document info
        info_frame = ctk.CTkFrame(card, fg_color="#f8fafc", corner_radius=10)
        info_frame.pack(fill="x")
        
        # Header with name and category
        header = ctk.CTkFrame(info_frame, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=10)
        
        name_frame = ctk.CTkFrame(header, fg_color="transparent")
        name_frame.pack(side="left")
        
        ctk.CTkLabel(
            name_frame,
            text=doc["name"],
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#000000"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            name_frame,
            text=doc["category"],
            font=ctk.CTkFont(size=12),
            text_color="#64748b"
        ).pack(anchor="w")
        
        # Status badge
        status_frame = ctk.CTkFrame(header, fg_color="#e0e7ff", corner_radius=15)
        status_frame.pack(side="right")
        
        ctk.CTkLabel(
            status_frame,
            text=doc["status"],
            font=ctk.CTkFont(size=12),
            text_color="#1e40af"
        ).pack(padx=10, pady=5)
        
        # Action buttons
        actions = ctk.CTkFrame(info_frame, fg_color="transparent")
        actions.pack(fill="x", padx=15, pady=(0, 10))
        
        ctk.CTkButton(
            actions,
            text="View",
            font=ctk.CTkFont(size=12),
            fg_color="#1a237e",
            hover_color="#283593",
            width=80,
            command=lambda: self.view_document(doc)
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            actions,
            text="Approve",
            font=ctk.CTkFont(size=12),
            fg_color="#059669",
            hover_color="#047857",
            width=80,
            command=lambda: self.update_status(doc, "Approved")
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            actions,
            text="Reject",
            font=ctk.CTkFont(size=12),
            fg_color="#dc2626",
            hover_color="#b91c1c",
            width=80,
            command=lambda: self.update_status(doc, "Rejected")
        ).pack(side="left")
        
    def filter_documents(self, *args):
        category = self.category_var.get()
        status = self.status_var.get()
        
        filtered = self.documents
        
        if category != "All":
            filtered = [d for d in filtered if d["category"] == category]
            
        if status != "All":
            filtered = [d for d in filtered if d["status"] == status]
            
        self.show_documents(filtered)
        
    def view_document(self, doc):
        # Open document in default application
        try:
            os.startfile(doc["path"])
        except:
            messagebox.showerror("Error", "Failed to open document")
            
    def update_status(self, doc, status):
        doc["status"] = status
        self.filter_documents() 

class ArchiveManagementDialog:
    def __init__(self, parent):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Archive Management")
        self.dialog.geometry("1000x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'+{x}+{y}')
        
        # Create archive directory if it doesn't exist
        self.archive_dir = "archives"
        if not os.path.exists(self.archive_dir):
            os.makedirs(self.archive_dir)
            
        self.load_archives()
        self.create_dialog_content()
        
    def load_archives(self):
        self.archives = []
        base_dir = "documents"
        
        # Load all documents with their metadata
        for category in ["Bills", "Laws", "Reports", "Minutes", "Hansards", "Circulars", "Others"]:
            category_path = os.path.join(base_dir, category)
            if os.path.exists(category_path):
                for doc in os.listdir(category_path):
                    doc_path = os.path.join(category_path, doc)
                    self.archives.append({
                        "name": doc,
                        "category": category,
                        "path": doc_path,
                        "size": os.path.getsize(doc_path),
                        "modified": datetime.fromtimestamp(os.path.getmtime(doc_path)),
                        "archived": os.path.exists(os.path.join(self.archive_dir, category, doc))
                    })
                    
    def create_dialog_content(self):
        # Create main container
        main_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header with search and filters
        header = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=10)
        header.pack(fill="x", pady=(0, 20))
        
        filter_frame = ctk.CTkFrame(header, fg_color="transparent")
        filter_frame.pack(fill="x", padx=15, pady=15)
        
        # Search box
        search_frame = ctk.CTkFrame(filter_frame, fg_color="#f1f5f9", corner_radius=20)
        search_frame.pack(side="left")
        
        ctk.CTkLabel(
            search_frame,
            text="🔍",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=(10, 0))
        
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self.filter_archives)
        
        ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Search documents...",
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            border_width=0,
            width=200
        ).pack(side="left", padx=10, pady=5)
        
        # Category filter
        ctk.CTkLabel(
            filter_frame,
            text="Category:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#000000"
        ).pack(side="left", padx=(20, 0))
        
        self.category_var = ctk.StringVar(value="All")
        categories = ["All", "Bills", "Laws", "Reports", "Minutes", "Hansards", "Circulars", "Others"]
        
        category_menu = ctk.CTkOptionMenu(
            filter_frame,
            values=categories,
            variable=self.category_var,
            font=ctk.CTkFont(size=12),
            fg_color="#1a237e",
            button_color="#283593",
            button_hover_color="#1e40af",
            width=150,
            command=self.filter_archives
        )
        category_menu.pack(side="left", padx=10)
        
        # Archive status filter
        self.archived_var = ctk.StringVar(value="All")
        statuses = ["All", "Archived", "Not Archived"]
        
        status_menu = ctk.CTkOptionMenu(
            filter_frame,
            values=statuses,
            variable=self.archived_var,
            font=ctk.CTkFont(size=12),
            fg_color="#1a237e",
            button_color="#283593",
            button_hover_color="#1e40af",
            width=150,
            command=self.filter_archives
        )
        status_menu.pack(side="left", padx=10)
        
        # Bulk actions
        bulk_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        bulk_frame.pack(side="right")
        
        ctk.CTkButton(
            bulk_frame,
            text="Archive Selected",
            font=ctk.CTkFont(size=12),
            fg_color="#059669",
            hover_color="#047857",
            width=120,
            command=self.archive_selected
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            bulk_frame,
            text="Delete Selected",
            font=ctk.CTkFont(size=12),
            fg_color="#dc2626",
            hover_color="#b91c1c",
            width=120,
            command=self.delete_selected
        ).pack(side="left", padx=5)
        
        # Documents list
        self.list_frame = ctk.CTkScrollableFrame(main_frame, fg_color="white", corner_radius=10)
        self.list_frame.pack(fill="both", expand=True)
        
        # Selection header
        select_frame = ctk.CTkFrame(self.list_frame, fg_color="transparent", height=40)
        select_frame.pack(fill="x", padx=15, pady=10)
        select_frame.pack_propagate(False)
        
        self.select_all_var = ctk.BooleanVar()
        ctk.CTkCheckBox(
            select_frame,
            text="",
            variable=self.select_all_var,
            command=self.toggle_all,
            width=20,
            height=20
        ).pack(side="left")
        
        headers = ["Name", "Category", "Size", "Modified", "Status", "Actions"]
        for header in headers:
            ctk.CTkLabel(
                select_frame,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#000000"
            ).pack(side="left", expand=True)
            
        self.show_archives()
        
    def show_archives(self, filtered_docs=None):
        # Clear current list except header
        for widget in list(self.list_frame.winfo_children())[1:]:
            widget.destroy()
            
        # Show documents
        docs = filtered_docs if filtered_docs is not None else self.archives
        for doc in docs:
            self.create_archive_row(doc)
            
    def create_archive_row(self, doc):
        row = ctk.CTkFrame(self.list_frame, fg_color="transparent", height=40)
        row.pack(fill="x", padx=15, pady=5)
        row.pack_propagate(False)
        
        # Selection checkbox
        doc["selected"] = ctk.BooleanVar()
        ctk.CTkCheckBox(
            row,
            text="",
            variable=doc["selected"],
            width=20,
            height=20
        ).pack(side="left")
        
        # Document name
        ctk.CTkLabel(
            row,
            text=doc["name"],
            font=ctk.CTkFont(size=12),
            text_color="#000000"
        ).pack(side="left", expand=True)
        
        # Category
        ctk.CTkLabel(
            row,
            text=doc["category"],
            font=ctk.CTkFont(size=12),
            text_color="#000000"
        ).pack(side="left", expand=True)
        
        # Size
        size_text = f"{doc['size'] / 1024:.1f} KB"
        ctk.CTkLabel(
            row,
            text=size_text,
            font=ctk.CTkFont(size=12),
            text_color="#000000"
        ).pack(side="left", expand=True)
        
        # Modified date
        modified_text = doc["modified"].strftime("%Y-%m-%d %H:%M")
        ctk.CTkLabel(
            row,
            text=modified_text,
            font=ctk.CTkFont(size=12),
            text_color="#000000"
        ).pack(side="left", expand=True)
        
        # Status
        status_frame = ctk.CTkFrame(
            row,
            fg_color="#d1fae5" if doc["archived"] else "#fee2e2",
            corner_radius=15
        )
        status_frame.pack(side="left", expand=True)
        
        status_text = "Archived" if doc["archived"] else "Not Archived"
        status_color = "#059669" if doc["archived"] else "#dc2626"
        
        ctk.CTkLabel(
            status_frame,
            text=status_text,
            font=ctk.CTkFont(size=12),
            text_color=status_color
        ).pack(padx=10, pady=5)
        
        # Actions
        actions = ctk.CTkFrame(row, fg_color="transparent")
        actions.pack(side="left", expand=True)
        
        if doc["archived"]:
            ctk.CTkButton(
                actions,
                text="Restore",
                font=ctk.CTkFont(size=12),
                fg_color="#1a237e",
                hover_color="#283593",
                width=80,
                command=lambda: self.restore_document(doc)
            ).pack(side="left", padx=(0, 5))
        else:
            ctk.CTkButton(
                actions,
                text="Archive",
                font=ctk.CTkFont(size=12),
                fg_color="#059669",
                hover_color="#047857",
                width=80,
                command=lambda: self.archive_document(doc)
            ).pack(side="left", padx=(0, 5))
            
        ctk.CTkButton(
            actions,
            text="Delete",
            font=ctk.CTkFont(size=12),
            fg_color="#dc2626",
            hover_color="#b91c1c",
            width=80,
            command=lambda: self.delete_document(doc)
        ).pack(side="left") 

    def filter_archives(self, *args):
        category = self.category_var.get()
        status = self.archived_var.get()
        search = self.search_var.get().lower()
        
        filtered = self.archives
        
        # Apply category filter
        if category != "All":
            filtered = [d for d in filtered if d["category"] == category]
            
        # Apply status filter
        if status != "All":
            is_archived = status == "Archived"
            filtered = [d for d in filtered if d["archived"] == is_archived]
            
        # Apply search filter
        if search:
            filtered = [d for d in filtered if search in d["name"].lower()]
            
        self.show_archives(filtered)
        
    def toggle_all(self):
        select_all = self.select_all_var.get()
        for doc in self.archives:
            doc["selected"].set(select_all)
            
    def archive_document(self, doc):
        try:
            # Create category directory in archive if it doesn't exist
            archive_category = os.path.join(self.archive_dir, doc["category"])
            os.makedirs(archive_category, exist_ok=True)
            
            # Move file to archive
            archive_path = os.path.join(archive_category, doc["name"])
            shutil.move(doc["path"], archive_path)
            
            # Update document status
            doc["archived"] = True
            doc["path"] = archive_path
            
            # Refresh display
            self.show_archives()
            messagebox.showinfo("Success", f"{doc['name']} has been archived")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to archive document: {str(e)}")
            
    def restore_document(self, doc):
        try:
            # Get original category path
            original_path = os.path.join("documents", doc["category"], doc["name"])
            
            # Move file back to original location
            shutil.move(doc["path"], original_path)
            
            # Update document status
            doc["archived"] = False
            doc["path"] = original_path
            
            # Refresh display
            self.show_archives()
            messagebox.showinfo("Success", f"{doc['name']} has been restored")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to restore document: {str(e)}")
            
    def delete_document(self, doc):
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete {doc['name']}?"):
            try:
                # Delete file
                os.remove(doc["path"])
                
                # Remove from archives list
                self.archives.remove(doc)
                
                # Refresh display
                self.show_archives()
                messagebox.showinfo("Success", f"{doc['name']} has been deleted")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete document: {str(e)}")
                
    def archive_selected(self):
        selected_docs = [doc for doc in self.archives 
                        if doc["selected"].get() and not doc["archived"]]
        
        if not selected_docs:
            messagebox.showinfo("Info", "No documents selected for archiving")
            return
            
        for doc in selected_docs:
            self.archive_document(doc)
            
    def delete_selected(self):
        selected_docs = [doc for doc in self.archives if doc["selected"].get()]
        
        if not selected_docs:
            messagebox.showinfo("Info", "No documents selected for deletion")
            return
            
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete {len(selected_docs)} documents?"):
            for doc in selected_docs:
                self.delete_document(doc)

class DocumentAccessDialog:
    def __init__(self, parent):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Document Access Control")
        self.dialog.geometry("800x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'+{x}+{y}')
        
        # Load data
        self.load_users()
        self.load_access_rules()
        
        self.create_dialog_content()
        
    def load_users(self):
        try:
            with open("data/users.json", 'r') as f:
                self.users = json.load(f)
        except:
            self.users = []
            
    def load_access_rules(self):
        try:
            with open("data/document_access.json", 'r') as f:
                self.access_rules = json.load(f)
        except:
            self.access_rules = {
                "Bills": ["Admin", "Clerk", "Speaker", "Member"],
                "Laws": ["Admin", "Clerk", "Speaker", "Member"],
                "Reports": ["Admin", "Clerk", "Speaker"],
                "Minutes": ["Admin", "Clerk"],
                "Hansards": ["Admin", "Clerk", "Speaker", "Member"],
                "Circulars": ["Admin", "Clerk"],
                "Others": ["Admin"]
            }
            
    def create_dialog_content(self):
        # Create main container
        main_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        ctk.CTkLabel(
            main_frame,
            text="Document Access Permissions",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#000000"
        ).pack(anchor="w", pady=(0, 20))
        
        # Access rules table
        table_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=10)
        table_frame.pack(fill="both", expand=True)
        
        # Headers
        headers_frame = ctk.CTkFrame(table_frame, fg_color="transparent", height=40)
        headers_frame.pack(fill="x", padx=15, pady=10)
        headers_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            headers_frame,
            text="Category",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#000000"
        ).pack(side="left", expand=True)
        
        roles = ["Admin", "Clerk", "Speaker", "Member"]
        for role in roles:
            ctk.CTkLabel(
                headers_frame,
                text=role,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#000000"
            ).pack(side="left", expand=True)
            
        # Rules rows
        for category in self.access_rules.keys():
            self.create_access_row(table_frame, category, roles)
            
        # Save button
        ctk.CTkButton(
            main_frame,
            text="Save Changes",
            font=ctk.CTkFont(size=12),
            fg_color="#1a237e",
            hover_color="#283593",
            width=120,
            command=self.save_changes
        ).pack(pady=(20, 0))
        
    def create_access_row(self, parent, category, roles):
        row = ctk.CTkFrame(parent, fg_color="transparent", height=40)
        row.pack(fill="x", padx=15, pady=5)
        row.pack_propagate(False)
        
        # Category name
        ctk.CTkLabel(
            row,
            text=category,
            font=ctk.CTkFont(size=12),
            text_color="#000000"
        ).pack(side="left", expand=True)
        
        # Role checkboxes
        for role in roles:
            var = ctk.BooleanVar(value=role in self.access_rules[category])
            self.access_rules[category + "_" + role] = var  # Store variable reference
            
            ctk.CTkCheckBox(
                row,
                text="",
                variable=var,
                width=20,
                height=20,
                command=lambda c=category, r=role: self.update_access(c, r)
            ).pack(side="left", expand=True)
            
    def update_access(self, category, role):
        var = self.access_rules[category + "_" + role]
        current_rules = self.access_rules[category]
        
        if var.get() and role not in current_rules:
            current_rules.append(role)
        elif not var.get() and role in current_rules:
            current_rules.remove(role)
            
    def save_changes(self):
        try:
            with open("data/document_access.json", 'w') as f:
                # Clean up temporary variables before saving
                rules = {k: v for k, v in self.access_rules.items() 
                        if not isinstance(v, ctk.BooleanVar)}
                json.dump(rules, f, indent=4)
                
            messagebox.showinfo("Success", "Access rules saved successfully")
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save access rules: {str(e)}")

class GeneralSettingsDialog(ScrollableDialog):
    def __init__(self, parent):
        super().__init__(parent, "General Settings", width=600, height=700)
        
        # System Settings Section
        self.create_section_header("System Settings")
        
        # System Name
        self.create_field("System Name:", "system_name", 
                         default="Assembly Management System")
        
        # Session Timeout
        self.create_field("Session Timeout (minutes):", "timeout", 
                         default="30")
        
        # Document Settings Section
        self.create_section_header("Document Settings")
        
        # Max Upload Size
        self.create_field("Maximum Upload Size (MB):", "max_upload", 
                         default="10")
        
        # Allowed File Types
        self.create_field("Allowed File Types (comma-separated):", "file_types",
                         default="pdf,doc,docx,txt")
        
        # Notification Settings
        self.create_section_header("Notification Settings")
        
        # Enable Notifications
        self.create_toggle("Enable Notifications", "notifications", default=True)
        
        # Backup Settings
        self.create_section_header("Backup Settings")
        
        # Enable Auto Backup
        self.create_toggle("Enable Automatic Backup", "auto_backup", default=True)
        
        # Backup Interval
        self.create_field("Backup Interval (hours):", "backup_interval",
                         default="24")
        
        # Buttons
        self.create_buttons()
        
    def create_section_header(self, text):
        ctk.CTkLabel(
            self.main_frame,
            text=text,
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", pady=(20, 10))
        
    def create_field(self, label, var_name, default=""):
        # Label
        ctk.CTkLabel(
            self.main_frame,
            text=label,
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", pady=(10, 5))
        
        # Entry
        entry = ctk.CTkEntry(
            self.main_frame,
            height=40,
            placeholder_text=default
        )
        entry.insert(0, default)
        entry.pack(fill="x", pady=(0, 10))
        setattr(self, var_name, entry)
        
    def create_toggle(self, label, var_name, default=False):
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            frame,
            text=label,
            font=ctk.CTkFont(size=14)
        ).pack(side="left")
        
        switch = ctk.CTkSwitch(
            frame,
            text="",
            font=ctk.CTkFont(size=14),
            fg_color="#1a237e",
            progress_color="#1a237e"
        )
        if default:
            switch.select()
        switch.pack(side="right")
        setattr(self, var_name, switch)
        
    def create_buttons(self):
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(20, 0))
        
        # Cancel Button
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            font=ctk.CTkFont(size=14),
            fg_color="#dc2626",
            hover_color="#b91c1c",
            command=self.dialog.destroy
        ).pack(side="right", padx=5)
        
        # Save Button
        ctk.CTkButton(
            button_frame,
            text="Save Changes",
            font=ctk.CTkFont(size=14),
            fg_color="#1a237e",
            hover_color="#283593",
            command=self.save_settings
        ).pack(side="right", padx=5)
        
    def save_settings(self):
        # Add your save logic here
        # You can access values using self.system_name.get(), etc.
            self.dialog.destroy()

class BackupRestoreDialog:
    def __init__(self, parent):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Backup & Restore")
        self.dialog.geometry("800x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'+{x}+{y}')
        
        # Create backup directory if it doesn't exist
        self.backup_dir = "backups"
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
            
        self.load_backups()
        self.create_dialog_content()
        
    def load_backups(self):
        self.backups = []
        if os.path.exists(self.backup_dir):
            for backup in os.listdir(self.backup_dir):
                backup_path = os.path.join(self.backup_dir, backup)
                if os.path.isdir(backup_path):
                    self.backups.append({
                        "name": backup,
                        "path": backup_path,
                        "date": datetime.fromtimestamp(os.path.getctime(backup_path)),
                        "size": sum(os.path.getsize(os.path.join(dirpath, filename))
                                  for dirpath, dirnames, filenames in os.walk(backup_path)
                                  for filename in filenames)
                    })
                    
        # Sort backups by date (newest first)
        self.backups.sort(key=lambda x: x["date"], reverse=True)
        
    def create_dialog_content(self):
        # Create main container
        main_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Action buttons
        actions = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=10)
        actions.pack(fill="x", pady=(0, 20))
        
        buttons_frame = ctk.CTkFrame(actions, fg_color="transparent")
        buttons_frame.pack(padx=15, pady=15)
        
        ctk.CTkButton(
            buttons_frame,
            text="Create Backup",
            font=ctk.CTkFont(size=12),
            fg_color="#1a237e",
            hover_color="#283593",
            width=120,
            command=self.create_backup
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            buttons_frame,
            text="Restore Backup",
            font=ctk.CTkFont(size=12),
            fg_color="#059669",
            hover_color="#047857",
            width=120,
            command=self.restore_selected
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            buttons_frame,
            text="Delete Selected",
            font=ctk.CTkFont(size=12),
            fg_color="#dc2626",
            hover_color="#b91c1c",
            width=120,
            command=self.delete_selected
        ).pack(side="left")
        
        # Backups list
        list_frame = ctk.CTkScrollableFrame(main_frame, fg_color="white", corner_radius=10)
        list_frame.pack(fill="both", expand=True)
        
        # Selection header
        select_frame = ctk.CTkFrame(list_frame, fg_color="transparent", height=40)
        select_frame.pack(fill="x", padx=15, pady=10)
        select_frame.pack_propagate(False)
        
        self.select_all_var = ctk.BooleanVar()
        ctk.CTkCheckBox(
            select_frame,
            text="",
            variable=self.select_all_var,
            command=self.toggle_all,
            width=20,
            height=20
        ).pack(side="left")
        
        headers = ["Backup Name", "Date", "Size", ""]
        for header in headers:
            ctk.CTkLabel(
                select_frame,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#000000"
            ).pack(side="left", expand=True)
            
        # Show backups
        self.list_container = ctk.CTkFrame(list_frame, fg_color="transparent")
        self.list_container.pack(fill="both", expand=True)
        
        self.show_backups()
        
    def show_backups(self):
        # Clear current list
        for widget in self.list_container.winfo_children():
            widget.destroy()
            
        # Show backups
        for backup in self.backups:
            self.create_backup_row(backup)
            
    def create_backup_row(self, backup):
        row = ctk.CTkFrame(self.list_container, fg_color="transparent", height=40)
        row.pack(fill="x", padx=15, pady=5)
        row.pack_propagate(False)
        
        # Selection checkbox
        backup["selected"] = ctk.BooleanVar()
        ctk.CTkCheckBox(
            row,
            text="",
            variable=backup["selected"],
            width=20,
            height=20
        ).pack(side="left")
        
        # Backup name
        ctk.CTkLabel(
            row,
            text=backup["name"],
            font=ctk.CTkFont(size=12),
            text_color="#000000"
        ).pack(side="left", expand=True)
        
        # Date
        date_text = backup["date"].strftime("%Y-%m-%d %H:%M")
        ctk.CTkLabel(
            row,
            text=date_text,
            font=ctk.CTkFont(size=12),
            text_color="#000000"
        ).pack(side="left", expand=True)
        
        # Size
        size_text = f"{backup['size'] / (1024*1024):.1f} MB"
        ctk.CTkLabel(
            row,
            text=size_text,
            font=ctk.CTkFont(size=12),
            text_color="#000000"
        ).pack(side="left", expand=True)
        
        # Actions
        actions = ctk.CTkFrame(row, fg_color="transparent")
        actions.pack(side="left", expand=True)
        
        ctk.CTkButton(
            actions,
            text="Delete",
            font=ctk.CTkFont(size=12),
            fg_color="#dc2626",
            hover_color="#b91c1c",
            width=80,
            command=lambda: self.delete_backup(backup)
        ).pack(side="left")
        
    def toggle_all(self):
        select_all = self.select_all_var.get()
        for backup in self.backups:
            backup["selected"].set(select_all)
            
    def create_backup(self):
        try:
            # Create backup directory with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(self.backup_dir, f"backup_{timestamp}")
            os.makedirs(backup_path)
            
            # Copy data directory
            data_path = os.path.join(backup_path, "data")
            if os.path.exists("data"):
                shutil.copytree("data", data_path)
                
            # Copy documents directory
            docs_path = os.path.join(backup_path, "documents")
            if os.path.exists("documents"):
                shutil.copytree("documents", docs_path)
                
            # Refresh backup list
            self.load_backups()
            self.show_backups()
            
            messagebox.showinfo("Success", "Backup created successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create backup: {str(e)}")
            
    def restore_selected(self):
        selected = [b for b in self.backups if b["selected"].get()]
        
        if not selected:
            messagebox.showinfo("Info", "Please select a backup to restore")
            return
            
        if len(selected) > 1:
            messagebox.showerror("Error", "Please select only one backup to restore")
            return
            
        backup = selected[0]
        
        if messagebox.askyesno("Confirm Restore", 
                              f"Are you sure you want to restore from {backup['name']}?\n"
                              "This will overwrite current data."):
            try:
                # Restore data directory
                data_path = os.path.join(backup["path"], "data")
                if os.path.exists(data_path):
                    if os.path.exists("data"):
                        shutil.rmtree("data")
                    shutil.copytree(data_path, "data")
                    
                # Restore documents directory
                docs_path = os.path.join(backup["path"], "documents")
                if os.path.exists(docs_path):
                    if os.path.exists("documents"):
                        shutil.rmtree("documents")
                    shutil.copytree(docs_path, "documents")
                    
                messagebox.showinfo("Success", "Backup restored successfully")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to restore backup: {str(e)}")
                
    def delete_backup(self, backup):
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete {backup['name']}?"):
            try:
                shutil.rmtree(backup["path"])
                self.backups.remove(backup)
                self.show_backups()
                messagebox.showinfo("Success", "Backup deleted successfully")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete backup: {str(e)}")
                
    def delete_selected(self):
        selected = [b for b in self.backups if b["selected"].get()]
        
        if not selected:
            messagebox.showinfo("Info", "No backups selected for deletion")
            return
            
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete {len(selected)} backups?"):
            for backup in selected:
                self.delete_backup(backup)

class SystemLogsDialog:
    def __init__(self, parent):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("System Logs")
        self.dialog.geometry("1000x700")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'+{x}+{y}')
        
        # Create logs directory if it doesn't exist
        self.logs_dir = "logs"
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)
            
        self.load_logs()
        self.create_dialog_content()
        
    def load_logs(self):
        self.logs = []
        log_types = {
            "system": "System Logs",
            "user": "User Activity",
            "document": "Document Activity",
            "session": "Session Logs",
            "error": "Error Logs"
        }
        
        for log_type, description in log_types.items():
            log_file = os.path.join(self.logs_dir, f"{log_type}.log")
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    entries = []
                    for line in f:
                        try:
                            timestamp, level, message = line.strip().split(" | ", 2)
                            entries.append({
                                "timestamp": datetime.fromisoformat(timestamp),
                                "level": level,
                                "message": message
                            })
                        except:
                            continue
                            
                    self.logs.append({
                        "type": log_type,
                        "description": description,
                        "entries": entries
                    })
                    
    def create_dialog_content(self):
        # Create main container
        main_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Filters
        filter_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=10)
        filter_frame.pack(fill="x", pady=(0, 20))
        
        filters = ctk.CTkFrame(filter_frame, fg_color="transparent")
        filters.pack(padx=15, pady=15, fill="x")
        
        # Log type filter
        type_frame = ctk.CTkFrame(filters, fg_color="transparent")
        type_frame.pack(side="left")
        
        ctk.CTkLabel(
            type_frame,
            text="Log Type:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#000000"
        ).pack(side="left")
        
        self.type_var = ctk.StringVar(value="All")
        types = ["All"] + [log["description"] for log in self.logs]
        
        type_menu = ctk.CTkOptionMenu(
            type_frame,
            values=types,
            variable=self.type_var,
            font=ctk.CTkFont(size=12),
            fg_color="#1a237e",
            button_color="#283593",
            button_hover_color="#1e40af",
            width=150,
            command=self.filter_logs
        )
        type_menu.pack(side="left", padx=10)
        
        # Level filter
        level_frame = ctk.CTkFrame(filters, fg_color="transparent")
        level_frame.pack(side="left", padx=20)
        
        ctk.CTkLabel(
            level_frame,
            text="Level:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#000000"
        ).pack(side="left")
        
        self.level_var = ctk.StringVar(value="All")
        levels = ["All", "INFO", "WARNING", "ERROR"]
        
        level_menu = ctk.CTkOptionMenu(
            level_frame,
            values=levels,
            variable=self.level_var,
            font=ctk.CTkFont(size=12),
            fg_color="#1a237e",
            button_color="#283593",
            button_hover_color="#1e40af",
            width=150,
            command=self.filter_logs
        )
        level_menu.pack(side="left", padx=10)
        
        # Date range
        date_frame = ctk.CTkFrame(filters, fg_color="transparent")
        date_frame.pack(side="left")
        
        self.start_date = ctk.StringVar()
        ctk.CTkEntry(
            date_frame,
            textvariable=self.start_date,
            placeholder_text="Start Date (YYYY-MM-DD)",
            width=150
        ).pack(side="left", padx=5)
        
        self.end_date = ctk.StringVar()
        ctk.CTkEntry(
            date_frame,
            textvariable=self.end_date,
            placeholder_text="End Date (YYYY-MM-DD)",
            width=150
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            date_frame,
            text="Apply",
            font=ctk.CTkFont(size=12),
            fg_color="#1a237e",
            hover_color="#283593",
            width=80,
            command=self.filter_logs
        ).pack(side="left", padx=5)
        
        # Export button
        ctk.CTkButton(
            filters,
            text="Export Logs",
            font=ctk.CTkFont(size=12),
            fg_color="#059669",
            hover_color="#047857",
            width=120,
            command=self.export_logs
        ).pack(side="right")
        
        # Logs list
        self.list_frame = ctk.CTkScrollableFrame(main_frame, fg_color="white", corner_radius=10)
        self.list_frame.pack(fill="both", expand=True)
        
        self.show_logs()
        
    def show_logs(self, filtered_entries=None):
        # Clear current list
        for widget in self.list_frame.winfo_children():
            widget.destroy()
            
        # Show log entries
        entries = []
        if filtered_entries is not None:
            entries = filtered_entries
        else:
            for log in self.logs:
                entries.extend(log["entries"])
                
        # Sort by timestamp (newest first)
        entries.sort(key=lambda x: x["timestamp"], reverse=True)
        
        for entry in entries:
            self.create_log_entry(entry)
            
    def create_log_entry(self, entry):
        # Entry container
        container = ctk.CTkFrame(self.list_frame, fg_color="transparent")
        container.pack(fill="x", padx=15, pady=5)
        
        # Level indicator
        level_colors = {
            "INFO": ("#059669", "#d1fae5"),
            "WARNING": ("#d97706", "#fef3c7"),
            "ERROR": ("#dc2626", "#fee2e2")
        }
        color, bg_color = level_colors.get(entry["level"], ("#6b7280", "#f3f4f6"))
        
        level_frame = ctk.CTkFrame(container, fg_color=bg_color, corner_radius=15)
        level_frame.pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            level_frame,
            text=entry["level"],
            font=ctk.CTkFont(size=12),
            text_color=color
        ).pack(padx=10, pady=5)
        
        # Timestamp
        time_text = entry["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        ctk.CTkLabel(
            container,
            text=time_text,
            font=ctk.CTkFont(size=12),
            text_color="#64748b"
        ).pack(side="left", padx=(0, 15))
        
        # Message
        ctk.CTkLabel(
            container,
            text=entry["message"],
            font=ctk.CTkFont(size=12),
            text_color="#000000",
            wraplength=700,
            justify="left"
        ).pack(side="left", fill="x")
        
    def filter_logs(self, *args):
        try:
            log_type = self.type_var.get()
            level = self.level_var.get()
            start_date = self.start_date.get().strip()
            end_date = self.end_date.get().strip()
            
            filtered = []
            for log in self.logs:
                if log_type != "All" and log["description"] != log_type:
                    continue
                    
                for entry in log["entries"]:
                    # Apply level filter
                    if level != "All" and entry["level"] != level:
                        continue
                        
                    # Apply date filter
                    if start_date and end_date:
                        entry_date = entry["timestamp"].date()
                        start = datetime.strptime(start_date, "%Y-%m-%d").date()
                        end = datetime.strptime(end_date, "%Y-%m-%d").date()
                        
                        if not (start <= entry_date <= end):
                            continue
                            
                    filtered.append(entry)
                    
            self.show_logs(filtered)
            
        except ValueError as e:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
            
    def export_logs(self):
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Export Logs"
            )
            
            if file_path:
                with open(file_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Timestamp", "Level", "Message"])
                    
                    for log in self.logs:
                        for entry in log["entries"]:
                            writer.writerow([
                                entry["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
                                entry["level"],
                                entry["message"]
                            ])
                            
                messagebox.showinfo("Success", "Logs exported successfully")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export logs: {str(e)}")

class ReviewMotionsDialog:
    def __init__(self, parent):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Review Motions")
        self.dialog.geometry("800x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.parent = parent
        self.data_manager = parent.data_manager
        
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
            text="Review Pending Motions",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)
        
        # Motions list
        self.content_frame = ctk.CTkScrollableFrame(
            self.dialog,
            fg_color="transparent"
        )
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Show pending motions
        pending_motions = [
            m for m in self.data_manager.get_motions()
            if m["needs_approval"]
        ]
        
        if not pending_motions:
            self.show_empty_state()
        else:
            for motion in pending_motions:
                self.create_motion_review_card(motion)
                
    def show_empty_state(self):
        empty_frame = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=15)
        empty_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            empty_frame,
            text="No Pending Motions",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(40, 10))
        
        ctk.CTkLabel(
            empty_frame,
            text="There are no motions waiting for review",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack()
                
    def create_motion_review_card(self, motion):
        card = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=15)
        card.pack(fill="x", pady=(0, 15))
        
        # Main content
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=20)
        
        # Motion details
        ctk.CTkLabel(
            content,
            text=motion["title"],
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w")
        
        # Approval buttons
        buttons_frame = ctk.CTkFrame(content, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(15, 0))
        
        ctk.CTkButton(
            buttons_frame,
            text="Approve",
            fg_color="#059669",
            hover_color="#047857",
            command=lambda: self.handle_motion(motion["id"], True)
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="Reject",
            fg_color="#dc2626",
            hover_color="#b91c1c",
            command=lambda: self.handle_motion(motion["id"], False)
        ).pack(side="left", padx=5)
        
    def handle_motion(self, motion_id, approved):
        self.data_manager.approve_motion(motion_id, approved)
        # Refresh the list
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.create_dialog_content()

class ReviewVotesDialog:
    def __init__(self, parent):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Review Votes")
        self.dialog.geometry("800x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.parent = parent
        self.data_manager = parent.data_manager
        
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
            text="Review Pending Votes",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)
        
        # Votes list
        self.content_frame = ctk.CTkScrollableFrame(
            self.dialog,
            fg_color="transparent"
        )
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Show pending votes
        pending_votes = [
            v for v in self.data_manager.get_votes()
            if v["needs_approval"]
        ]
        
        if not pending_votes:
            self.show_empty_state()
        else:
            for vote in pending_votes:
                self.create_vote_review_card(vote)
                
    def show_empty_state(self):
        empty_frame = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=15)
        empty_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            empty_frame,
            text="No Pending Votes",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(40, 10))
        
        ctk.CTkLabel(
            empty_frame,
            text="There are no votes waiting for review",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack()
                
    def create_vote_review_card(self, vote):
        card = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=15)
        card.pack(fill="x", pady=(0, 15))
        
        # Main content
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=20)
        
        # Vote details
        ctk.CTkLabel(
            content,
            text=f"Vote on: {vote['motion_title']}",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            content,
            text=f"Initiated by: {vote['created_by']}",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(anchor="w", pady=(5, 10))
        
        # Vote results
        results_frame = ctk.CTkFrame(content, fg_color="#f8fafc", corner_radius=6)
        results_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            results_frame,
            text=f"Yes: {vote['yes_votes']} | No: {vote['no_votes']} | Abstain: {vote['abstain']}",
            font=ctk.CTkFont(size=14)
        ).pack(padx=15, pady=10)
        
        # Approval buttons
        buttons = ctk.CTkFrame(content, fg_color="transparent")
        buttons.pack(fill="x")
        
        ctk.CTkButton(
            buttons,
            text="Approve",
            fg_color="#059669",
            hover_color="#047857",
            command=lambda: self.handle_vote(vote["id"], True)
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            buttons,
            text="Reject",
            fg_color="#dc2626",
            hover_color="#b91c1c",
            command=lambda: self.handle_vote(vote["id"], False)
        ).pack(side="left", padx=5)
        
    def handle_vote(self, vote_id, approved):
        self.data_manager.approve_vote(vote_id, approved)
        # Refresh the list
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.create_dialog_content()