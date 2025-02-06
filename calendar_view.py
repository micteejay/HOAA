import customtkinter as ctk
from datetime import datetime
import calendar

class CalendarView(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Session Calendar")
        self.geometry("800x600")
        
        self.parent = parent
        self.current_date = datetime.now()
        
        self.create_calendar()
        
    def create_calendar(self):
        # Create controls
        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.pack(fill="x", padx=20, pady=20)
        
        # Month/Year navigation
        nav = ctk.CTkFrame(controls, fg_color="transparent")
        nav.pack(side="left")
        
        ctk.CTkButton(
            nav,
            text="<",
            width=30,
            command=self.previous_month
        ).pack(side="left", padx=5)
        
        self.month_label = ctk.CTkLabel(
            nav,
            text=self.current_date.strftime("%B %Y"),
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.month_label.pack(side="left", padx=15)
        
        ctk.CTkButton(
            nav,
            text=">",
            width=30,
            command=self.next_month
        ).pack(side="left", padx=5)
        
        # Calendar grid
        self.calendar_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.calendar_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.update_calendar()
        
    def update_calendar(self):
        # Clear current calendar
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
            
        # Update month/year label
        self.month_label.configure(
            text=self.current_date.strftime("%B %Y")
        )
        
        # Get events for current month
        events = self.parent.data_manager.get_calendar_events(
            self.current_date.year,
            self.current_date.month
        )
        
        # Create calendar grid
        self.create_calendar_grid(events)
        
    def create_calendar_grid(self, events):
        # Days of week header
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        header = ctk.CTkFrame(self.calendar_frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))
        
        for i, day in enumerate(days):
            header.grid_columnconfigure(i, weight=1)
            ctk.CTkLabel(
                header,
                text=day,
                font=ctk.CTkFont(size=12, weight="bold")
            ).grid(row=0, column=i, pady=5)
            
        # Get calendar for current month
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)
        
        # Create grid
        grid = ctk.CTkFrame(self.calendar_frame, fg_color="transparent")
        grid.pack(fill="both", expand=True)
        
        for i in range(7):
            grid.grid_columnconfigure(i, weight=1)
            
        # Create day cells
        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                cell = self.create_day_cell(grid, day, week_num, day_num, events)
                cell.grid(row=week_num, column=day_num, sticky="nsew", padx=2, pady=2)
                
    def create_day_cell(self, parent, day, week, col, events):
        cell = ctk.CTkFrame(parent, fg_color="white", corner_radius=8)
        
        if day == 0:
            return cell
            
        # Check if this is today
        is_today = (self.current_date.year == datetime.now().year and
                   self.current_date.month == datetime.now().month and
                   day == datetime.now().day)
                   
        # Date label
        date_label = ctk.CTkLabel(
            cell,
            text=str(day),
            font=ctk.CTkFont(
                size=14,
                weight="bold" if is_today else "normal"
            ),
            text_color="#1a237e" if is_today else "#000000"
        )
        date_label.pack(anchor="w", padx=8, pady=5)
        
        # Find events for this day
        day_events = [
            event for event in events
            if datetime.strptime(event["date"], "%Y-%m-%d").day == day
        ]
        
        # Show events
        for event in day_events:
            self.create_event_indicator(cell, event)
            
        return cell
        
    def create_event_indicator(self, parent, event):
        indicator = ctk.CTkFrame(
            parent,
            fg_color="#e0e7ff",
            corner_radius=4,
            height=20
        )
        indicator.pack(fill="x", padx=5, pady=1)
        indicator.pack_propagate(False)
        
        ctk.CTkLabel(
            indicator,
            text=f"• {event['title']}",
            font=ctk.CTkFont(size=11),
            text_color="#3730a3"
        ).pack(side="left", padx=5)
        
    def previous_month(self):
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(
                year=self.current_date.year - 1,
                month=12
            )
        else:
            self.current_date = self.current_date.replace(
                month=self.current_date.month - 1
            )
        self.update_calendar()
        
    def next_month(self):
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(
                year=self.current_date.year + 1,
                month=1
            )
        else:
            self.current_date = self.current_date.replace(
                month=self.current_date.month + 1
            )
        self.update_calendar() 