import customtkinter as ctk

class DashboardContent(ctk.CTkFrame):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        self.configure(fg_color="#f1f5f9")
        
        # Placeholder content
        ctk.CTkLabel(
            self,
            text="Dashboard Content",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)

class OrderPaperContent(ctk.CTkFrame):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        self.configure(fg_color="#f1f5f9")
        
        # Placeholder content
        ctk.CTkLabel(
            self,
            text="Order Paper Content",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)

class OrderOfDayContent(ctk.CTkFrame):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        self.configure(fg_color="#f1f5f9")
        
        # Placeholder content
        ctk.CTkLabel(
            self,
            text="Order of Day Content",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)

class PetitionContent(ctk.CTkFrame):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        self.configure(fg_color="#f1f5f9")
        
        # Placeholder content
        ctk.CTkLabel(
            self,
            text="Petition Content",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)

class AIChatContent(ctk.CTkFrame):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        self.configure(fg_color="#f1f5f9")
        
        # Placeholder content
        ctk.CTkLabel(
            self,
            text="AI Chat Content",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20) 