import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox, filedialog
import os
import shutil
from document_viewer import DocumentViewer

class OrderPaperContent(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=1, sticky="nsew")
        self.configure(fg_color="#f1f5f9")
        
        # Store papers data
        self.papers = []
        self.selected_paper = None
        
        # Create documents directory if it doesn't exist
        self.docs_dir = "documents"
        if not os.path.exists(self.docs_dir):
            os.makedirs(self.docs_dir)
        
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
        
        # Title with icon
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left", padx=30)
        
        ctk.CTkLabel(
            title_frame,
            text="📜",
            font=ctk.CTkFont(size=24)
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            title_frame,
            text="Order Papers",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left")
        
        # Right side buttons
        buttons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        buttons_frame.pack(side="right", padx=30)
        
        # Upload Document button
        self.upload_button = ctk.CTkButton(
            buttons_frame,
            text="📎 Upload Document",
            font=ctk.CTkFont(size=12),
            fg_color="#6366f1",
            hover_color="#4f46e5",
            height=35,
            command=self.upload_document
        )
        self.upload_button.pack(side="right", padx=5)
        
        # New Paper button
        self.new_paper_button = ctk.CTkButton(
            buttons_frame,
            text="+ New Paper",
            font=ctk.CTkFont(size=12),
            fg_color="#1a237e",
            hover_color="#283593",
            height=35,
            command=self.create_new_paper
        )
        self.new_paper_button.pack(side="right", padx=5)
        
        # Publish button
        self.publish_button = ctk.CTkButton(
            buttons_frame,
            text="Publish Paper",
            font=ctk.CTkFont(size=12),
            fg_color="#059669",
            hover_color="#047857",
            height=35,
            state="disabled",
            command=self.publish_paper
        )
        self.publish_button.pack(side="right", padx=5)
        
    def create_stats_bar(self):
        """Create statistics bar below header"""
        stats_frame = ctk.CTkFrame(self, fg_color="white", height=100)
        stats_frame.pack(fill="x", padx=0, pady=(0, 2))
        stats_frame.pack_propagate(False)
        
        # Stats container
        container = ctk.CTkFrame(stats_frame, fg_color="transparent")
        container.pack(padx=30, pady=20, fill="x")
        
        # Statistics
        stats = [
            {
                "title": "Total Papers",
                "value": len(self.papers),
                "icon": "📚",
                "color": "#6366f1",
                "bg_color": "#e0e7ff"  # Light indigo
            },
            {
                "title": "Published",
                "value": sum(1 for p in self.papers if p["status"] == "Published"),
                "icon": "✅",
                "color": "#10b981",
                "bg_color": "#d1fae5"  # Light emerald
            },
            {
                "title": "Drafts",
                "value": sum(1 for p in self.papers if p["status"] == "Draft"),
                "icon": "📝",
                "color": "#f59e0b",
                "bg_color": "#fef3c7"  # Light amber
            },
            {
                "title": "With Documents",
                "value": sum(1 for p in self.papers if p.get("document_path")),
                "icon": "📎",
                "color": "#8b5cf6",
                "bg_color": "#ede9fe"  # Light violet
            }
        ]
        
        for i, stat in enumerate(stats):
            stat_frame = ctk.CTkFrame(container, fg_color="transparent")
            stat_frame.grid(row=0, column=i, padx=15, sticky="ew")
            container.grid_columnconfigure(i, weight=1)
            
            # Icon and value
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
            text="No Order Papers",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(40, 10))
        
        ctk.CTkLabel(
            empty_frame,
            text="Click '+ New Paper' to create a new order paper",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack()
        
    def create_new_paper(self):
        dialog = NewPaperDialog(self)
        self.wait_window(dialog.dialog)
        
        if hasattr(dialog, 'result'):
            self.papers.append(dialog.result)
            self.show_papers_list()
            
    def show_papers_list(self):
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        if not self.papers:
            self.show_empty_state()
            return
            
        # Papers grid
        for paper in self.papers:
            self.create_paper_card(paper)
            
    def create_paper_card(self, paper):
        card = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=15)
        card.pack(fill="x", pady=(0, 15))
        
        # Add hover effect
        def on_enter(e):
            card.configure(fg_color="#f8fafc")
            
        def on_leave(e):
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
        
        doc_icon = "📄" if paper.get("document_path") else "📝"
        ctk.CTkLabel(
            icon_frame,
            text=doc_icon,
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
            text=f"Paper No. {paper['number']}",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left")
        
        date_frame = ctk.CTkFrame(
            header_frame,
            fg_color="#f1f5f9",
            corner_radius=6
        )
        date_frame.pack(side="right")
        
        ctk.CTkLabel(
            date_frame,
            text=f"📅 {paper['date'].strftime('%B %d, %Y')}",
            font=ctk.CTkFont(size=12),
            text_color="#64748b"
        ).pack(padx=8, pady=4)
        
        # Description
        ctk.CTkLabel(
            info_frame,
            text=paper["description"],
            font=ctk.CTkFont(size=14),
            text_color="#334155",
            wraplength=600
        ).pack(anchor="w", pady=(5, 0))
        
        # Right side actions
        actions_frame = ctk.CTkFrame(content, fg_color="transparent")
        actions_frame.pack(side="right", padx=(15, 0))
        
        # Action buttons
        if paper.get("document_path"):
            view_button = ctk.CTkButton(
                actions_frame,
                text="View Document",
                font=ctk.CTkFont(size=12),
                fg_color="#6366f1",
                hover_color="#4f46e5",
                height=32,
                image=None,
                command=lambda: self.view_document(paper["document_path"])
            )
            view_button.pack(side="right", padx=(10, 0))
        
        # Status badge
        status_colors = {
            "Draft": ("#f1f5f9", "#64748b", "⚪"),
            "Published": ("#dcfce7", "#16a34a", "✓"),
            "Archived": ("#fef3c7", "#d97706", "📦")
        }
        
        bg_color, text_color, icon = status_colors.get(paper["status"])
        status_label = ctk.CTkFrame(
            actions_frame,
            fg_color=bg_color,
            corner_radius=6
        )
        status_label.pack(side="right")
        
        ctk.CTkLabel(
            status_label,
            text=f"{icon} {paper['status']}",
            font=ctk.CTkFont(size=12),
            text_color=text_color
        ).pack(padx=10, pady=4)
        
        # Update card click binding to select paper
        card.bind("<Button-1>", lambda e, p=paper: self.select_paper(p))
        
        # Add selection indicator
        if self.selected_paper and self.selected_paper["number"] == paper["number"]:
            card.configure(fg_color="#f1f5f9")  # Show as selected

    def upload_document(self):
        file_path = filedialog.askopenfilename(
            title="Select Document",
            filetypes=[
                ("PDF files", "*.pdf"),
                ("Word files", "*.docx"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Create unique filename
                filename = os.path.basename(file_path)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_filename = f"{timestamp}_{filename}"
                destination = os.path.join(self.docs_dir, new_filename)
                
                # Copy file to documents directory
                shutil.copy2(file_path, destination)
                
                # Create new paper with document
                dialog = NewPaperDialog(self, document_path=destination)
                self.wait_window(dialog.dialog)
                
                if hasattr(dialog, 'result'):
                    self.papers.append(dialog.result)
                    self.show_papers_list()
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to upload document: {str(e)}")

    def view_document(self, document_path):
        try:
            if not os.path.exists(document_path):
                messagebox.showerror("Error", "Document file not found")
                return
            
            # Get the main window (root)
            root = self.winfo_toplevel()
            
            viewer = DocumentViewer(root, document_path)  # Pass root as parent
            
        except ModuleNotFoundError:
            messagebox.showerror(
                "Error",
                "Required modules not found. Please install PyMuPDF and Pillow:\n" +
                "pip install PyMuPDF Pillow"
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Could not open document: {str(e)}\n" +
                "Make sure you have the required modules installed."
            )

    def select_paper(self, paper):
        """Select a paper and enable publish button if it's in draft"""
        self.selected_paper = paper
        
        # Enable/disable publish button based on paper status
        if paper["status"] == "Draft":
            self.publish_button.configure(state="normal")
        else:
            self.publish_button.configure(state="disabled")

    def publish_paper(self):
        """Publish the selected paper"""
        if not self.selected_paper:
            return
        
        # Confirm before publishing
        if messagebox.askyesno(
            "Confirm Publish",
            "Are you sure you want to publish this paper? This action cannot be undone."
        ):
            # Update paper status
            self.selected_paper["status"] = "Published"
            
            # Update stats and refresh display
            self.show_papers_list()
            self.create_stats_bar()  # Refresh stats
            
            # Reset selection and disable publish button
            self.selected_paper = None
            self.publish_button.configure(state="disabled")
            
            messagebox.showinfo(
                "Success",
                "Paper has been published successfully"
            )

class NewPaperDialog:
    def __init__(self, parent, document_path=None):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Create New Order Paper")
        self.dialog.geometry("600x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.document_path = document_path
        
        # Center the dialog
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'+{x}+{y}')
        
        self.create_dialog_content()
        
    def create_dialog_content(self):
        # Paper Info
        info_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        info_frame.pack(fill="x", padx=20, pady=20)
        
        # Paper number
        number_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        number_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            number_frame,
            text="Paper Number:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w")
        
        self.number_var = ctk.StringVar()
        number_entry = ctk.CTkEntry(
            number_frame,
            textvariable=self.number_var,
            placeholder_text="Enter paper number"
        )
        number_entry.pack(fill="x", pady=(5, 0))
        
        # Date
        date_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        date_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            date_frame,
            text="Date:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w")
        
        self.date_var = ctk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        date_entry = ctk.CTkEntry(
            date_frame,
            textvariable=self.date_var
        )
        date_entry.pack(fill="x", pady=(5, 0))
        
        # Description
        desc_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        desc_frame.pack(fill="x")
        
        ctk.CTkLabel(
            desc_frame,
            text="Description:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w")
        
        self.desc_var = ctk.StringVar()
        desc_entry = ctk.CTkEntry(
            desc_frame,
            textvariable=self.desc_var,
            placeholder_text="Enter paper description"
        )
        desc_entry.pack(fill="x", pady=(5, 0))
        
        if self.document_path:
            # Show attached document info
            doc_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            doc_frame.pack(fill="x", pady=(15, 0))
            
            ctk.CTkLabel(
                doc_frame,
                text="Attached Document:",
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(anchor="w")
            
            doc_info = ctk.CTkFrame(doc_frame, fg_color="#f1f5f9", corner_radius=6)
            doc_info.pack(fill="x", pady=(5, 0))
            
            ctk.CTkLabel(
                doc_info,
                text=f"📄 {os.path.basename(self.document_path)}",
                font=ctk.CTkFont(size=12),
                text_color="#64748b"
            ).pack(padx=10, pady=8)
        
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
            text="Create Paper",
            fg_color="#1a237e",
            hover_color="#283593",
            width=100,
            command=self.create_paper
        ).pack(side="right")
        
    def create_paper(self):
        try:
            number = self.number_var.get().strip()
            date = datetime.strptime(self.date_var.get(), "%Y-%m-%d")
            description = self.desc_var.get().strip()
            
            if not all([number, description]):
                raise ValueError("All fields are required")
                
            # Create paper data
            paper_data = {
                "number": number,
                "date": date,
                "description": description,
                "status": "Draft",  # Always start as draft
                "items": [],
                "document_path": self.document_path
            }
            
            self.result = paper_data
            self.dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e)) 