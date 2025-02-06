import customtkinter as ctk
from tkinter import messagebox
from navbar import NavigationBar
from order_of_day import OrderOfDayContent
from order_paper import OrderPaperContent
from petition import PetitionContent
from voting import VotingContent
from chat import ChatContent
from motion import MotionContent
from documents import DocumentContent
from datetime import datetime
from signout import SignOut

class DashboardContent(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=1, sticky="nsew")
        self.configure(fg_color="#f1f5f9")
        
        self.parent = parent  # Store parent reference to access data_manager
        
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
            text="🏛️",
            font=ctk.CTkFont(size=24)
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            title_frame,
            text="Assembly Dashboard",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left")
        
        # Right side buttons
        buttons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        buttons_frame.pack(side="right", padx=30)
        
        ctk.CTkButton(
            buttons_frame,
            text="+ New Motion",
            font=ctk.CTkFont(size=12),
            fg_color="#1a237e",
            hover_color="#283593",
            height=35,
            command=self.new_motion
        ).pack(side="right", padx=5)
        
    def new_motion(self):
        # Switch to Motions page and open new motion dialog
        self.parent.show_content("Motions")
        if hasattr(self.parent.current_content, 'create_motion'):
            self.parent.current_content.create_motion()
        
    def create_content(self):
        content_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Top row with key metrics
        self.create_key_metrics(content_frame)
        
        # Middle row with session info and upcoming events
        middle_row = ctk.CTkFrame(content_frame, fg_color="transparent")
        middle_row.pack(fill="x", pady=(0, 30))
        
        self.create_current_session(middle_row)
        self.create_upcoming_events(middle_row)
        
        # Bottom row with recent activities and quick actions
        bottom_row = ctk.CTkFrame(content_frame, fg_color="transparent")
        bottom_row.pack(fill="x")
        
        self.create_recent_activities(bottom_row)
        self.create_quick_actions(bottom_row)
        
    def create_key_metrics(self, parent):
        metrics_frame = ctk.CTkFrame(parent, fg_color="transparent")
        metrics_frame.pack(fill="x", pady=(0, 30))
        
        metrics = [
            {
                "title": "Active Members",
                "value": "245",
                "change": "+2",
                "color": "#10b981",
                "icon": "👥"
            },
            {
                "title": "Bills in Progress",
                "value": str(len(self.parent.data_manager.get_bills())),
                "change": "+3",
                "color": "#6366f1",
                "icon": "📜",
                "link": "Bills"
            },
            {
                "title": "Pending Motions",
                "value": "8",
                "change": "-1",
                "color": "#f59e0b",
                "icon": "⚖️"
            },
            {
                "title": "Today's Attendance",
                "value": "92%",
                "change": "+5%",
                "color": "#8b5cf6",
                "icon": "📊"
            }
        ]
        
        for i, metric in enumerate(metrics):
            card = ctk.CTkFrame(metrics_frame, fg_color="white", corner_radius=15)
            card.grid(row=0, column=i, padx=10, sticky="ew")
            metrics_frame.grid_columnconfigure(i, weight=1)
            
            # Make card and all its children clickable if it has a link
            if "link" in metric:
                def make_clickable(widget, section=metric["link"]):
                    widget.bind("<Button-1>", lambda e, s=section: self.navigate_to_section(s))
                    widget.configure(cursor="hand2")
                    for child in widget.winfo_children():
                        make_clickable(child, section)
                
                make_clickable(card)
            
            # Icon and title
            header = ctk.CTkFrame(card, fg_color="transparent")
            header.pack(fill="x", padx=20, pady=(20, 10))
            
            icon_label = ctk.CTkLabel(
                header,
                text=metric["icon"],
                font=ctk.CTkFont(size=24)
            )
            icon_label.pack(side="left")
            
            title_label = ctk.CTkLabel(
                header,
                text=metric["title"],
                font=ctk.CTkFont(size=14),
                text_color="#000000"
            )
            title_label.pack(side="left", padx=(10, 0))
            
            # Value and change
            value_frame = ctk.CTkFrame(card, fg_color="transparent")
            value_frame.pack(fill="x", padx=20, pady=(0, 20))
            
            value_label = ctk.CTkLabel(
                value_frame,
                text=metric["value"],
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color="#000000"
            )
            value_label.pack(side="left")
            
            change_color = "#10b981" if "+" in metric["change"] else "#ef4444"
            change_frame = ctk.CTkFrame(
                value_frame,
                fg_color=change_color,
                corner_radius=6
            )
            change_frame.pack(side="right")
            
            change_label = ctk.CTkLabel(
                change_frame,
                text=metric["change"],
                font=ctk.CTkFont(size=12),
                text_color="white"
            )
            change_label.pack(padx=8, pady=4)
            
    def navigate_to_section(self, section):
        """Navigate to a specific section"""
        self.parent.show_content(section)
        
    def create_current_session(self, parent):
        session_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=15)
        session_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        # Header
        header = ctk.CTkFrame(session_frame, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            header,
            text="Current Session",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#000000"
        ).pack(side="left")
        
        status_frame = ctk.CTkFrame(
            header,
            fg_color="#ecfdf5",
            corner_radius=6
        )
        status_frame.pack(side="right")
        
        ctk.CTkLabel(
            status_frame,
            text="🟢 In Progress",
            font=ctk.CTkFont(size=12),
            text_color="#059669"
        ).pack(padx=10, pady=4)
        
        # Session info
        info_frame = ctk.CTkFrame(session_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        session_info = [
            ("Date", "Wednesday, January 31, 2024"),
            ("Time", "10:00 AM - 2:00 PM"),
            ("Type", "Regular Session"),
            ("Agenda Items", "5 Remaining"),
            ("Current Topic", "Budget Discussion")
        ]
        
        for label, value in session_info:
            item_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            item_frame.pack(fill="x", pady=5)
            
            ctk.CTkLabel(
                item_frame,
                text=label,
                font=ctk.CTkFont(size=12),
                text_color="gray"
            ).pack(side="left")
            
            ctk.CTkLabel(
                item_frame,
                text=value,
                font=ctk.CTkFont(size=12, weight="bold")
            ).pack(side="right")
            
    def create_upcoming_events(self, parent):
        events_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=15)
        events_frame.pack(side="right", fill="both", expand=True, padx=(15, 0))
        
        # Header
        header = ctk.CTkFrame(events_frame, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            header,
            text="Upcoming Events",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left")
        
        # Events list
        events_list = ctk.CTkFrame(events_frame, fg_color="transparent")
        events_list.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Get upcoming sessions from data manager
        upcoming_sessions = self.parent.data_manager.get_upcoming_sessions()
        
        for session in upcoming_sessions:
            self.create_event_item(events_list, session)
        
    def create_event_item(self, parent, event):
        item = ctk.CTkFrame(parent, fg_color="transparent", height=60)
        item.pack(fill="x", pady=5)
        item.pack_propagate(False)
        
        # Date indicator
        date = datetime.strptime(event["date"], "%Y-%m-%d")
        date_frame = ctk.CTkFrame(item, fg_color="#e0e7ff", width=50, corner_radius=8)
        date_frame.pack(side="left")
        date_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            date_frame,
            text=date.strftime("%d"),
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#3730a3"
        ).pack(pady=(5, 0))
        
        ctk.CTkLabel(
            date_frame,
            text=date.strftime("%b"),
            font=ctk.CTkFont(size=12),
            text_color="#3730a3"
        ).pack()
        
        # Event details
        details = ctk.CTkFrame(item, fg_color="transparent")
        details.pack(side="left", fill="both", expand=True, padx=15)
        
        ctk.CTkLabel(
            details,
            text=event["title"],
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#000000"
        ).pack(anchor="w")
        
        info = ctk.CTkFrame(details, fg_color="transparent")
        info.pack(fill="x")
        
        ctk.CTkLabel(
            info,
            text=f"🕒 {event['time']}",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            info,
            text=f"📍 {event['type']} Session",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(side="left")
            
    def create_recent_activities(self, parent):
        activities_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=15)
        activities_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        # Header
        header = ctk.CTkFrame(activities_frame, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            header,
            text="Recent Activities",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left")
        
        # Activities list
        activities = [
            {
                "action": "Motion Filed",
                "description": "Infrastructure Development Plan",
                "time": "2 hours ago",
                "icon": "📝",
                "color": "#818cf8"
            },
            {
                "action": "Bill Passed",
                "description": "Education Reform Act 2024",
                "time": "4 hours ago",
                "icon": "✅",
                "color": "#34d399"
            },
            {
                "action": "Vote Completed",
                "description": "Budget Amendment Proposal",
                "time": "5 hours ago",
                "icon": "🗳️",
                "color": "#f472b6"
            }
        ]
        
        for activity in activities:
            activity_item = ctk.CTkFrame(activities_frame, fg_color="transparent")
            activity_item.pack(fill="x", padx=20, pady=5)
            
            # Icon
            icon_frame = ctk.CTkFrame(
                activity_item,
                width=32,
                height=32,
                fg_color=activity["color"],
                corner_radius=8
            )
            icon_frame.pack(side="left")
            icon_frame.pack_propagate(False)
            
            ctk.CTkLabel(
                icon_frame,
                text=activity["icon"],
                font=ctk.CTkFont(size=16)
            ).place(relx=0.5, rely=0.5, anchor="center")
            
            # Info
            info_frame = ctk.CTkFrame(activity_item, fg_color="transparent")
            info_frame.pack(side="left", padx=(15, 0), fill="x", expand=True)
            
            ctk.CTkLabel(
                info_frame,
                text=activity["action"],
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                info_frame,
                text=activity["description"],
                font=ctk.CTkFont(size=12),
                text_color="gray"
            ).pack(anchor="w")
            
            # Time
            ctk.CTkLabel(
                activity_item,
                text=activity["time"],
                font=ctk.CTkFont(size=12),
                text_color="gray"
            ).pack(side="right")

    def create_quick_actions(self, parent):
        actions_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=15)
        actions_frame.pack(side="right", fill="both", expand=True, padx=(15, 0))
        
        # Header
        header = ctk.CTkFrame(actions_frame, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            header,
            text="Quick Actions",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left")
        
        # Actions grid
        actions_grid = ctk.CTkFrame(actions_frame, fg_color="transparent")
        actions_grid.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        actions = [
            {"text": "New Motion", "icon": "📝", "color": "#818cf8"},
            {"text": "Schedule Session", "icon": "📅", "color": "#f472b6"},
            {"text": "View Reports", "icon": "📊", "color": "#34d399"},
            {"text": "Member Directory", "icon": "👥", "color": "#f59e0b"}
        ]
        
        for i, action in enumerate(actions):
            row = i // 2
            col = i % 2
            
            action_button = ctk.CTkButton(
                actions_grid,
                text=f"{action['icon']}  {action['text']}",
                font=ctk.CTkFont(size=14),
                fg_color=action["color"],
                hover_color=action["color"],
                height=45
            )
            action_button.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            actions_grid.grid_columnconfigure(col, weight=1)

class AssemblyDashboard(ctk.CTkFrame):
    def __init__(self, parent, current_user, is_admin=False, data_manager=None):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        
        # Store user info and data manager
        self.current_user = current_user
        self.is_admin = is_admin
        self.data_manager = data_manager
        self.parent = parent  # Store parent reference
        self.window = parent  # Store window reference
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create navigation
        self.nav = NavigationBar(self, self.on_nav_change)
        self.nav.grid(row=0, column=0, sticky="nsw")
        
        # Initialize current content
        self.current_content = None
        self.show_content("Dashboard")
        
    def show_content(self, section):
        # Remove current content if exists
        if self.current_content:
            self.current_content.destroy()
            
        # Show selected content
        if section == "Dashboard":
            self.current_content = DashboardContent(self)
            self.current_content.grid(row=0, column=1, sticky="nsew")
        elif section == "Bills":
            from bill import BillContent
            self.current_content = BillContent(
                self,
                current_user=self.current_user,
                is_admin=self.is_admin
            )
            self.current_content.grid(row=0, column=1, sticky="nsew")
        elif section == "Order Paper":
            self.current_content = OrderPaperContent(self)
            self.current_content.grid(row=0, column=1, sticky="nsew")
        elif section == "Order of the Day":
            self.current_content = OrderOfDayContent(self)
            self.current_content.grid(row=0, column=1, sticky="nsew")
        elif section == "Petitions":
            self.current_content = PetitionContent(
                self,
                current_user=self.current_user,
                is_admin=self.is_admin
            )
            self.current_content.grid(row=0, column=1, sticky="nsew")
        elif section == "Voting":
            self.current_content = VotingContent(
                self,
                current_user=self.current_user,
                is_admin=self.is_admin
            )
            self.current_content.grid(row=0, column=1, sticky="nsew")
        elif section == "Chat":
            self.current_content = ChatContent(
                self,
                current_user=self.current_user,
                is_admin=self.is_admin
            )
            self.current_content.grid(row=0, column=1, sticky="nsew")
        elif section == "Motions":
            self.current_content = MotionContent(
                self,
                current_user=self.current_user,
                is_admin=self.is_admin
            )
            self.current_content.grid(row=0, column=1, sticky="nsew")
        elif section == "Documents":
            self.current_content = DocumentContent(
                self,
                current_user=self.current_user,
                is_admin=self.is_admin
            )
            self.current_content.grid(row=0, column=1, sticky="nsew")
        elif section == "Admin":
            if self.is_admin:  # Only show admin page if user is admin
                # Import here to avoid circular imports
                import admin
                self.current_content = admin.AdminContent(
                    self,
                    current_user=self.current_user,
                    is_admin=self.is_admin
                )
                self.current_content.grid(row=0, column=1, sticky="nsew")
            else:
                messagebox.showerror("Access Denied", "You don't have permission to access this page")
                return
        elif section == "Sign Out":
            SignOut.handle_signout(self, self.parent)
            return
            
    def on_nav_change(self, section):
        self.show_content(section)

    def update_dashboard(self):
        """Update dashboard content when data changes"""
        if isinstance(self.current_content, DashboardContent):
            self.current_content.destroy()
            self.current_content = DashboardContent(self)
            self.current_content.grid(row=0, column=1, sticky="nsew")

if __name__ == "__main__":
    app = AssemblyDashboard()
    app.run()