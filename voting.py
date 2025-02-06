import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox

class VotingContent(ctk.CTkFrame):
    def __init__(self, parent, current_user, is_admin=False):
        super().__init__(parent)
        
        # Store user info
        self.current_user = current_user
        self.is_admin = is_admin
        
        # Configure frame
        self.configure(fg_color="#f1f5f9")
        
        # Store voting data
        self.votes = []
        self.current_vote = None
        self.countdown = None
        self.timer = None
        
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
            text="🗳️",
            font=ctk.CTkFont(size=24)
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            title_frame,
            text="Voting",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left")
        
        # Right side buttons
        buttons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        buttons_frame.pack(side="right", padx=30)
        
        # New Vote button (admin only)
        if self.is_admin:
            self.new_vote_button = ctk.CTkButton(
                buttons_frame,
                text="+ New Vote",
                font=ctk.CTkFont(size=12),
                fg_color="#1a237e",
                hover_color="#283593",
                height=35,
                command=self.create_new_vote
            )
            self.new_vote_button.pack(side="right", padx=5)
            
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
        
        created_votes = sum(1 for v in self.votes if v["status"] == "Created")
        active_votes = sum(1 for v in self.votes if v["status"] == "Active")
        completed_votes = sum(1 for v in self.votes if v["status"] == "Completed")
        approved_votes = sum(1 for v in self.votes if v["status"] == "Approved")
        
        stats = [
            {
                "title": "Total Votes",
                "value": len(self.votes),
                "icon": "🗳️",
                "color": "#6366f1",
                "bg_color": "#e0e7ff"
            },
            {
                "title": "Created",
                "value": created_votes,
                "icon": "🆕",
                "color": "#4f46e5",
                "bg_color": "#e0e7ff"
            },
            {
                "title": "Active",
                "value": active_votes,
                "icon": "⏳",
                "color": "#f59e0b",
                "bg_color": "#fef3c7"
            },
            {
                "title": "Completed",
                "value": completed_votes,
                "icon": "✅",
                "color": "#10b981",
                "bg_color": "#d1fae5"
            },
            {
                "title": "Approved",
                "value": approved_votes,
                "icon": "📋",
                "color": "#475569",
                "bg_color": "#f1f5f9"
            }
        ]
        
        for i, stat in enumerate(stats):
            self.create_stat_card(container, stat, i)
            
    def create_vote_card(self, vote):
        card = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=15)
        card.pack(fill="x", pady=(0, 15))
        
        # Main content
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=20)
        
        # Left side info
        info_frame = ctk.CTkFrame(content, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)
        
        # Title and status
        header_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        header_frame.pack(fill="x")
        
        ctk.CTkLabel(
            header_frame,
            text=vote["title"],
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#000000"
        ).pack(side="left")
        
        # Status badge
        status_colors = {
            "Created": ("#e0e7ff", "#000000", "🆕"),
            "Active": ("#fef3c7", "#000000", "⏳"),
            "Completed": ("#dcfce7", "#000000", "✅"),
            "Approved": ("#f1f5f9", "#000000", "📋")
        }
        
        bg_color, text_color, icon = status_colors.get(vote["status"])
        status_frame = ctk.CTkFrame(
            header_frame,
            fg_color=bg_color,
            corner_radius=6
        )
        status_frame.pack(side="right")
        
        ctk.CTkLabel(
            status_frame,
            text=f"{icon} {vote['status']}",
            font=ctk.CTkFont(size=12),
            text_color=text_color
        ).pack(padx=10, pady=4)
        
        # Right side - Actions or results
        action_frame = ctk.CTkFrame(content, fg_color="transparent")
        action_frame.pack(side="right", padx=(20, 0))
        
        if vote["status"] == "Created" and self.is_admin:
            # Show start button for admin
            start_button = ctk.CTkButton(
                action_frame,
                text="Start Vote",
                font=ctk.CTkFont(size=14),
                fg_color="#4f46e5",
                hover_color="#4338ca",
                width=100,
                command=lambda v=vote: self.start_vote(v)
            )
            start_button.pack()
            
        elif vote["status"] == "Active":
            # Show countdown for admin
            if self.is_admin:
                countdown_frame = ctk.CTkFrame(action_frame, fg_color="transparent")
                countdown_frame.pack(fill="x")
                
                ctk.CTkLabel(
                    countdown_frame,
                    text=f"Time remaining: {vote.get('countdown', 0)}s",
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color="#ef4444"
                ).pack(pady=5)
                
                # Show vote count
                vote_count = len(vote["votes"])
                ctk.CTkLabel(
                    countdown_frame,
                    text=f"Votes cast: {vote_count}/245",
                    font=ctk.CTkFont(size=12),
                    text_color="#6b7280"
                ).pack()
            
            # Show voting buttons if not voted
            if self.current_user not in vote["votes"]:
                voting_frame = ctk.CTkFrame(action_frame, fg_color="transparent")
                voting_frame.pack(pady=(10 if self.is_admin else 0))
                
                for choice, colors in [
                    ("Yes", ("#059669", "#047857")),
                    ("No", ("#dc2626", "#b91c1c")),
                    ("Abstain", ("#6b7280", "#4b5563"))
                ]:
                    ctk.CTkButton(
                        voting_frame,
                        text=choice,
                        font=ctk.CTkFont(size=14),
                        fg_color=colors[0],
                        hover_color=colors[1],
                        width=80,
                        command=lambda v=vote, c=choice: self.cast_vote(v, c)
                    ).pack(side="left", padx=5)
            else:
                # Show user's vote
                vote_value = vote["votes"][self.current_user]
                vote_colors = {
                    "Yes": "#059669",
                    "No": "#dc2626",
                    "Abstain": "#6b7280"
                }
                
                ctk.CTkLabel(
                    action_frame,
                    text=f"Voted: {vote_value}",
                    font=ctk.CTkFont(size=14),
                    text_color=vote_colors[vote_value]
                ).pack()
                
        elif vote["status"] == "Completed" and self.is_admin:
            # Show approve button for admin
            ctk.CTkButton(
                action_frame,
                text="Approve Results",
                font=ctk.CTkFont(size=14),
                fg_color="#059669",
                hover_color="#047857",
                width=120,
                command=lambda v=vote: self.approve_results(v)
            ).pack()
            
            # Show detailed results for admin
            self.show_detailed_results(vote, action_frame)
            
        else:
            # Show summary results
            self.show_summary_results(vote, action_frame)

    def start_vote(self, vote):
        if messagebox.askyesno("Start Vote", "Are you sure you want to start this vote?"):
            vote["status"] = "Active"
            vote["countdown"] = 25
            self.current_vote = vote
            self.show_votes_list()
            self.create_stats_bar()
            
            # Start countdown for admin
            self.start_admin_countdown(vote)
            
            # Show voting overlay for all users
            self.show_voting_overlay(vote)

    def start_admin_countdown(self, vote):
        if vote["countdown"] > 0:
            # Update countdown in vote card
            self.show_votes_list()
            vote["countdown"] -= 1
            self.after(1000, lambda: self.start_admin_countdown(vote))
        else:
            # When countdown ends, show approval dialog for admin
            vote["status"] = "Completed"
            self.current_vote = None
            self.show_votes_list()
            self.create_stats_bar()
            if self.is_admin:
                self.show_approval_dialog(vote)

    def show_approval_dialog(self, vote):
        dialog = ApproveResultsDialog(self, vote)
        self.wait_window(dialog.dialog)
        
        if hasattr(dialog, 'result'):
            vote.update({
                "status": "Approved",
                "approved_by": self.current_user,
                "approved_at": datetime.now(),
                "approval_notes": dialog.result["notes"]
            })
            self.show_votes_list()
            self.create_stats_bar()

    def show_voting_overlay(self, vote):
        # Create fullscreen overlay
        overlay = VotingOverlay(self, vote)
        self.wait_window(overlay.overlay)
        
        # After overlay closes, check if voting is complete
        if len(vote["votes"]) >= 245:  # Total assembly members
            vote["status"] = "Completed"
            self.current_vote = None
            self.show_votes_list()
            self.create_stats_bar()

    def show_detailed_results(self, vote, parent):
        results_frame = ctk.CTkFrame(parent, fg_color="transparent")
        results_frame.pack(pady=(10, 0))
        
        # Count votes
        yes_votes = sum(1 for v in vote["votes"].values() if v == "Yes")
        no_votes = sum(1 for v in vote["votes"].values() if v == "No")
        abstain_votes = sum(1 for v in vote["votes"].values() if v == "Abstain")
        total_votes = len(vote["votes"])
        
        # Show counts
        for choice, count, color in [
            ("Yes", yes_votes, "#059669"),
            ("No", no_votes, "#dc2626"),
            ("Abstain", abstain_votes, "#6b7280")
        ]:
            ctk.CTkLabel(
                results_frame,
                text=f"{choice}: {count} ({count/total_votes*100:.1f}%)",
                font=ctk.CTkFont(size=14),
                text_color=color
            ).pack(anchor="w")
            
        # Show voters list
        if total_votes > 0:
            voters_frame = ctk.CTkFrame(parent, fg_color="#f8fafc", corner_radius=6)
            voters_frame.pack(fill="x", pady=(10, 0))
            
            ctk.CTkLabel(
                voters_frame,
                text="Voters:",
                font=ctk.CTkFont(size=12, weight="bold")
            ).pack(anchor="w", padx=10, pady=(10, 5))
            
            for voter, choice in vote["votes"].items():
                vote_color = {
                    "Yes": "#059669",
                    "No": "#dc2626",
                    "Abstain": "#6b7280"
                }[choice]
                
                ctk.CTkLabel(
                    voters_frame,
                    text=f"{voter}: {choice}",
                    font=ctk.CTkFont(size=12),
                    text_color=vote_color
                ).pack(anchor="w", padx=10, pady=2)

    def show_summary_results(self, vote, parent):
        results_frame = ctk.CTkFrame(parent, fg_color="transparent")
        results_frame.pack()
        
        yes_votes = sum(1 for v in vote["votes"].values() if v == "Yes")
        no_votes = sum(1 for v in vote["votes"].values() if v == "No")
        abstain_votes = sum(1 for v in vote["votes"].values() if v == "Abstain")
        total_votes = len(vote["votes"])
        
        for choice, count, color in [
            ("Yes", yes_votes, "#059669"),
            ("No", no_votes, "#dc2626"),
            ("Abstain", abstain_votes, "#6b7280")
        ]:
            ctk.CTkLabel(
                results_frame,
                text=f"{choice}: {count} ({count/total_votes*100:.1f}%)",
                font=ctk.CTkFont(size=14),
                text_color=color
            ).pack(anchor="w")

    def approve_results(self, vote):
        dialog = ApproveResultsDialog(self, vote)
        self.wait_window(dialog.dialog)
        
        if hasattr(dialog, 'result'):
            vote.update({
                "status": "Approved",
                "approved_by": self.current_user,
                "approved_at": datetime.now(),
                "approval_notes": dialog.result["notes"]
            })
            
            self.show_votes_list()
            self.create_stats_bar()

    def create_content(self):
        # Create main scrollable frame
        self.content_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Show empty state or votes list
        self.show_votes_list()

    def show_empty_state(self):
        empty_frame = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=15)
        empty_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            empty_frame,
            text="No Active Votes",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(40, 10))
        
        message = "Click '+ New Vote' to create a new vote" if self.is_admin else "No votes available at this time"
        ctk.CTkLabel(
            empty_frame,
            text=message,
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack()
        
    def create_new_vote(self):
        dialog = NewVoteDialog(self)
        self.wait_window(dialog.dialog)
        
        if hasattr(dialog, 'result'):
            # Add new vote
            vote_data = dialog.result
            vote_data.update({
                "id": datetime.now().strftime("%Y%m%d%H%M%S"),
                "created_by": self.current_user,
                "created_at": datetime.now(),
                "status": "Created",  # Changed from "Active" to "Created"
                "votes": {}
            })
            
            self.votes.append(vote_data)
            self.show_votes_list()
            self.create_stats_bar()
            
    def show_votes_list(self):
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        if not self.votes:
            self.show_empty_state()
            return
        
        # Show votes
        for vote in self.votes:
            self.create_vote_card(vote)
        
    def cast_vote(self, vote, choice):
        if messagebox.askyesno("Confirm Vote", f"Are you sure you want to vote '{choice}'?"):
            vote["votes"][self.current_user] = choice
            
            # Check if voting is complete
            total_members = 245  # Total assembly members
            if len(vote["votes"]) >= total_members:
                vote["status"] = "Completed"
                vote["completed_at"] = datetime.now()
            
            self.show_votes_list()
            self.create_stats_bar()
            
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

class NewVoteDialog:
    def __init__(self, parent):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("New Vote")
        self.dialog.geometry("500x200")  # Reduced height since we removed description
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
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
            text="Vote Title:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w")
        
        self.title_var = ctk.StringVar()
        title_entry = ctk.CTkEntry(
            title_frame,
            textvariable=self.title_var,
            placeholder_text="Enter vote title"
        )
        title_entry.pack(fill="x", pady=(5, 0))
        
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
            text="Create Vote",
            fg_color="#1a237e",
            hover_color="#283593",
            width=100,
            command=self.create_vote
        ).pack(side="right")
        
    def create_vote(self):
        try:
            title = self.title_var.get().strip()
            
            if not title:
                raise ValueError("Please enter a vote title")
                
            self.result = {
                "title": title,
                "description": ""  # Empty description
            }
            
            self.dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create vote: {str(e)}")

class ApproveResultsDialog:
    def __init__(self, parent, vote):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Approve Vote Results")
        self.dialog.geometry("600x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Store vote data
        self.vote = vote
        
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
        
        # Vote info
        info_frame = ctk.CTkFrame(content_frame, fg_color="white", corner_radius=10)
        info_frame.pack(fill="x", pady=(0, 20))
        
        # Title
        ctk.CTkLabel(
            info_frame,
            text=self.vote["title"],
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=20, pady=(20, 10))
        
        # Description
        ctk.CTkLabel(
            info_frame,
            text=self.vote["description"],
            font=ctk.CTkFont(size=14),
            text_color="#334155",
            wraplength=540
        ).pack(anchor="w", padx=20, pady=(0, 20))
        
        # Results summary
        results_frame = ctk.CTkFrame(content_frame, fg_color="white", corner_radius=10)
        results_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            results_frame,
            text="Voting Results",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(20, 10))
        
        # Count votes
        yes_votes = sum(1 for v in self.vote["votes"].values() if v == "Yes")
        no_votes = sum(1 for v in self.vote["votes"].values() if v == "No")
        abstain_votes = sum(1 for v in self.vote["votes"].values() if v == "Abstain")
        total_votes = len(self.vote["votes"])
        
        # Show results
        for choice, count, color in [
            ("Yes", yes_votes, "#059669"),
            ("No", no_votes, "#dc2626"),
            ("Abstain", abstain_votes, "#6b7280")
        ]:
            result_item = ctk.CTkFrame(results_frame, fg_color="transparent")
            result_item.pack(fill="x", padx=20, pady=5)
            
            ctk.CTkLabel(
                result_item,
                text=choice,
                font=ctk.CTkFont(size=14),
                text_color=color
            ).pack(side="left")
            
            ctk.CTkLabel(
                result_item,
                text=f"{count} votes ({count/total_votes*100:.1f}%)",
                font=ctk.CTkFont(size=14),
                text_color=color
            ).pack(side="right")
        
        ctk.CTkLabel(
            results_frame,
            text=f"Total Votes: {total_votes}",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 20))
        
        # Approval notes
        notes_frame = ctk.CTkFrame(content_frame, fg_color="white", corner_radius=10)
        notes_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            notes_frame,
            text="Approval Notes:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(20, 10))
        
        self.notes_text = ctk.CTkTextbox(
            notes_frame,
            font=ctk.CTkFont(size=12),
            height=100
        )
        self.notes_text.pack(fill="x", padx=20, pady=(0, 20))
        
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
            text="Approve Results",
            fg_color="#059669",
            hover_color="#047857",
            width=120,
            command=self.approve_results
        ).pack(side="right")
        
    def approve_results(self):
        try:
            notes = self.notes_text.get("1.0", "end-1c").strip()
            
            if not notes:
                raise ValueError("Please enter approval notes")
                
            self.result = {
                "notes": notes
            }
            
            self.dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to approve results: {str(e)}") 

class VotingOverlay:
    def __init__(self, parent, vote):
        self.overlay = ctk.CTkToplevel()
        self.overlay.title("Vote Now")
        self.overlay.attributes('-fullscreen', True)
        self.overlay.transient(parent)
        self.overlay.grab_set()
        
        # Store data
        self.parent = parent
        self.vote = vote
        self.countdown = vote["countdown"]
        
        # Configure grid
        self.overlay.grid_columnconfigure(0, weight=1)
        self.overlay.grid_rowconfigure(0, weight=1)
        
        # Create content
        self.create_overlay_content()
        self.start_countdown()
        
    def create_overlay_content(self):
        # Main container
        container = ctk.CTkFrame(
            self.overlay,
            fg_color="#1e293b",
            corner_radius=0
        )
        container.grid(row=0, column=0, sticky="nsew")
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=1)
        
        # Header
        header = ctk.CTkFrame(container, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=40, pady=20)
        
        ctk.CTkLabel(
            header,
            text="🗳️",
            font=ctk.CTkFont(size=32)
        ).pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(
            header,
            text="Active Vote",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        ).pack(side="left")
        
        self.countdown_label = ctk.CTkLabel(
            header,
            text=f"Time remaining: {self.countdown}s",
            font=ctk.CTkFont(size=20),
            text_color="#ef4444"
        )
        self.countdown_label.pack(side="right")
        
        # Vote content
        content = ctk.CTkFrame(container, fg_color="transparent")
        content.grid(row=1, column=0, sticky="nsew", padx=40)
        content.grid_columnconfigure(0, weight=1)
        
        # Vote info
        info_frame = ctk.CTkFrame(content, fg_color="#334155", corner_radius=15)
        info_frame.pack(fill="x", pady=(0, 30))
        
        ctk.CTkLabel(
            info_frame,
            text=self.vote["title"],
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        ).pack(anchor="w", padx=30, pady=(30, 15))
        
        ctk.CTkLabel(
            info_frame,
            text=self.vote["description"],
            font=ctk.CTkFont(size=16),
            text_color="#94a3b8",
            wraplength=800
        ).pack(anchor="w", padx=30, pady=(0, 30))
        
        # Voting buttons
        buttons_frame = ctk.CTkFrame(content, fg_color="transparent")
        buttons_frame.pack(pady=30)
        
        for choice, colors in [
            ("Yes", ("#059669", "#047857")),
            ("No", ("#dc2626", "#b91c1c")),
            ("Abstain", ("#6b7280", "#4b5563"))
        ]:
            ctk.CTkButton(
                buttons_frame,
                text=choice,
                font=ctk.CTkFont(size=20),
                fg_color=colors[0],
                hover_color=colors[1],
                width=150,
                height=50,
                command=lambda c=choice: self.cast_vote(c)
            ).pack(side="left", padx=15)
            
    def start_countdown(self):
        if self.countdown > 0:
            self.countdown_label.configure(text=f"Time remaining: {self.countdown}s")
            self.countdown -= 1
            self.overlay.after(1000, self.start_countdown)
        else:
            self.overlay.destroy()
            
    def cast_vote(self, choice):
        if messagebox.askyesno("Confirm Vote", f"Are you sure you want to vote '{choice}'?"):
            self.vote["votes"][self.parent.current_user] = choice
            messagebox.showinfo("Success", "Your vote has been recorded")
            self.overlay.destroy() 