import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime
import os
import fitz  # Add this import at the top
from PIL import Image, ImageTk

class BillContent(ctk.CTkFrame):
    def __init__(self, parent, current_user, is_admin=False):
        super().__init__(parent)
        
        # Store user info
        self.current_user = current_user
        self.is_admin = is_admin
        self.parent = parent
        self.data_manager = parent.data_manager
        
        # Configure frame
        self.configure(fg_color="#f1f5f9")
        
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
            text="📜",
            font=ctk.CTkFont(size=24)
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            title_frame,
            text="Bills",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#000000"
        ).pack(side="left")
        
        # Right side buttons - Only show for admin users
        if self.is_admin:
            buttons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
            buttons_frame.pack(side="right", padx=30)
            
            # New Bill button
            self.new_bill_button = ctk.CTkButton(
                buttons_frame,
                text="+ New Bill",
                font=ctk.CTkFont(size=12),
                fg_color="#1a237e",
                hover_color="#283593",
                height=35,
                command=self.create_bill
            )
            self.new_bill_button.pack(side="right", padx=5)
        
    def create_content(self):
        self.content_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Show empty state or bills list
        self.show_bills_list()
        
    def show_bills_list(self):
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Get bills from data manager
        bills = self.data_manager.get_bills()
            
        if not bills:
            self.show_empty_state()
        else:
            for bill in bills:
                self.create_bill_card(bill)
                
    def show_empty_state(self):
        empty_frame = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=15)
        empty_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            empty_frame,
            text="No Bills Yet",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(40, 10))
        
        ctk.CTkLabel(
            empty_frame,
            text="There are no bills in the system",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack()
        
    def create_bill(self):
        dialog = NewBillDialog(self)
        self.wait_window(dialog.dialog)
        
        if hasattr(dialog, 'result'):
            # Add timestamp and metadata
            bill_data = {
                **dialog.result,
                "id": str(datetime.now().timestamp()),
                "date": datetime.now(),
                "created_by": self.current_user["username"],
                "status": "Draft"
            }
            
            # Save to data manager
            self.data_manager.add_bill(bill_data)
            
            # Refresh the list
            self.show_bills_list()

    def create_bill_card(self, bill):
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
            text=bill["title"],
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#000000"
        ).pack(side="left")
        
        # Bill type badge
        type_frame = ctk.CTkFrame(
            header,
            fg_color="#f1f5f9",
            corner_radius=6
        )
        type_frame.pack(side="right")
        
        ctk.CTkLabel(
            type_frame,
            text=bill["type"],
            font=ctk.CTkFont(size=12),
            text_color="#64748b"
        ).pack(padx=10, pady=4)
        
        # Bill description
        ctk.CTkLabel(
            content,
            text=bill["description"],
            font=ctk.CTkFont(size=14),
            text_color="#000000",
            wraplength=800,
            justify="left"
        ).pack(anchor="w", pady=(0, 15))
        
        # Document section
        if "document" in bill and bill["document"]:
            doc_frame = ctk.CTkFrame(content, fg_color="#f8fafc", corner_radius=10)
            doc_frame.pack(fill="x", pady=(0, 15))
            
            doc_content = ctk.CTkFrame(doc_frame, fg_color="transparent")
            doc_content.pack(fill="x", padx=15, pady=10)
            
            # Document icon and name
            doc_icon = ctk.CTkLabel(
                doc_content,
                text="📄",
                font=ctk.CTkFont(size=16)
            )
            doc_icon.pack(side="left", padx=(0, 10))
            
            doc_name = ctk.CTkLabel(
                doc_content,
                text=os.path.basename(bill["document"]),
                font=ctk.CTkFont(size=12),
                text_color="#1e293b"
            )
            doc_name.pack(side="left", fill="x", expand=True)
            
            # View button
            view_btn = ctk.CTkButton(
                doc_content,
                text="View Document",
                font=ctk.CTkFont(size=12),
                fg_color="#1a237e",
                hover_color="#283593",
                width=120,
                command=lambda: self.view_document(bill["document"])
            )
            view_btn.pack(side="right")
        
        # Footer with metadata
        footer = ctk.CTkFrame(content, fg_color="transparent")
        footer.pack(fill="x", pady=(15, 0))
        
        # Created by and date
        info = ctk.CTkFrame(footer, fg_color="transparent")
        info.pack(side="left")
        
        ctk.CTkLabel(
            info,
            text=f"Created by {bill['created_by']}",
            font=ctk.CTkFont(size=12),
            text_color="#64748b"
        ).pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(
            info,
            text=bill["date"].strftime("%Y-%m-%d %H:%M"),
            font=ctk.CTkFont(size=12),
            text_color="#64748b"
        ).pack(side="left")
        
        # Status badge
        status_colors = {
            "Draft": ("#fef3c7", "#d97706", "📝"),
            "In Review": ("#e0e7ff", "#4f46e5", "👀"),
            "Passed": ("#d1fae5", "#059669", "✅"),
            "Rejected": ("#fee2e2", "#dc2626", "❌")
        }
        
        status_info = status_colors.get(
            bill["status"], 
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
            text=f"{icon} {bill['status']}",
            font=ctk.CTkFont(size=12),
            text_color=text_color
        ).pack(padx=10, pady=4) 

    def view_document(self, file_path):
        """Open document in in-app viewer"""
        try:
            DocumentViewerDialog(self, file_path, os.path.basename(file_path))
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Could not open the document: {str(e)}"
            )

class NewBillDialog:
    def __init__(self, parent):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("New Bill")
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
        
        self.attached_file = None  # Store attached file path
        
    def create_dialog_content(self):
        # Title
        ctk.CTkLabel(
            self.dialog,
            text="New Bill",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)
        
        # Form container
        form = ctk.CTkFrame(self.dialog, fg_color="transparent")
        form.pack(fill="x", padx=20)
        
        # Bill Title
        ctk.CTkLabel(
            form,
            text="Bill Title:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w")
        
        self.title_var = ctk.StringVar()
        ctk.CTkEntry(
            form,
            textvariable=self.title_var,
            height=35
        ).pack(fill="x", pady=(5, 15))
        
        # Bill Type
        ctk.CTkLabel(
            form,
            text="Bill Type:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w")
        
        self.bill_type = ctk.StringVar(value="Regular")
        types_frame = ctk.CTkFrame(form, fg_color="transparent")
        types_frame.pack(fill="x", pady=(5, 15))
        
        bill_types = ["Regular", "Emergency", "Amendment", "Private Member"]
        for btype in bill_types:
            ctk.CTkRadioButton(
                types_frame,
                text=btype,
                variable=self.bill_type,
                value=btype,
                font=ctk.CTkFont(size=12)
            ).pack(side="left", padx=10)
        
        # Bill Description
        ctk.CTkLabel(
            form,
            text="Bill Description:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w")
        
        self.description = ctk.CTkTextbox(
            form,
            height=200
        )
        self.description.pack(fill="x", pady=(5, 15))
        
        # Supporting Documents
        ctk.CTkLabel(
            form,
            text="Supporting Documents:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w")
        
        # Store docs_frame as instance variable
        self.docs_frame = ctk.CTkFrame(form, fg_color="transparent")
        self.docs_frame.pack(fill="x", pady=(5, 15))
        
        self.file_button = ctk.CTkButton(
            self.docs_frame,
            text="Attach Files",
            font=ctk.CTkFont(size=12),
            fg_color="#1a237e",
            hover_color="#283593",
            command=self.attach_files
        )
        self.file_button.pack(side="left")
        
        # Buttons
        buttons = ctk.CTkFrame(self.dialog, fg_color="transparent")
        buttons.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(
            buttons,
            text="Submit",
            font=ctk.CTkFont(size=14),
            fg_color="#1a237e",
            hover_color="#283593",
            command=self.submit_bill
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
        file = filedialog.askopenfilename(
            title="Select Bill Document",
            filetypes=[
                ("PDF files", "*.pdf"),
                ("Word files", "*.doc;*.docx"),
                ("All files", "*.*")
            ]
        )
        if file:
            # Store the file path
            self.attached_file = file
            
            # Update button text to show selected file
            filename = os.path.basename(file)
            for widget in self.docs_frame.winfo_children():
                if isinstance(widget, ctk.CTkButton):
                    widget.configure(text=f"Change File ({filename})")
                    break
            
    def submit_bill(self):
        try:
            title = self.title_var.get().strip()
            description = self.description.get("1.0", "end-1c").strip()
            
            if not title:
                raise ValueError("Please enter a bill title")
            if not description:
                raise ValueError("Please enter the bill description")
            if not self.attached_file:
                raise ValueError("Please attach a bill document")
                
            # Create bill data
            self.result = {
                "title": title,
                "type": self.bill_type.get(),
                "description": description,
                "document": self.attached_file
            }
            
            self.dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e)) 

class DocumentViewerDialog:
    def __init__(self, parent, file_path, title):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title(f"Viewing: {title}")
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
        
        # Create viewer content
        self.create_viewer(file_path)
        
    def create_viewer(self, file_path):
        # Header with controls
        header = ctk.CTkFrame(self.dialog, fg_color="white", height=50)
        header.pack(fill="x", pady=(0, 2))
        header.pack_propagate(False)
        
        # Controls
        controls = ctk.CTkFrame(header, fg_color="transparent")
        controls.pack(side="right", padx=20)
        
        # Open externally button
        ctk.CTkButton(
            controls,
            text="📂 Open Externally",
            width=120,
            font=ctk.CTkFont(size=12),
            fg_color="#059669",
            hover_color="#047857",
            command=lambda: os.startfile(file_path)
        ).pack(side="left", padx=5)
        
        # Document viewer frame
        self.viewer_frame = ctk.CTkScrollableFrame(
            self.dialog,
            fg_color="white"
        )
        self.viewer_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Document content
        try:
            if file_path.lower().endswith('.pdf'):
                self.display_pdf(file_path)
            elif file_path.endswith(('.txt', '.md', '.py')):
                self.display_text(file_path)
            else:
                self.show_unsupported_message()
                
        except Exception as e:
            self.show_error_message(str(e))
            
    def display_pdf(self, file_path):
        try:
            # Open PDF document
            doc = fitz.open(file_path)
            
            # Create frame for each page
            for page_num in range(len(doc)):
                page = doc[page_num]
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for better quality
                
                # Convert to CTkImage
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                ctk_image = ctk.CTkImage(
                    light_image=img,
                    dark_image=img,
                    size=(pix.width, pix.height)
                )
                
                # Create page frame
                page_frame = ctk.CTkFrame(self.viewer_frame, fg_color="white")
                page_frame.pack(fill="x", pady=(0, 20))
                
                # Add page label
                label = ctk.CTkLabel(
                    page_frame,
                    text="",  # Empty text since we're using image
                    image=ctk_image
                )
                label.image = ctk_image  # Keep reference to prevent garbage collection
                label.pack(pady=10)
                
            doc.close()
            
        except Exception as e:
            self.show_error_message(f"Error loading PDF: {str(e)}")
            
    def display_text(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        text_widget = ctk.CTkTextbox(
            self.viewer_frame,
            wrap="word",
            font=ctk.CTkFont(family="Courier", size=12)
        )
        text_widget.pack(fill="both", expand=True)
        text_widget.insert("1.0", content)
        text_widget.configure(state="disabled")
            
    def show_unsupported_message(self):
        ctk.CTkLabel(
            self.viewer_frame,
            text="Preview not available for this file type.\nClick 'Open Externally' to view.",
            font=ctk.CTkFont(size=14)
        ).pack(pady=50)
                
    def show_error_message(self, error_text):
        ctk.CTkLabel(
            self.viewer_frame,
            text=f"Error loading document:\n{error_text}",
            font=ctk.CTkFont(size=14),
            text_color="#dc2626"
        ).pack(pady=50) 