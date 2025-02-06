import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox, filedialog
import os
import shutil

class PetitionContent(ctk.CTkFrame):
    def __init__(self, parent, current_user, is_admin=False):
        super().__init__(parent)
        
        # Store user info
        self.current_user = current_user
        self.is_admin = is_admin
        
        # Store petitions data
        self.petitions = []
        self.selected_petition = None
        
        # Create documents directory if it doesn't exist
        self.docs_dir = "petitions"
        if not os.path.exists(self.docs_dir):
            os.makedirs(self.docs_dir)
        
        # Configure frame
        self.configure(fg_color="#f1f5f9")
        
        # Create UI sections
        self.create_header()
        self.create_stats_bar()
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
        
        # Title with icon and back button
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left", padx=30)
        
        # Back button
        self.back_button = ctk.CTkButton(
            title_frame,
            text="← Back",
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            text_color="#1a237e",
            hover_color="#e8eaf6",
            width=60,
            height=30,
            command=self.show_petitions_list
        )
        self.back_button.pack(side="left", padx=(0, 15))
        self.back_button.pack_forget()  # Hide initially
        
        ctk.CTkLabel(
            title_frame,
            text="⚖️",
            font=ctk.CTkFont(size=24)
        ).pack(side="left", padx=(0, 10))
        
        self.title_label = ctk.CTkLabel(
            title_frame,
            text="Petitions",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(side="left")
        
        # Right side buttons
        buttons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        buttons_frame.pack(side="right", padx=30)
        
        # Approve button (only visible to admin)
        if self.is_admin:
            self.approve_button = ctk.CTkButton(
                buttons_frame,
                text="Approve Petition",
                font=ctk.CTkFont(size=12),
                fg_color="#059669",
                hover_color="#047857",
                height=35,
                state="disabled",
                command=self.approve_petition
            )
            self.approve_button.pack(side="right", padx=5)
        
        # Edit button
        self.edit_button = ctk.CTkButton(
            buttons_frame,
            text="Edit Petition",
            font=ctk.CTkFont(size=12),
            fg_color="#6366f1",
            hover_color="#4f46e5",
            height=35,
            state="disabled",
            command=self.edit_petition
        )
        self.edit_button.pack(side="right", padx=5)
        
        # New Petition button
        self.new_petition_button = ctk.CTkButton(
            buttons_frame,
            text="+ New Petition",
            font=ctk.CTkFont(size=12),
            fg_color="#1a237e",
            hover_color="#283593",
            height=35,
            command=self.create_new_petition
        )
        self.new_petition_button.pack(side="right", padx=5)
        
    def create_stats_bar(self):
        # Remove existing stats frame if it exists
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and hasattr(widget, 'stats_tag'):
                widget.destroy()
        
        stats_frame = ctk.CTkFrame(self, fg_color="white", height=100)
        stats_frame.stats_tag = True  # Add tag to identify stats frame
        stats_frame.pack(fill="x", padx=0, pady=(0, 2))
        stats_frame.pack_propagate(False)
        
        container = ctk.CTkFrame(stats_frame, fg_color="transparent")
        container.pack(padx=30, pady=20, fill="x")
        
        # Filter petitions based on visibility and user role
        visible_petitions = [p for p in self.petitions if 
                            p["visible"] or  # Show approved petitions
                            p["created_by"] == self.current_user or  # Show own petitions
                            self.is_admin]  # Show all to admin
        
        # Get counts
        total_count = len(visible_petitions)
        pending_count = sum(1 for p in visible_petitions if p["status"] == "Pending")
        approved_count = sum(1 for p in visible_petitions if p["status"] == "Approved")
        
        stats = [
            {
                "title": "Total Petitions",
                "value": total_count,
                "icon": "⚖️",
                "color": "#6366f1",
                "bg_color": "#e0e7ff"
            },
            {
                "title": "Pending Approval",
                "value": pending_count,
                "icon": "⏳",
                "color": "#f59e0b",
                "bg_color": "#fef3c7"
            },
            {
                "title": "Approved",
                "value": approved_count,
                "icon": "✅",
                "color": "#10b981",
                "bg_color": "#d1fae5"
            }
        ]
        
        for i, stat in enumerate(stats):
            self.create_stat_card(container, stat, i)
            
    def create_stat_card(self, container, stat, index):
        stat_frame = ctk.CTkFrame(container, fg_color="transparent")
        stat_frame.grid(row=0, column=index, padx=15, sticky="ew")
        container.grid_columnconfigure(index, weight=1)
        
        header = ctk.CTkFrame(stat_frame, fg_color="transparent")
        header.pack(fill="x")
        
        icon_frame = ctk.CTkFrame(
            header,
            fg_color=stat["bg_color"],
            width=40,
            height=40,
            corner_radius=8
        )
        icon_frame.pack(side="left")
        icon_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            icon_frame,
            text=stat["icon"],
            font=ctk.CTkFont(size=20),
            text_color=stat["color"]
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        value_frame = ctk.CTkFrame(header, fg_color="transparent")
        value_frame.pack(side="left", padx=10)
        
        ctk.CTkLabel(
            value_frame,
            text=str(stat["value"]),
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=stat["color"]
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            value_frame,
            text=stat["title"],
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(anchor="w") 

    def create_content(self):
        self.content_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Show empty state initially
        self.show_empty_state()
        
    def show_empty_state(self):
        empty_frame = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=15)
        empty_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            empty_frame,
            text="No Petitions",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(40, 10))
        
        ctk.CTkLabel(
            empty_frame,
            text="Click '+ New Petition' to create a new petition",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack()
        
    def create_new_petition(self):
        dialog = NewPetitionDialog(self)
        self.wait_window(dialog.dialog)
        
        if hasattr(dialog, 'result'):
            # Add creator info and visibility
            petition_data = dialog.result
            petition_data.update({
                "created_by": self.current_user,
                "visible": False  # Hidden until approved
            })
            
            self.petitions.append(petition_data)
            self.show_petitions_list()
            self.create_stats_bar()  # Update stats
            
    def show_petitions_list(self):
        # Reset title and hide back button
        self.title_label.configure(text="Petitions")
        self.back_button.pack_forget()
        
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Filter petitions based on visibility and user role
        visible_petitions = [p for p in self.petitions if 
                            p["visible"] or  # Show approved petitions
                            p["created_by"] == self.current_user or  # Show own petitions
                            self.is_admin]  # Show all to admin
        
        if not visible_petitions:
            self.show_empty_state()
            return
            
        # Petitions grid
        for petition in visible_petitions:
            self.create_petition_card(petition)
        
        # Update stats after showing petitions
        self.create_stats_bar()
            
    def create_petition_card(self, petition):
        card = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=15)
        card.pack(fill="x", pady=(0, 15))
        
        # Add hover effect
        def on_enter(e):
            if self.selected_petition != petition:
                card.configure(fg_color="#f8fafc")
                
        def on_leave(e):
            if self.selected_petition != petition:
                card.configure(fg_color="white")
                
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        
        # Main content
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=20)
        
        # Left side with icon
        icon_frame = ctk.CTkFrame(
            content,
            fg_color="#f1f5f9",
            width=50,
            height=50,
            corner_radius=10
        )
        icon_frame.pack(side="left")
        icon_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            icon_frame,
            text="📝",
            font=ctk.CTkFont(size=24)
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        # Info section
        info_frame = ctk.CTkFrame(content, fg_color="transparent")
        info_frame.pack(side="left", padx=15, fill="x", expand=True)
        
        # Title and date row
        header_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        header_frame.pack(fill="x")
        
        ctk.CTkLabel(
            header_frame,
            text=petition["title"],
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#000000"
        ).pack(side="left")
        
        date_frame = ctk.CTkFrame(
            header_frame,
            fg_color="#f1f5f9",
            corner_radius=6
        )
        date_frame.pack(side="right")
        
        ctk.CTkLabel(
            date_frame,
            text=f"📅 {petition['date'].strftime('%B %d, %Y')}",
            font=ctk.CTkFont(size=12),
            text_color="#64748b"
        ).pack(padx=8, pady=4)
        
        # Document info
        doc_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        doc_frame.pack(fill="x", pady=(5, 0))
        
        ctk.CTkLabel(
            doc_frame,
            text=f"📎 {os.path.basename(petition['document'])}",
            font=ctk.CTkFont(size=14),
            text_color="#334155"
        ).pack(side="left")
        
        ctk.CTkButton(
            doc_frame,
            text="View",
            font=ctk.CTkFont(size=12),
            fg_color="#1a237e",
            hover_color="#283593",
            width=60,
            command=lambda p=petition: self.view_document(p['document'])
        ).pack(side="right")
        
        # Right side - Status badge
        status_colors = {
            "Draft": ("#f1f5f9", "#64748b", "📝"),
            "Pending": ("#fef3c7", "#d97706", "⏳"),
            "Under Review": ("#e0e7ff", "#4f46e5", "🔍"),
            "Approved": ("#d1fae5", "#059669", "✅"),
            "Rejected": ("#fee2e2", "#dc2626", "❌")
        }
        
        # Get status colors with default value
        status_info = status_colors.get(
            petition["status"], 
            ("#f1f5f9", "#64748b", "❓")  # Default values if status not found
        )
        bg_color, text_color, icon = status_info
        
        status_frame = ctk.CTkFrame(
            content,
            fg_color=bg_color,
            corner_radius=6
        )
        status_frame.pack(side="right")
        
        ctk.CTkLabel(
            status_frame,
            text=f"{icon} {petition['status']}",
            font=ctk.CTkFont(size=12),
            text_color=text_color
        ).pack(padx=10, pady=4)
        
        # Add selection binding
        card.bind("<Button-1>", lambda e, p=petition: self.select_petition(p))
        
        # Show selection if this is the selected petition
        if self.selected_petition and self.selected_petition["id"] == petition["id"]:
            card.configure(fg_color="#f1f5f9")

    def select_petition(self, petition):
        """Select a petition and enable appropriate buttons"""
        self.selected_petition = petition
        
        try:
            # Show back button and update title
            self.back_button.pack(side="left", padx=(0, 15))
            self.title_label.configure(text=petition["title"])
            
            # Enable/disable approve button based on petition status and user role
            if hasattr(self, 'approve_button'):  # Only if admin
                if petition["status"] == "Pending":
                    self.approve_button.configure(state="normal")
                else:
                    self.approve_button.configure(state="disabled")
            
            # Enable/disable edit button based on ownership
            if hasattr(self, 'edit_button'):
                if petition["created_by"] == self.current_user and petition["status"] == "Pending":
                    self.edit_button.configure(state="normal")
                else:
                    self.edit_button.configure(state="disabled")
            
            # Show petition details
            self.show_petition_details(petition)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to select petition: {str(e)}")

    def show_petition_details(self, petition):
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create details view
        details_frame = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=15)
        details_frame.pack(fill="both", expand=True)
        
        # Document preview section
        preview_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        preview_frame.pack(fill="x", padx=30, pady=30)
        
        ctk.CTkLabel(
            preview_frame,
            text="📎 Document:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w")
        
        doc_frame = ctk.CTkFrame(preview_frame, fg_color="#f1f5f9", corner_radius=6)
        doc_frame.pack(fill="x", pady=(10, 0))
        
        ctk.CTkLabel(
            doc_frame,
            text=os.path.basename(petition["document"]),
            font=ctk.CTkFont(size=12),
            text_color="#64748b"
        ).pack(side="left", padx=15, pady=10)
        
        ctk.CTkButton(
            doc_frame,
            text="View Document",
            font=ctk.CTkFont(size=12),
            fg_color="#1a237e",
            hover_color="#283593",
            width=120,
            command=lambda: self.view_document(petition["document"])
        ).pack(side="right", padx=15, pady=5)
        
        # Status info
        status_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        status_frame.pack(fill="x", padx=30)
        
        status_colors = {
            "Pending": ("#000000", "⏳"),
            "Approved": ("#000000", "✅"),
            "Rejected": ("#000000", "❌")
        }
        
        bg_color, text_color, icon = status_colors.get(petition["status"])
        
        status_label = ctk.CTkFrame(
            status_frame,
            fg_color=bg_color,
            corner_radius=6
        )
        status_label.pack(side="left")
        
        ctk.CTkLabel(
            status_label,
            text=f"{icon} {petition['status']}",
            font=ctk.CTkFont(size=12),
            text_color=text_color
        ).pack(padx=10, pady=4)
        
        # Created date
        ctk.CTkLabel(
            status_frame,
            text=f"Created on {petition['date'].strftime('%B %d, %Y')}",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(side="left", padx=15)
        
        # Show approval info if approved
        if petition["status"] == "Approved":
            approval_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
            approval_frame.pack(fill="x", padx=30, pady=(20, 0))
            
            ctk.CTkLabel(
                approval_frame,
                text="✍️ Approval Notes:",
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                approval_frame,
                text=petition.get("approval_notes", "No notes provided"),
                font=ctk.CTkFont(size=12),
                text_color="#64748b",
                wraplength=800
            ).pack(anchor="w", pady=(5, 0))
            
            ctk.CTkLabel(
                approval_frame,
                text=f"Approved by {petition['approved_by']} on {petition['approval_date'].strftime('%B %d, %Y')}",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            ).pack(anchor="w", pady=(10, 0))

    def forward_to_committee(self):
        """Forward selected petition to committee"""
        if not self.selected_petition:
            return
        
        dialog = ForwardToCommitteeDialog(self)
        self.wait_window(dialog.dialog)
        
        if hasattr(dialog, 'result'):
            # Update petition status and committee
            self.selected_petition["status"] = "In Committee"
            self.selected_petition["committee"] = dialog.result["committee"]
            self.selected_petition["forward_date"] = datetime.now()
            
            # Update stats and refresh display
            self.show_petitions_list()
            self.create_stats_bar()
            
            # Reset selection and disable forward button
            self.selected_petition = None
            self.forward_button.configure(state="disabled")
            
            messagebox.showinfo(
                "Success",
                "Petition has been forwarded to committee successfully"
            )

    def approve_petition(self):
        """Approve the selected petition"""
        if not self.selected_petition or not self.is_admin:
            return
        
        dialog = ApprovePetitionDialog(self)
        self.wait_window(dialog.dialog)
        
        if hasattr(dialog, 'result'):
            # Update petition status
            self.selected_petition.update({
                "status": "Approved",
                "approval_date": datetime.now(),
                "approval_notes": dialog.result["notes"],
                "approved_by": self.current_user,
                "visible": True  # Make visible to all users
            })
            
            # Update display
            self.show_petitions_list()
            self.create_stats_bar()
            
            # Reset selection and disable approve button
            self.selected_petition = None
            self.approve_button.configure(state="disabled")
            
            messagebox.showinfo(
                "Success",
                "Petition has been approved successfully"
            )

    def view_document(self, document_path):
        """Open the petition document"""
        from document_viewer import DocumentViewer
        
        if os.path.exists(document_path):
            viewer = DocumentViewer(self, document_path)
        else:
            messagebox.showerror("Error", "Document file not found")

    def edit_petition(self):
        """Edit the selected petition"""
        if not self.selected_petition:
            return
        
        dialog = EditPetitionDialog(self, self.selected_petition)
        self.wait_window(dialog.dialog)
        
        if hasattr(dialog, 'result'):
            # Update petition data
            self.selected_petition.update(dialog.result)
            
            # Update display
            self.show_petitions_list()
            
            # Reset selection and disable edit button
            self.selected_petition = None
            self.edit_button.configure(state="disabled")
            
            messagebox.showinfo(
                "Success",
                "Petition has been updated successfully"
            )

class NewPetitionDialog:
    def __init__(self, parent):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("New Petition")
        self.dialog.geometry("600x800")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'+{x}+{y}')
        
        self.document_path = None  # Store uploaded document path
        self.create_dialog_content()
        
    def create_dialog_content(self):
        content_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            title_frame,
            text="Petition Title:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w")
        
        self.title_var = ctk.StringVar()
        title_entry = ctk.CTkEntry(
            title_frame,
            textvariable=self.title_var,
            placeholder_text="Enter petition title"
        )
        title_entry.pack(fill="x", pady=(5, 0))
        
        # Document upload
        doc_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        doc_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            doc_frame,
            text="Petition Document:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w")
        
        upload_frame = ctk.CTkFrame(doc_frame, fg_color="#f1f5f9", corner_radius=6)
        upload_frame.pack(fill="x", pady=(5, 0))
        
        self.doc_label = ctk.CTkLabel(
            upload_frame,
            text="No document selected",
            font=ctk.CTkFont(size=12),
            text_color="#64748b"
        )
        self.doc_label.pack(side="left", padx=10, pady=8)
        
        ctk.CTkButton(
            upload_frame,
            text="Browse",
            font=ctk.CTkFont(size=12),
            fg_color="#1a237e",
            hover_color="#283593",
            width=80,
            command=self.browse_document
        ).pack(side="right", padx=10, pady=4)
        
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
            text="Submit Petition",
            fg_color="#1a237e",
            hover_color="#283593",
            width=100,
            command=self.submit_petition
        ).pack(side="right")
        
    def browse_document(self):
        file_path = filedialog.askopenfilename(
            title="Select Petition Document",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if file_path:
            self.document_path = file_path
            self.doc_label.configure(text=os.path.basename(file_path))
            
    def submit_petition(self):
        try:
            title = self.title_var.get().strip()
            
            if not title:
                raise ValueError("Please enter a petition title")
            if not self.document_path:
                raise ValueError("Please upload a petition document")
                
            # Copy document to petitions directory
            filename = f"petition_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
            dest_path = os.path.join("petitions", filename)
            shutil.copy2(self.document_path, dest_path)
            
            # Create petition data
            petition_data = {
                "id": datetime.now().strftime("%Y%m%d%H%M%S"),
                "title": title,
                "document": dest_path,
                "date": datetime.now(),
                "status": "Pending"
            }
            
            self.result = petition_data
            self.dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save petition: {str(e)}")

class ForwardToCommitteeDialog:
    def __init__(self, parent):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Forward to Committee")
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
        # Main content
        content_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(
            content_frame,
            text="Select Committee",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(0, 20))
        
        # Committees list
        committees_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        committees_frame.pack(fill="both", expand=True)
        
        self.committee_var = ctk.StringVar()
        
        committees = [
            "Public Accounts Committee",
            "Rules and Business Committee",
            "Ethics and Privileges Committee",
            "House Services Committee",
            "Selection Committee",
            "Public Petitions Committee"
        ]
        
        for committee in committees:
            ctk.CTkRadioButton(
                committees_frame,
                text=committee,
                variable=self.committee_var,
                value=committee,
                font=ctk.CTkFont(size=14),
                fg_color="#1a237e",
                hover_color="#283593"
            ).pack(anchor="w", pady=10)
            
        # Notes
        notes_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        notes_frame.pack(fill="x", pady=(20, 0))
        
        ctk.CTkLabel(
            notes_frame,
            text="Notes (optional):",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w")
        
        self.notes_text = ctk.CTkTextbox(
            notes_frame,
            height=100,
            font=ctk.CTkFont(size=12)
        )
        self.notes_text.pack(fill="x", pady=(5, 0))
        
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
            text="Forward",
            fg_color="#059669",
            hover_color="#047857",
            width=100,
            command=self.forward_petition
        ).pack(side="right")
        
    def forward_petition(self):
        try:
            committee = self.committee_var.get()
            notes = self.notes_text.get("1.0", "end-1c").strip()
            
            if not committee:
                raise ValueError("Please select a committee")
                
            # Create forward data
            forward_data = {
                "committee": committee,
                "notes": notes if notes else None,
                "date": datetime.now()
            }
            
            self.result = forward_data
            self.dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e)) 

class ApprovePetitionDialog:
    def __init__(self, parent):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Approve Petition")
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
        # Main content
        content_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(
            content_frame,
            text="Approve Petition",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(0, 20))
        
        # Notes
        notes_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        notes_frame.pack(fill="x", pady=(20, 0))
        
        ctk.CTkLabel(
            notes_frame,
            text="Notes (optional):",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w")
        
        self.notes_text = ctk.CTkTextbox(
            notes_frame,
            height=100,
            font=ctk.CTkFont(size=12)
        )
        self.notes_text.pack(fill="x", pady=(5, 0))
        
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
            text="Approve",
            fg_color="#059669",
            hover_color="#047857",
            width=100,
            command=self.approve_petition
        ).pack(side="right")
        
    def approve_petition(self):
        try:
            notes = self.notes_text.get("1.0", "end-1c").strip()
            
            if not notes:
                raise ValueError("Please enter notes")
                
            # Create approval data
            approval_data = {
                "notes": notes if notes else None,
                "date": datetime.now()
            }
            
            self.result = approval_data
            self.dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e)) 

class EditPetitionDialog:
    def __init__(self, parent, petition):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Edit Petition")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Store original petition data
        self.petition = petition
        self.document_path = None
        
        # Center dialog
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'+{x}+{y}')
        
        self.create_dialog_content()
        
    def create_dialog_content(self):
        content_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            title_frame,
            text="Petition Title:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w")
        
        self.title_var = ctk.StringVar(value=self.petition["title"])
        title_entry = ctk.CTkEntry(
            title_frame,
            textvariable=self.title_var,
            placeholder_text="Enter petition title"
        )
        title_entry.pack(fill="x", pady=(5, 0))
        
        # Current document info
        current_doc_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        current_doc_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            current_doc_frame,
            text="Current Document:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            current_doc_frame,
            text=os.path.basename(self.petition["document"]),
            font=ctk.CTkFont(size=12),
            text_color="#64748b"
        ).pack(anchor="w", pady=(5, 0))
        
        # New document upload (optional)
        doc_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        doc_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            doc_frame,
            text="Replace Document (optional):",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w")
        
        upload_frame = ctk.CTkFrame(doc_frame, fg_color="#f1f5f9", corner_radius=6)
        upload_frame.pack(fill="x", pady=(5, 0))
        
        self.doc_label = ctk.CTkLabel(
            upload_frame,
            text="No new document selected",
            font=ctk.CTkFont(size=12),
            text_color="#64748b"
        )
        self.doc_label.pack(side="left", padx=10, pady=8)
        
        ctk.CTkButton(
            upload_frame,
            text="Browse",
            font=ctk.CTkFont(size=12),
            fg_color="#1a237e",
            hover_color="#283593",
            width=80,
            command=self.browse_document
        ).pack(side="right", padx=10, pady=4)
        
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
            text="Save Changes",
            fg_color="#1a237e",
            hover_color="#283593",
            width=100,
            command=self.save_changes
        ).pack(side="right")
        
    def browse_document(self):
        file_path = filedialog.askopenfilename(
            title="Select New Document",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if file_path:
            self.document_path = file_path
            self.doc_label.configure(text=os.path.basename(file_path))
            
    def save_changes(self):
        try:
            title = self.title_var.get().strip()
            
            if not title:
                raise ValueError("Please enter a petition title")
                
            # Update petition data
            updated_data = {
                "title": title
            }
            
            # Handle document update if new one was selected
            if self.document_path:
                filename = f"petition_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
                dest_path = os.path.join("petitions", filename)
                shutil.copy2(self.document_path, dest_path)
                updated_data["document"] = dest_path
            
            self.result = updated_data
            self.dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save changes: {str(e)}") 