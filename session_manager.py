"""
Session Manager for Employee Lookup Agent
==========================================
Handles user sessions, memory, and conversation context with local file storage.
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
import uuid

class SessionManager:
    """Manages user sessions and conversation memory"""
    
    def __init__(self, sessions_dir: str = "user_sessions"):
        """Initialize session manager with local storage directory"""
        self.sessions_dir = sessions_dir
        self.ensure_sessions_directory()
        
    def ensure_sessions_directory(self):
        """Create sessions directory if it doesn't exist"""
        if not os.path.exists(self.sessions_dir):
            os.makedirs(self.sessions_dir)
    
    def create_session(self, user_email: str = None) -> str:
        """Create a new session and return session ID"""
        session_id = str(uuid.uuid4())
        
        session_data = {
            'session_id': session_id,
            'user_email': user_email,
            'created_at': datetime.now().isoformat(),
            'last_activity': datetime.now().isoformat(),
            'conversation_history': [],
            'user_context': {
                'authenticated': bool(user_email),
                'employee_data': None,
                'preferences': {},
                'search_history': []
            },
            'session_state': 'active'
        }
        
        self._save_session(session_id, session_data)
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Retrieve session data by ID"""
        session_file = os.path.join(self.sessions_dir, f"{session_id}.json")
        
        if not os.path.exists(session_file):
            return None
            
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
                
            # Update last activity
            session_data['last_activity'] = datetime.now().isoformat()
            self._save_session(session_id, session_data)
            
            return session_data
        except Exception as e:
            print(f"Error loading session {session_id}: {e}")
            return None
    
    def update_session(self, session_id: str, updates: Dict) -> bool:
        """Update session data"""
        session_data = self.get_session(session_id)
        if not session_data:
            return False
            
        # Deep merge updates
        for key, value in updates.items():
            if key in session_data and isinstance(session_data[key], dict) and isinstance(value, dict):
                session_data[key].update(value)
            else:
                session_data[key] = value
        
        session_data['last_activity'] = datetime.now().isoformat()
        return self._save_session(session_id, session_data)
    
    def authenticate_user(self, session_id: str, user_email: str, employee_data: Dict = None) -> bool:
        """Authenticate user and store their data"""
        updates = {
            'user_email': user_email,
            'user_context': {
                'authenticated': True,
                'employee_data': employee_data,
                'preferences': {},
                'search_history': []
            }
        }
        
        return self.update_session(session_id, updates)
    
    def add_conversation_message(self, session_id: str, message: Dict) -> bool:
        """Add a message to conversation history"""
        session_data = self.get_session(session_id)
        if not session_data:
            return False
        
        message['timestamp'] = datetime.now().isoformat()
        message['id'] = len(session_data['conversation_history']) + 1
        
        session_data['conversation_history'].append(message)
        
        # Keep only last 50 messages to manage file size
        if len(session_data['conversation_history']) > 50:
            session_data['conversation_history'] = session_data['conversation_history'][-50:]
        
        return self._save_session(session_id, session_data)
    
    def add_search_to_history(self, session_id: str, query: str, results: Any) -> bool:
        """Add search query to user's search history"""
        session_data = self.get_session(session_id)
        if not session_data:
            return False
        
        search_entry = {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'results_count': len(results) if isinstance(results, list) else 1
        }
        
        if 'search_history' not in session_data['user_context']:
            session_data['user_context']['search_history'] = []
        
        session_data['user_context']['search_history'].append(search_entry)
        
        # Keep only last 20 searches
        if len(session_data['user_context']['search_history']) > 20:
            session_data['user_context']['search_history'] = session_data['user_context']['search_history'][-20:]
        
        return self._save_session(session_id, session_data)
    
    def is_user_authenticated(self, session_id: str) -> bool:
        """Check if user is authenticated in this session"""
        session_data = self.get_session(session_id)
        if not session_data:
            return False
        
        return session_data.get('user_context', {}).get('authenticated', False)
    
    def get_user_email(self, session_id: str) -> Optional[str]:
        """Get authenticated user's email"""
        session_data = self.get_session(session_id)
        if not session_data:
            return None
        
        return session_data.get('user_email')
    
    def get_user_context(self, session_id: str) -> Dict:
        """Get full user context including employee data and preferences"""
        session_data = self.get_session(session_id)
        if not session_data:
            return {}
        
        return session_data.get('user_context', {})
    
    def get_conversation_history(self, session_id: str, limit: int = 10) -> List[Dict]:
        """Get recent conversation history"""
        session_data = self.get_session(session_id)
        if not session_data:
            return []
        
        history = session_data.get('conversation_history', [])
        return history[-limit:] if limit > 0 else history
    
    def cleanup_old_sessions(self, days_old: int = 7):
        """Clean up sessions older than specified days"""
        current_time = time.time()
        cutoff_time = current_time - (days_old * 24 * 60 * 60)
        
        cleaned_count = 0
        for filename in os.listdir(self.sessions_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(self.sessions_dir, filename)
                if os.path.getmtime(file_path) < cutoff_time:
                    try:
                        os.remove(file_path)
                        cleaned_count += 1
                    except Exception as e:
                        print(f"Error removing old session {filename}: {e}")
        
        return cleaned_count
    
    def _save_session(self, session_id: str, session_data: Dict) -> bool:
        """Save session data to file"""
        session_file = os.path.join(self.sessions_dir, f"{session_id}.json")
        
        try:
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2, default=str)
            return True
        except Exception as e:
            print(f"Error saving session {session_id}: {e}")
            return False
    
    def list_active_sessions(self) -> List[Dict]:
        """List all active sessions with basic info"""
        sessions = []
        
        for filename in os.listdir(self.sessions_dir):
            if filename.endswith('.json'):
                session_id = filename[:-5]  # Remove .json extension
                session_data = self.get_session(session_id)
                
                if session_data:
                    sessions.append({
                        'session_id': session_id,
                        'user_email': session_data.get('user_email'),
                        'created_at': session_data.get('created_at'),
                        'last_activity': session_data.get('last_activity'),
                        'authenticated': session_data.get('user_context', {}).get('authenticated', False),
                        'message_count': len(session_data.get('conversation_history', []))
                    })
        
        # Sort by last activity
        sessions.sort(key=lambda x: x['last_activity'], reverse=True)
        return sessions


# Global session manager instance
session_manager = SessionManager()


def get_or_create_session(session_id: str = None) -> str:
    """Helper function to get existing session or create new one"""
    if session_id and session_manager.get_session(session_id):
        return session_id
    else:
        return session_manager.create_session()


def require_authentication(session_id: str) -> Dict:
    """Check if user is authenticated, return appropriate response"""
    if not session_manager.is_user_authenticated(session_id):
        return {
            'success': False,
            'requires_auth': True,
            'message': '👋 Welcome to Elig AI! To give you personalized assistance, please enter your employee email address.',
            'suggestions': [
                'john.doe@abc-company.com',
                'mary.smith@abc-company.com', 
                'kevin.brown@abc-company.com',
                'amanda.tan@abc-company.com',
                'rakesh.patel@abc-company.com'
            ]
        }
    
    return {'success': True}


if __name__ == "__main__":
    # Test the session manager
    print("Testing Session Manager...")
    
    # Create a test session
    session_id = session_manager.create_session()
    print(f"Created session: {session_id}")
    
    # Authenticate user
    session_manager.authenticate_user(session_id, "john.doe@abc-company.com", {"name": "John Doe"})
    print("User authenticated")
    
    # Add conversation messages
    session_manager.add_conversation_message(session_id, {
        'type': 'user',
        'content': 'Hello!'
    })
    
    session_manager.add_conversation_message(session_id, {
        'type': 'bot', 
        'content': 'Hi John! How can I help you today?'
    })
    
    # Get session info
    session_data = session_manager.get_session(session_id)
    print(f"Session has {len(session_data['conversation_history'])} messages")
    
    print("Session manager test completed!")