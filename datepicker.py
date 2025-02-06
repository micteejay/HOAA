import customtkinter as ctk
from datetime import datetime
import calendar

class DatePicker(ctk.CTkToplevel):
    def __init__(self, parent, selected_date=None):
        super().__init__(parent)
        self.title("Select Date")
        self.geometry("300x400")
        self.resizable(False, False)
        
        # Center the dialog
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')
        
        # Initialize variables
        self.selected_date = selected_date or datetime.now()
        self.current_date = self.selected_date
        self.callback = None
        
        self.create_calendar()
        
    def create_calendar(self):
        # Create main container
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Month and Year selector
        header = ctk.CTkFrame(main_frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        # Previous month button
        ctk.CTkButton(
            header,
            text="<",
            width=30,
            command=self.previous_month
        ).pack(side="left")
        
        # Month and Year label
        self.month_year_label = ctk.CTkLabel(
            header,
            text=self.current_date.strftime("%B %Y"),
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.month_year_label.pack(side="left", expand=True)
        
        # Next month button
        ctk.CTkButton(
            header,
            text=">",
            width=30,
            command=self.next_month
        ).pack(side="right")
        
        # Days of week header
        days_header = ctk.CTkFrame(main_frame, fg_color="transparent")
        days_header.pack(fill="x")
        
        for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
            ctk.CTkLabel(
                days_header,
                text=day,
                font=ctk.CTkFont(size=12),
                width=35
            ).pack(side="left", padx=2)
        
        # Calendar grid
        self.calendar_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.calendar_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        self.update_calendar()
        
    def update_calendar(self):
        # Clear existing calendar
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
            
        # Update month/year label
        self.month_year_label.configure(
            text=self.current_date.strftime("%B %Y")
        )
        
        # Get calendar for current month
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)
        
        # Create calendar buttons
        for week_num, week in enumerate(cal):
            week_frame = ctk.CTkFrame(self.calendar_frame, fg_color="transparent")
            week_frame.pack(fill="x", pady=2)
            
            for day_num, day in enumerate(week):
                if day != 0:
                    date = datetime(self.current_date.year, 
                                 self.current_date.month, day)
                    
                    # Check if this is the selected date
                    is_selected = (date.year == self.selected_date.year and
                                 date.month == self.selected_date.month and
                                 date.day == self.selected_date.day)
                    
                    # Check if this is today
                    is_today = (date.year == datetime.now().year and
                              date.month == datetime.now().month and
                              date.day == datetime.now().day)
                    
                    button = ctk.CTkButton(
                        week_frame,
                        text=str(day),
                        width=35,
                        height=35,
                        fg_color="#1a237e" if is_selected else 
                                 "#3949ab" if is_today else "transparent",
                        hover_color="#283593",
                        command=lambda d=date: self.select_date(d)
                    )
                    button.pack(side="left", padx=2)
                else:
                    # Empty space for days not in month
                    ctk.CTkFrame(
                        week_frame,
                        width=35,
                        height=35,
                        fg_color="transparent"
                    ).pack(side="left", padx=2)
                    
    def previous_month(self):
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, 
                                                        month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        self.update_calendar()
        
    def next_month(self):
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, 
                                                        month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        self.update_calendar()
        
    def select_date(self, date):
        self.selected_date = date
        if self.callback:
            self.callback(date)
        self.destroy()
        
    def get_date(self, callback):
        self.callback = callback
        self.grab_set()
        self.wait_window() 