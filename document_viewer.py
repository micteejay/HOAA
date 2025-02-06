import customtkinter as ctk
from tkinter import messagebox
import fitz  # PyMuPDF
from PIL import Image
import io

class DocumentViewer:
    def __init__(self, parent, file_path):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Document Viewer")
        self.dialog.geometry("800x600")
        
        self.file_path = file_path
        self.current_page = 0
        self.zoom_level = 1.0
        
        # Center dialog
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'+{x}+{y}')
        
        self.create_viewer()
        
    def create_viewer(self):
        # Toolbar
        toolbar = ctk.CTkFrame(self.dialog)
        toolbar.pack(fill="x", padx=10, pady=5)
        
        # Navigation buttons
        ctk.CTkButton(
            toolbar,
            text="Previous",
            command=self.prev_page
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            toolbar,
            text="Next",
            command=self.next_page
        ).pack(side="left", padx=5)
        
        # Zoom buttons
        ctk.CTkButton(
            toolbar,
            text="Zoom In",
            command=self.zoom_in
        ).pack(side="right", padx=5)
        
        ctk.CTkButton(
            toolbar,
            text="Zoom Out",
            command=self.zoom_out
        ).pack(side="right", padx=5)
        
        # Document view
        self.view_frame = ctk.CTkScrollableFrame(self.dialog)
        self.view_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Load document
        self.load_document()
        
    def load_document(self):
        try:
            self.doc = fitz.open(self.file_path)
            self.show_page()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load document: {str(e)}")
            
    def show_page(self):
        # Clear current view
        for widget in self.view_frame.winfo_children():
            widget.destroy()
            
        # Get page
        page = self.doc[self.current_page]
        
        # Render page
        zoom = self.zoom_level
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        
        # Convert to PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Show image
        img_tk = ctk.CTkImage(img, size=(pix.width, pix.height))
        label = ctk.CTkLabel(self.view_frame, image=img_tk, text="")
        label.image = img_tk
        label.pack(expand=True)
        
    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page()
            
    def next_page(self):
        if self.current_page < len(self.doc) - 1:
            self.current_page += 1
            self.show_page()
            
    def zoom_in(self):
        self.zoom_level *= 1.2
        self.show_page()
        
    def zoom_out(self):
        self.zoom_level /= 1.2
        self.show_page()
        
    def show(self):
        self.dialog.grab_set()
        self.dialog.focus_set() 