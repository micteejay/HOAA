import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime
import json
import os

class MotionContent(ctk.CTkFrame):
    def __init__(self, parent, current_user, is_admin=False):
        super().__init__(parent)
        
        # Store user info
        self.current_user = current_user
        self.is_admin = is_admin
        
        # Configure frame
        self.configure(fg_color="#f1f5f9")
        
        # Initialize motions list
        self.motions = []
        
        # Add data_manager reference
        self.data_manager = parent.data_manager
        
        # Create UI sections
        self.create_header()
        self.create_content()
        
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
            text="📌",
            font=ctk.CTkFont(size=24)
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            title_frame,
            text="Motions",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#000000"
        ).pack(side="left")
        
        # Right side buttons
        buttons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        buttons_frame.pack(side="right", padx=30)
        
        # New Motion button
        self.new_motion_button = ctk.CTkButton(
            buttons_frame,
            text="+ New Motion",
            font=ctk.CTkFont(size=12),
            fg_color="#1a237e",
            hover_color="#283593",
            height=35,
            command=self.create_motion
        )
        self.new_motion_button.pack(side="right", padx=5)
        
    def create_content(self):
        self.content_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Show empty state or motions list
        self.show_motions_list()
        
    def show_motions_list(self):
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        if not self.motions:
            self.show_empty_state()
        else:
            for motion in self.motions:
                self.create_motion_card(motion)
                
    def show_empty_state(self):
        empty_frame = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=15)
        empty_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            empty_frame,
            text="No Motions",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(40, 10))
        
        ctk.CTkLabel(
            empty_frame,
            text="Click '+ New Motion' to create a new motion",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack()
        
    def create_motion(self):
        dialog = NewMotionDialog(self)
        self.wait_window(dialog.dialog)
        
        if hasattr(dialog, 'result'):
            # Add new motion to the list
            motion_data = dialog.result
            motion_data.update({
                "id": str(datetime.now().timestamp()),
                "created_by": self.current_user,
                "date": datetime.now(),
                "status": "Pending",
                "needs_approval": True
            })
            
            # Save to data manager
            self.data_manager.add_motion(motion_data)
            self.motions = self.data_manager.get_motions()
            self.show_motions_list()

    def create_motion_card(self, motion):
        card = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=15)
        card.pack(fill="x", pady=(0, 15))
        
        # Main content
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=20)
        
        # Header with title and type
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            header,
            text=motion["title"],
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#000000"
        ).pack(side="left")
        
        # Motion type badge
        type_frame = ctk.CTkFrame(
            header,
            fg_color="#f1f5f9",
            corner_radius=6
        )
        type_frame.pack(side="right")
        
        ctk.CTkLabel(
            type_frame,
            text=motion["type"],
            font=ctk.CTkFont(size=12),
            text_color="#64748b"
        ).pack(padx=10, pady=4)
        
        # Motion text
        ctk.CTkLabel(
            content,
            text=motion["text"],
            font=ctk.CTkFont(size=14),
            text_color="#000000",
            wraplength=800,
            justify="left"
        ).pack(anchor="w")
        
        # Footer with metadata
        footer = ctk.CTkFrame(content, fg_color="transparent")
        footer.pack(fill="x", pady=(15, 0))
        
        # Created by and date
        info = ctk.CTkFrame(footer, fg_color="transparent")
        info.pack(side="left")
        
        ctk.CTkLabel(
            info,
            text=f"Created by {motion['created_by']}",
            font=ctk.CTkFont(size=12),
            text_color="#64748b"
        ).pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(
            info,
            text=motion["date"].strftime("%Y-%m-%d %H:%M"),
            font=ctk.CTkFont(size=12),
            text_color="#64748b"
        ).pack(side="left")
        
        # Status badge
        status_colors = {
            "Pending": ("#fef3c7", "#d97706", "⏳"),
            "Approved": ("#d1fae5", "#059669", "✅"),
            "Rejected": ("#fee2e2", "#dc2626", "❌")
        }
        
        status_info = status_colors.get(
            motion["status"], 
            ("#f1f5f9", "#64748b", "❓")
        )
        bg_color, text_color, icon = status_info
        
        status_frame = ctk.CTkFrame(
            footer,
            fg_color=bg_color,
            corner_radius=6
        )
        status_frame.pack(side="right")
        
        ctk.CTkLabel(
            status_frame,
            text=f"{icon} {motion['status']}",
            font=ctk.CTkFont(size=12),
            text_color=text_color
        ).pack(padx=10, pady=4)

class NewMotionDialog:
    def __init__(self, parent):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("New Motion")
        self.dialog.geometry("600x700")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Store parent reference
        self.parent = parent
        
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
            text="New Motion",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)
        
        # Form container
        form = ctk.CTkFrame(self.dialog, fg_color="transparent")
        form.pack(fill="x", padx=20)
        
        # Motion Title
        ctk.CTkLabel(
            form,
            text="Motion Title:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w")
        
        self.title_var = ctk.StringVar()
        ctk.CTkEntry(
            form,
            textvariable=self.title_var,
            height=35
        ).pack(fill="x", pady=(5, 15))
        
        # Motion Type
        ctk.CTkLabel(
            form,
            text="Motion Type:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w")
        
        self.motion_type = ctk.StringVar(value="Regular")
        types_frame = ctk.CTkFrame(form, fg_color="transparent")
        types_frame.pack(fill="x", pady=(5, 15))
        
        motion_types = ["Regular", "Urgent", "Amendment", "Procedural"]
        for mtype in motion_types:
            ctk.CTkRadioButton(
                types_frame,
                text=mtype,
                variable=self.motion_type,
                value=mtype,
                font=ctk.CTkFont(size=12)
            ).pack(side="left", padx=10)
        
        # Motion Text
        ctk.CTkLabel(
            form,
            text="Motion Text:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w")
        
        self.motion_text = ctk.CTkTextbox(
            form,
            height=200
        )
        self.motion_text.pack(fill="x", pady=(5, 15))
        
        # Supporting Documents
        ctk.CTkLabel(
            form,
            text="Supporting Documents:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w")
        
        docs_frame = ctk.CTkFrame(form, fg_color="transparent")
        docs_frame.pack(fill="x", pady=(5, 15))
        
        ctk.CTkButton(
            docs_frame,
            text="Attach Files",
            font=ctk.CTkFont(size=12),
            fg_color="#1a237e",
            hover_color="#283593",
            command=self.attach_files
        ).pack(side="left")
        
        # Buttons
        buttons = ctk.CTkFrame(self.dialog, fg_color="transparent")
        buttons.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(
            buttons,
            text="Submit",
            font=ctk.CTkFont(size=14),
            fg_color="#1a237e",
            hover_color="#283593",
            command=self.submit_motion
        ).pack(side="left", expand=True, padx=5)
        
        ctk.CTkButton(
            buttons,
            text="Cancel",
            font=ctk.CTkFont(size=14),
            fg_color="#dc2626",
            hover_color="#b91c1c",
            command=self.dialog.destroy
        ).pack(side="left", expand=True, padx=5)
        
    def attach_files(self):
        files = filedialog.askopenfilenames(
            title="Select Files",
            filetypes=[
                ("PDF files", "*.pdf"),
                ("Word files", "*.doc;*.docx"),
                ("All files", "*.*")
            ]
        )
        if files:
            # Handle file attachments
            pass
            
    def submit_motion(self):
        try:
            title = self.title_var.get().strip()
            motion_text = self.motion_text.get("1.0", "end-1c").strip()
            
            if not title:
                raise ValueError("Please enter a motion title")
            if not motion_text:
                raise ValueError("Please enter the motion text")
                
            # Create motion data
            self.result = {
                "title": title,
                "type": self.motion_type.get(),
                "text": motion_text
            }
            
            self.dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e)) 