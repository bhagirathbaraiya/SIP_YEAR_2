import firebase_admin
from firebase_admin import credentials, db
import json
import os
from config import Config

class FirebaseService:
    def __init__(self):
        self.db = None
        self.initialize_firebase()
    
    def initialize_firebase(self):
        """Initialize Firebase Admin SDK"""
        try:
            # Check if Firebase is already initialized
            if not firebase_admin._apps:
                # Use service account key file if it exists
                service_account_path = 'firebase-service-account.json'
                if os.path.exists(service_account_path):
                    cred = credentials.Certificate(service_account_path)
                    firebase_admin.initialize_app(cred, {
                        'databaseURL': Config.FIREBASE_CONFIG['databaseURL']
                    })
                else:
                    # Initialize with default credentials (for production)
                    firebase_admin.initialize_app(options={
                        'databaseURL': Config.FIREBASE_CONFIG['databaseURL']
                    })
            
            self.db = db.reference()
            print("Firebase initialized successfully")
        except Exception as e:
            print(f"Error initializing Firebase: {e}")
            self.db = None
    
    def get_bot_data(self):
        """Fetch bot data from Firebase"""
        try:
            if not self.db:
                return self.get_mock_data()
            
            # Fetch data from Firebase
            data = self.db.get()
            if data:
                return data
            else:
                return self.get_mock_data()
        except Exception as e:
            print(f"Error fetching Firebase data: {e}")
            return self.get_mock_data()
    
    def get_users_data(self):
        """Fetch users data from Firebase"""
        try:
            if not self.db:
                return self.get_mock_users_data()
            
            users_ref = self.db.child('MU_BOT/USERS')
            users_data = users_ref.get()
            
            if users_data:
                return users_data
            else:
                return self.get_mock_users_data()
        except Exception as e:
            print(f"Error fetching users data: {e}")
            return self.get_mock_users_data()
    
    def get_messages_data(self):
        """Fetch messages data from Firebase"""
        try:
            if not self.db:
                return self.get_mock_messages_data()
            
            messages_ref = self.db.child('MU_BOT/MESSAGES')
            messages_data = messages_ref.get()
            
            if messages_data:
                return messages_data
            else:
                return self.get_mock_messages_data()
        except Exception as e:
            print(f"Error fetching messages data: {e}")
            return self.get_mock_messages_data()
    
    def update_user_status(self, user_id, status):
        """Update user status in Firebase"""
        try:
            if not self.db:
                return {"success": False, "message": "Firebase not initialized"}
            
            user_ref = self.db.child(f'MU_BOT/USERS/{user_id}/data')
            user_ref.update({'status': status})
            
            return {"success": True, "message": f"User {user_id} status updated to {status}"}
        except Exception as e:
            print(f"Error updating user status: {e}")
            return {"success": False, "message": str(e)}
    
    def get_mock_data(self):
        """Return mock data structure similar to Firebase"""
        return {
            "MU_BOT": {
                "USERS": {
                    "user1": {
                        "data": {
                            "userID": "123456789",
                            "username": "john_doe",
                            "firstName": "John",
                            "lastName": "Doe",
                            "status": "allowed",
                            "joinedDate": "2024-01-15"
                        }
                    },
                    "user2": {
                        "data": {
                            "userID": "987654321",
                            "username": "jane_smith",
                            "firstName": "Jane",
                            "lastName": "Smith",
                            "status": "blocked",
                            "joinedDate": "2024-02-20"
                        }
                    },
                    "user3": {
                        "data": {
                            "userID": "456789123",
                            "username": "bob_wilson",
                            "firstName": "Bob",
                            "lastName": "Wilson",
                            "status": "pending",
                            "joinedDate": "2024-03-10"
                        }
                    }
                },
                "MESSAGES": {
                    "msg1": {
                        "user_id": "123456789",
                        "message_type": "text",
                        "message_status": "success",
                        "time_stamp": "2024-03-15T10:30:00Z"
                    },
                    "msg2": {
                        "user_id": "987654321",
                        "message_type": "image",
                        "message_status": "failed",
                        "time_stamp": "2024-03-15T11:15:00Z"
                    },
                    "msg3": {
                        "user_id": "123456789",
                        "message_type": "image",
                        "message_status": "success",
                        "time_stamp": "2024-03-15T12:00:00Z"
                    }
                },
                "STATS": {
                    "totalImages": 1250,
                    "totalUsers": 850,
                    "totalMessages": 3420,
                    "totalDownloads": 2100,
                    "studentImages": 750,
                    "facultyImages": 500,
                    "messageTypes": {
                        "text": 1200,
                        "image": 1500,
                        "document": 720
                    },
                    "messageStatus": {
                        "success": 2800,
                        "failed": 620
                    },
                    "userStatus": {
                        "allowed": 680,
                        "blocked": 120,
                        "pending": 50
                    },
                    "imageStatus": {
                        "processed": 1000,
                        "pending": 150,
                        "failed": 100
                    },
                    "imageTypes": {
                        "student": 750,
                        "faculty": 500
                    }
                }
            }
        }
    
    def get_mock_users_data(self):
        """Return mock users data"""
        return self.get_mock_data()["MU_BOT"]["USERS"]
    
    def get_mock_messages_data(self):
        """Return mock messages data"""
        return self.get_mock_data()["MU_BOT"]["MESSAGES"]

# Global Firebase service instance
firebase_service = FirebaseService()
