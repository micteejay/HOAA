class AccessControl:
    # Define access levels and their permissions
    ACCESS_LEVELS = {
        "Full Access": {
            "pages": [
                "Dashboard", "Bills", "Order Paper", "Order of the Day", "Petitions",
                "Chat", "Voting", "Motions", "Documents", "Admin"
            ],
            "roles": ["Speaker", "Clerk"],
            "permissions": {
                "create_bill": True,
                "approve_bill": True,
                "delete_bill": True
            }
        },
        
        "Administrative": {
            "pages": [
                "Dashboard", "Bills", "Order Paper", "Order of the Day", 
                "Documents", "Chat", "Admin"
            ],
            "roles": ["Deputy Speaker", "Deputy Clerk", "ICT Officer"],
            "permissions": {
                "create_bill": True,
                "approve_bill": True
            }
        },
        
        "Member": {
            "pages": [
                "Dashboard", "Bills", "Order Paper", "Order of the Day",
                "Petitions", "Chat", "Voting", "Motions"
            ],
            "roles": ["Member"],
            "permissions": {
                "view_bill": True
            }
        },
        
        "Legislative": {
            "pages": [
                "Dashboard", "Order Paper", "Order of the Day",
                "Motions", "Voting", "Chat", "Documents"
            ],
            "roles": [
                "Majority Leader", "Deputy Majority Leader",
                "Minority Leader", "Deputy Minority Leader",
                "Majority Whip", "Deputy Majority Whip",
                "Minority Whip", "Deputy Minority Whip"
            ]
        },
        
        "Committee": {
            "pages": [
                "Dashboard", "Order Paper", "Order of the Day",
                "Petitions", "Documents", "Chat"
            ],
            "roles": ["Committee Chair", "Deputy Committee Chair"]
        },
        
        "Support": {
            "pages": [
                "Dashboard", "Documents", "Chat"
            ],
            "roles": [
                "Legal Adviser", "Deputy Legal Adviser",
                "Public Relations Officer", "Deputy Public Relations Officer"
            ]
        },
        
        "Security": {
            "pages": [
                "Dashboard", "Chat"
            ],
            "roles": ["Sergeant-at-Arms", "Deputy Sergeant-at-Arms"]
        },
        
        "ICT": {
            "pages": [
                "Dashboard", "Chat", "Vote Results", "System Logs",
                "User Management", "Backup & Restore"
            ],
            "roles": ["ICT Officer"],
            "permissions": {
                "view_vote_details": True,      # Can see detailed voting records
                "manage_users": True,           # Can manage user accounts
                "view_system_logs": True,       # Can view system logs
                "manage_backups": True,         # Can manage system backups
                "technical_support": True,      # Can provide technical support
                "view_analytics": True          # Can view system analytics
            }
        }
    }
    
    @staticmethod
    def get_access_level(role):
        """Get access level for a given role"""
        for level, data in AccessControl.ACCESS_LEVELS.items():
            if role in data["roles"]:
                return level
        return None
        
    @staticmethod
    def get_permitted_pages(role):
        """Get list of permitted pages for a role"""
        access_level = AccessControl.get_access_level(role)
        if access_level:
            return AccessControl.ACCESS_LEVELS[access_level]["pages"]
        return ["Dashboard", "Chat"]  # Default minimal access
        
    @staticmethod
    def has_page_access(role, page):
        """Check if role has access to specific page"""
        permitted_pages = AccessControl.get_permitted_pages(role)
        return page in permitted_pages 