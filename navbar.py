import customtkinter as ctk
from PIL import Image
from access_control import AccessControl

class NavigationBar(ctk.CTkFrame):
    def __init__(self, parent, callback):
        super().__init__(
            parent,
            fg_color="#1a237e",
            width=300,
            corner_radius=0
        )
        
        # Store reference to parent window
        self.parent = parent
        
        # Store all after IDs
        self.after_ids = []
        
        # Main container for all nav elements
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=2)
        
        # Logo section
        self.create_logo_section()
        
        # Profile section
        self.create_profile_section()
        
        # Navigation items container with scrollable frame
        self.nav_container = ctk.CTkScrollableFrame(
            self.main_container,
            fg_color="transparent",
            scrollbar_fg_color="transparent",
            scrollbar_button_color="#3949ab",
            scrollbar_button_hover_color="#283593"
        )
        self.nav_container.pack(fill="both", expand=True, pady=(20, 0))
        
        # Navigation items
        self.create_navigation_items(callback)
        
        # Bind cleanup to window destroy event
        self.parent.bind("<Destroy>", self.cleanup)
        
    def cleanup(self, event=None):
        # Cancel all pending after events
        for after_id in self.after_ids:
            try:
                self.parent.after_cancel(after_id)
            except:
                pass
        self.after_ids.clear()
        
    def create_logo_section(self):
        logo_frame = ctk.CTkFrame(self.main_container, fg_color="transparent", height=70)
        logo_frame.pack(fill="x", pady=(10, 0))
        logo_frame.pack_propagate(False)
        
        # Container for logo and text
        logo_container = ctk.CTkFrame(logo_frame, fg_color="transparent")
        logo_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo image with reduced size (changed from 120x120 to 40x40)
        logo_image = ctk.CTkImage(
            light_image=Image.open("logo.png"),
            dark_image=Image.open("logo.png"),
            size=(40, 40)  # Reduced size here
        )
        
        # Logo label
        ctk.CTkLabel(
            logo_container,
            text="",
            image=logo_image
        ).pack(side="left", padx=(0, 10))
        
        # Title label
        ctk.CTkLabel(
            logo_container,
            text="H O A EKITI",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        ).pack(side="left")
        
    def create_profile_section(self):
        profile_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="#283593",  # Slightly lighter blue matching login theme
            corner_radius=15,
            height=80
        )
        profile_frame.pack(fill="x", padx=15, pady=(20, 0))
        
        # Profile header with hover effect
        profile_header = ctk.CTkButton(
            profile_frame,
            fg_color="transparent",
            hover_color="#3949ab",  # Hover color matching login theme
            corner_radius=10,
            height=70
        )
        profile_header.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95)
        
        # Profile circle
        profile_circle = ctk.CTkFrame(
            profile_header,
            width=45,
            height=45,
            corner_radius=25,
            fg_color="#3f51b5"  # Indigo color matching login theme
        )
        profile_circle.place(relx=0.1, rely=0.5, anchor="w")
        profile_circle.pack_propagate(False)
        
        # User initial
        ctk.CTkLabel(
            profile_circle,
            text="A",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        # User info container
        user_info = ctk.CTkFrame(profile_header, fg_color="transparent")
        user_info.place(relx=0.3, rely=0.5, anchor="w")
        
        ctk.CTkLabel(
            user_info,
            text="Admin User",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            user_info,
            text="Administrator",
            font=ctk.CTkFont(size=12),
            text_color="#94a3b8"
        ).pack(anchor="w")
        
        # Settings icon
        ctk.CTkLabel(
            profile_header,
            text="⚙️",
            font=ctk.CTkFont(size=16),
            text_color="#94a3b8"
        ).place(relx=0.9, rely=0.5, anchor="e")
        
    def create_navigation_items(self, callback):
        # Get permitted pages based on user's role
        permitted_pages = AccessControl.get_permitted_pages(self.parent.current_user["role"])
        
        nav_items = []
        
        # Only add nav items that user has permission for
        if "Dashboard" in permitted_pages:
            nav_items.append(("Dashboard", "🏠", True))
            
        if "Bills" in permitted_pages:
            nav_items.append(("Bills", "📜"))
            
        if "Order Paper" in permitted_pages:
            nav_items.append(("Order Paper", "📄"))
            
        if "Order of the Day" in permitted_pages:
            nav_items.append(("Order of the Day", "📄"))
            
        if "Petitions" in permitted_pages:
            nav_items.append(("Petitions", "⚖️"))
            
        if "Chat" in permitted_pages:
            nav_items.append(("Chat", "💬"))
            
        if "Voting" in permitted_pages:
            nav_items.append(("Voting", "✓"))
            
        if "Motions" in permitted_pages:
            nav_items.append(("Motions", "📌"))
            
        if "Documents" in permitted_pages:
            nav_items.append(("Documents", "📁"))
            
        if "Admin" in permitted_pages:
            nav_items.append(("Admin", "⚙️", True))
            
        nav_items.append(("Sign Out", "🚪", True))
        
        # Create navigation buttons
        for item in nav_items:
            if len(item) > 2 and item[2]:
                separator = ctk.CTkFrame(self.nav_container, fg_color="#3949ab", height=1)
                separator.pack(fill="x", padx=15, pady=10)
            
            text, icon = item[0], item[1]
            
            # Create button container for hover effect
            button_container = ctk.CTkFrame(self.nav_container, fg_color="transparent")
            button_container.pack(fill="x", pady=2)
            
            button = ctk.CTkButton(
                button_container,
                text=f"{icon}  {text}",
                font=ctk.CTkFont(size=14),
                fg_color="transparent",
                text_color="#90caf9" if text != "Sign Out" else "#ff8a80",
                hover_color="#283593",
                anchor="w",
                height=45,
                corner_radius=8,
                command=lambda t=text: callback(t)
            )
            button.pack(fill="x", padx=15)
            
            # Add active indicator for Dashboard
            if text == "Dashboard":
                indicator = ctk.CTkFrame(button_container, fg_color="#90caf9", width=3)
                indicator.place(rely=0.5, relheight=0.7, anchor="w")
        
    def create_nav_items(self):
        items = [
            {
                "id": "order_papers",
                "icon": "📜",
                "text": "Order Papers"
            },
            {
                "id": "petitions",
                "icon": "⚖️",
                "text": "Petitions"
            },
            # ... other items ...
        ] 