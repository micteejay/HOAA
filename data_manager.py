import json
import os
from datetime import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        return super().default(obj)

class DataManager:
    def __init__(self):
        self.sessions = {}
        self.motions = {}
        self.votes = {}
        self.bills = {}
        
        # Create data directory if it doesn't exist
        if not os.path.exists("data"):
            os.makedirs("data")
            
        self.load_data()
        
    def load_data(self):
        # Load sessions
        try:
            if os.path.exists("data/sessions.json"):
                with open("data/sessions.json", "r") as f:
                    content = f.read()
                    self.sessions = json.loads(content) if content else {}
            else:
                with open("data/sessions.json", "w") as f:
                    json.dump({}, f)
        except Exception as e:
            print(f"Error loading sessions: {str(e)}")
            self.sessions = {}
                
        # Load motions
        try:
            if os.path.exists("data/motions.json"):
                with open("data/motions.json", "r") as f:
                    content = f.read()
                    motions_data = json.loads(content) if content else {}
                    # Convert date strings back to datetime objects
                    for motion_id, motion in motions_data.items():
                        if "date" in motion:
                            try:
                                motion["date"] = datetime.strptime(motion["date"], "%Y-%m-%d %H:%M:%S")
                            except ValueError:
                                # Handle invalid date format
                                motion["date"] = datetime.now()
                    self.motions = motions_data
            else:
                with open("data/motions.json", "w") as f:
                    json.dump({}, f)
                self.motions = {}
        except Exception as e:
            print(f"Error loading motions: {str(e)}")
            self.motions = {}
                
        # Load votes
        try:
            if os.path.exists("data/votes.json"):
                with open("data/votes.json", "r") as f:
                    content = f.read()
                    self.votes = json.loads(content) if content else {}
            else:
                with open("data/votes.json", "w") as f:
                    json.dump({}, f)
                self.votes = {}
        except Exception as e:
            print(f"Error loading votes: {str(e)}")
            self.votes = {}
                
        # Load bills
        try:
            if os.path.exists("data/bills.json"):
                with open("data/bills.json", "r") as f:
                    content = f.read()
                    bills_data = json.loads(content) if content else {}
                    # Convert date strings back to datetime objects
                    for bill_id, bill in bills_data.items():
                        if "date" in bill:
                            try:
                                bill["date"] = datetime.strptime(bill["date"], "%Y-%m-%d %H:%M:%S")
                            except ValueError:
                                bill["date"] = datetime.now()
                    self.bills = bills_data
            else:
                with open("data/bills.json", "w") as f:
                    json.dump({}, f)
                self.bills = {}
        except Exception as e:
            print(f"Error loading bills: {str(e)}")
            self.bills = {}

    def save_data(self):
        # Create data directory if it doesn't exist
        if not os.path.exists("data"):
            os.makedirs("data")
            
        # Save sessions
        with open("data/sessions.json", "w") as f:
            json.dump(self.sessions, f, cls=DateTimeEncoder)
            
        # Save motions
        with open("data/motions.json", "w") as f:
            json.dump(self.motions, f, cls=DateTimeEncoder)
            
        # Save votes
        with open("data/votes.json", "w") as f:
            json.dump(self.votes, f, cls=DateTimeEncoder)
            
        # Save bills
        with open("data/bills.json", "w") as f:
            json.dump(self.bills, f, cls=DateTimeEncoder)
            
    def add_session(self, session_data):
        session_id = str(datetime.now().timestamp())
        self.sessions[session_id] = session_data
        self.save_data()
        return session_id
        
    def get_upcoming_sessions(self, limit=5):
        # Sort sessions by date and return the next 'limit' sessions
        sorted_sessions = sorted(
            [
                {**session, "id": id} 
                for id, session in self.sessions.items()
            ],
            key=lambda x: datetime.strptime(f"{x['date']} {x['time']}", "%Y-%m-%d %H:%M")
        )
        return sorted_sessions[:limit]
        
    def get_calendar_events(self, year, month):
        # Return all events for the specified month
        events = []
        for id, session in self.sessions.items():
            date = datetime.strptime(session["date"], "%Y-%m-%d")
            if date.year == year and date.month == month:
                events.append({
                    "id": id,
                    "title": session["title"],
                    "date": session["date"],
                    "time": session["time"],
                    "type": session["type"]
                })
        return events 
        
    def add_motion(self, motion_data):
        self.motions[motion_data["id"]] = motion_data
        self.save_data()
        
    def get_motions(self, include_pending=True):
        motions = []
        for id, motion in self.motions.items():
            if not include_pending and motion["status"] == "Pending":
                continue
            motions.append({**motion, "id": id})
        return motions
        
    def approve_motion(self, motion_id, approved=True):
        if motion_id in self.motions:
            self.motions[motion_id]["status"] = "Approved" if approved else "Rejected"
            self.motions[motion_id]["needs_approval"] = False
            self.save_data() 
        
    def add_vote(self, vote_data):
        self.votes[vote_data["id"]] = vote_data
        self.save_data()
        
    def get_votes(self, include_pending=True):
        votes = []
        for id, vote in self.votes.items():
            if not include_pending and vote["status"] == "Pending":
                continue
            votes.append({**vote, "id": id})
        return votes
        
    def approve_vote(self, vote_id, approved=True):
        if vote_id in self.votes:
            self.votes[vote_id]["status"] = "Approved" if approved else "Rejected"
            self.votes[vote_id]["needs_approval"] = False
            self.save_data() 
        
    def add_bill(self, bill_data):
        """Add a new bill to storage"""
        self.bills[bill_data["id"]] = bill_data
        self.save_data()
        
    def get_bills(self, include_drafts=True):
        """Get list of bills"""
        bills = []
        for id, bill in self.bills.items():
            if not include_drafts and bill["status"] == "Draft":
                continue
            bills.append({**bill, "id": id})
        return bills
        
    def approve_bill(self, bill_id, approved=True):
        """Approve or reject a bill"""
        if bill_id in self.bills:
            self.bills[bill_id]["status"] = "Passed" if approved else "Rejected"
            self.bills[bill_id]["needs_approval"] = False
            self.save_data() 