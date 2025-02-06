import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox, filedialog
import os
import shutil
from document_viewer import DocumentViewer

class DocumentContent(ctk.CTkFrame):
    def __init__(self, parent, current_user, is_admin=False):
        super().__init__(parent)
        
        # Store user info
        self.current_user = current_user
        self.is_admin = is_admin
        
        # Configure frame
        self.configure(fg_color="#f1f5f9")
        
        # Store documents data
        self.documents = []
        self.selected_doc = None
        
        # Create document categories
        self.categories = {
            "Bills": "📜",
            "Laws": "⚖️",
            "Reports": "📊",
            "Minutes": "📝",
            "Hansards": "📚",
            "Circulars": "📢",
            "Others": "📁"
        }
        
        # Create documents directory structure
        self.base_dir = "documents"
        self.create_directory_structure()
        
        # Create UI sections
        self.create_header()
        self.create_stats_bar()
        self.create_content()
        
    def create_directory_structure(self):
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
            
        for category in self.categories.keys():
            category_path = os.path.join(self.base_dir, category)
            if not os.path.exists(category_path):
                os.makedirs(category_path)
                
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
            text="📁",
            font=ctk.CTkFont(size=24)
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            title_frame,
            text="Documents",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#000000"
        ).pack(side="left")
        
        # Right side buttons
        buttons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        buttons_frame.pack(side="right", padx=30)
        
        # Upload Document button
        self.upload_button = ctk.CTkButton(
            buttons_frame,
            text="+ Upload Document",
            font=ctk.CTkFont(size=12),
            fg_color="#1a237e",
            hover_color="#283593",
            height=35,
            command=self.upload_document
        )
        self.upload_button.pack(side="right", padx=5)
        
    def create_stats_bar(self):
        stats_frame = ctk.CTkFrame(self, fg_color="white", height=100)
        stats_frame.pack(fill="x", padx=0, pady=(0, 2))
        stats_frame.pack_propagate(False)
        
        container = ctk.CTkFrame(stats_frame, fg_color="transparent")
        container.pack(padx=30, pady=20, fill="x")
        
        # Calculate stats
        total_docs = sum(len(os.listdir(os.path.join(self.base_dir, cat))) 
                        for cat in self.categories)
        
        stats = [
            {
                "title": "Total Documents",
                "value": total_docs,
                "icon": "📁",
                "color": "#6366f1",
                "bg_color": "#e0e7ff"
            }
        ]
        
        # Add category stats
        for category, icon in self.categories.items():
            cat_count = len(os.listdir(os.path.join(self.base_dir, category)))
            stats.append({
                "title": category,
                "value": cat_count,
                "icon": icon,
                "color": "#1a237e",
                "bg_color": "#e8eaf6"
            }) 

    def create_content(self):
        # Create main content area with tabs
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Create tabs for categories
        tabs_frame = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=15)
        tabs_frame.pack(fill="x", pady=(0, 15))
        
        for category in self.categories.keys():
            tab = ctk.CTkButton(
                tabs_frame,
                text=f"{self.categories[category]} {category}",
                font=ctk.CTkFont(size=14),
                fg_color="transparent",
                text_color="#000000",
                hover_color="#e8eaf6",
                anchor="w",
                command=lambda c=category: self.show_category(c)
            )
            tab.pack(side="left", padx=15, pady=10)
        
        # Documents list area
        self.docs_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent"
        )
        self.docs_frame.pack(fill="both", expand=True)
        
        # Show all documents initially
        self.show_category("All")

    def show_category(self, category):
        # Clear current documents
        for widget in self.docs_frame.winfo_children():
            widget.destroy()
        
        if category == "All":
            # Show documents from all categories
            for cat in self.categories.keys():
                self.show_category_documents(cat)
        else:
            # Show documents from selected category
            self.show_category_documents(category)

    def show_category_documents(self, category):
        category_path = os.path.join(self.base_dir, category)
        documents = os.listdir(category_path)
        
        if documents:
            # Category header
            header = ctk.CTkFrame(self.docs_frame, fg_color="transparent")
            header.pack(fill="x", pady=(0, 10))
            
            ctk.CTkLabel(
                header,
                text=f"{self.categories[category]} {category}",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#000000"
            ).pack(side="left")
            
            # Documents grid
            for doc in documents:
                self.create_document_card(category, doc)
        
    def create_document_card(self, category, filename):
        card = ctk.CTkFrame(self.docs_frame, fg_color="white", corner_radius=15)
        card.pack(fill="x", pady=(0, 15))
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=20)
        
        # Icon and filename
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            header,
            text="📄",
            font=ctk.CTkFont(size=24)
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            header,
            text=filename,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#000000"
        ).pack(side="left")
        
        # Action buttons
        actions = ctk.CTkFrame(content, fg_color="transparent")
        actions.pack(fill="x")
        
        ctk.CTkButton(
            actions,
            text="View",
            font=ctk.CTkFont(size=12),
            fg_color="#1a237e",
            hover_color="#283593",
            width=80,
            command=lambda: self.view_document(category, filename)
        ).pack(side="right", padx=5)

    def view_document(self, category, filename):
        file_path = os.path.join(self.base_dir, category, filename)
        viewer = DocumentViewer(self, file_path)
        viewer.show()

    def upload_document(self):
        file_path = filedialog.askopenfilename(
            title="Select Document",
            filetypes=[
                ("PDF files", "*.pdf"),
                ("Word files", "*.doc;*.docx"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            dialog = UploadDocumentDialog(self, file_path)
            self.wait_window(dialog.dialog)
            
            if hasattr(dialog, 'result'):
                category = dialog.result["category"]
                filename = os.path.basename(file_path)
                dest_path = os.path.join(self.base_dir, category, filename)
                
                # Copy file to appropriate category folder
                shutil.copy2(file_path, dest_path)
                
                # Refresh display
                self.create_stats_bar()
                self.show_category("All") 

class UploadDocumentDialog:
    def __init__(self, parent, file_path):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Upload Document")
        self.dialog.geometry("400x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Configure dark theme
        self.dialog.configure(fg_color="#1a1a1a")  # Dark background
        
        self.file_path = file_path
        
        # Center dialog
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'+{x}+{y}')
        
        self.create_dialog_content()
        
    def create_dialog_content(self):
        # File info
        info_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        info_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            info_frame,
            text="Selected File:",
            font=ctk.CTkFont(size=14),
            text_color="white"
        ).pack(anchor="w")
        
        file_info = ctk.CTkFrame(info_frame, fg_color="#2d2d2d", corner_radius=6)
        file_info.pack(fill="x", pady=(5, 0))
        
        ctk.CTkLabel(
            file_info,
            text=f"📄 {os.path.basename(self.file_path)}",
            font=ctk.CTkFont(size=12),
            text_color="white"
        ).pack(padx=10, pady=8)
        
        # Document category
        category_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        category_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(
            category_frame,
            text="Document Category:",
            font=ctk.CTkFont(size=14),
            text_color="white"
        ).pack(anchor="w")
        
        # Category options with dark theme
        categories = [
            ("📜 Bills", "Bills"),
            ("⚖️ Laws", "Laws"),
            ("📊 Reports", "Reports"),
            ("📝 Minutes", "Minutes"),
            ("📚 Hansards", "Hansards"),
            ("📢 Circulars", "Circulars"),
            ("📁 Others", "Others")
        ]
        
        self.category_var = ctk.StringVar(value="Bills")  # Default to Bills
        
        options_frame = ctk.CTkFrame(category_frame, fg_color="transparent")
        options_frame.pack(fill="x", pady=(5, 0))
        
        for i, (label, value) in enumerate(categories):
            row = i // 2
            col = i % 2
            
            radio = ctk.CTkRadioButton(
                options_frame,
                text=label,
                variable=self.category_var,
                value=value,
                font=ctk.CTkFont(size=12),
                text_color="white",
                fg_color="#1a237e",
                border_color="gray",
                hover_color="#283593"
            )
            radio.grid(row=row, column=col, padx=10, pady=5, sticky="w")
            
        options_frame.grid_columnconfigure(0, weight=1)
        options_frame.grid_columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(
            button_frame,
            text="Upload",
            font=ctk.CTkFont(size=12),
            fg_color="#1a237e",
            hover_color="#283593",
            width=100,
            command=self.upload_document
        ).pack(side="right", padx=(10, 0))
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            font=ctk.CTkFont(size=12),
            fg_color="#dc2626",  # Red color
            hover_color="#b91c1c",
            width=100,
            command=self.dialog.destroy
        ).pack(side="right")
        
    def upload_document(self):
        try:
            category = self.category_var.get()
            
            if not category:
                raise ValueError("Please select a document category")
                
            self.result = {
                "category": category
            }
            
            self.dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e)) 