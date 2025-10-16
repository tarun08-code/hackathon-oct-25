"""
Flask API for Employee Lookup Agent with Session Management
Provides REST endpoints with memory and authentication
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from employee_lookup_agent import EmployeeLookupAgent
from session_manager import session_manager, get_or_create_session
import traceback
import uuid

app = Flask(__name__)
CORS(app)

# Initialize agent once
try:
    agent = EmployeeLookupAgent()
    print("Employee Lookup Agent with Session Management initialized successfully")
except Exception as e:
    print(f"Error initializing agent: {e}")
    agent = None

@app.route('/api/lookup', methods=['POST'])
def lookup_employee():
    """Session-aware employee lookup with memory and authentication"""
    try:
        if not agent:
            return jsonify({
                'success': False,
                'error': 'Agent not initialized'
            }), 500
        
        data = request.json
        query = data.get('email', '').strip()
        session_id = data.get('session_id', '')
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Please enter an employee email address or ask me a question!'
            }), 400
        
        # Get or create session
        if not session_id:
            session_id = get_or_create_session()
        
        # Perform session-aware lookup
        result = agent.lookup_employee_with_session(query, session_id)
        
        # Always include session_id in response
        result['session_id'] = session_id
        
        # Log the request
        result_type = result.get('type', 'lookup')
        authenticated = session_manager.is_user_authenticated(session_id)
        print(f"[INFO] Query: {query} | Type: {result_type} | Success: {result.get('success')} | Auth: {authenticated} | Session: {session_id[:8]}...")
        
        return jsonify(result)
    
    except Exception as e:
        print(f"[ERROR] Error in lookup: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': 'An error occurred. Please try again.'
        }), 500

@app.route('/api/search', methods=['POST'])
def smart_search():
    """Advanced search endpoint for assets, employees, and suggestions"""
    try:
        from smart_search_mcp import SmartSearchMCP
        search_engine = SmartSearchMCP()
        
        data = request.json
        query = data.get('query', '').strip()
        search_type = data.get('type', 'all')  # all, employees, assets, suggestions
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Search query is required'
            }), 400
        
        results = {}
        
        if search_type in ['all', 'employees']:
            results['employees'] = search_engine.search_employees(query)
        
        if search_type in ['all', 'assets']:
            results['assets'] = search_engine.search_assets(query)
        
        if search_type in ['all', 'suggestions']:
            results['query_analysis'] = search_engine.smart_query_understanding(query)
        
        # Get personalized suggestions if employee email is provided
        employee_email = data.get('employee_email')
        if employee_email:
            results['personalized'] = search_engine.get_purchase_suggestions(employee_email, query)
        
        return jsonify({
            'success': True,
            'query': query,
            'results': results
        })
    
    except Exception as e:
        print(f"[ERROR] Error in smart search: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': 'Search error occurred'
        }), 500

@app.route('/api/session/create', methods=['POST'])
def create_session():
    """Create a new user session"""
    try:
        data = request.json or {}
        user_email = data.get('user_email')
        
        session_id = session_manager.create_session(user_email)
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'authenticated': bool(user_email)
        })
    
    except Exception as e:
        print(f"[ERROR] Error creating session: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to create session'
        }), 500

@app.route('/api/session/<session_id>', methods=['GET'])
def get_session(session_id):
    """Get session information"""
    try:
        session_data = session_manager.get_session(session_id)
        
        if not session_data:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        # Return safe session info (exclude sensitive data)
        safe_session = {
            'session_id': session_id,
            'authenticated': session_data.get('user_context', {}).get('authenticated', False),
            'user_email': session_data.get('user_email'),
            'created_at': session_data.get('created_at'),
            'last_activity': session_data.get('last_activity'),
            'message_count': len(session_data.get('conversation_history', []))
        }
        
        return jsonify({
            'success': True,
            'session': safe_session
        })
    
    except Exception as e:
        print(f"[ERROR] Error getting session: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get session'
        }), 500

@app.route('/api/session/<session_id>/history', methods=['GET'])
def get_conversation_history(session_id):
    """Get conversation history for a session"""
    try:
        limit = request.args.get('limit', 20, type=int)
        history = session_manager.get_conversation_history(session_id, limit)
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'history': history,
            'count': len(history)
        })
    
    except Exception as e:
        print(f"[ERROR] Error getting history: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get conversation history'
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint with session stats"""
    try:
        active_sessions = session_manager.list_active_sessions()
        
        return jsonify({
            'status': 'ok',
            'agent_ready': agent is not None,
            'session_manager_ready': True,
            'active_sessions': len(active_sessions),
            'features': {
                'authentication': True,
                'conversation_memory': True,
                'smart_search': True,
                'product_links': True
            }
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'agent_ready': agent is not None,
            'session_manager_ready': False,
            'error': str(e)
        })

@app.route('/')
def home():
    """Root endpoint"""
    return jsonify({
        'message': 'Employee Lookup Agent API',
        'version': '1.0',
        'endpoints': {
            '/api/lookup': 'POST - Lookup employee by email',
            '/api/health': 'GET - Health check'
        }
    })

if __name__ == '__main__':
    print("Starting Employee Lookup Agent API on http://localhost:5000")
    print("Frontend should run on http://localhost:5173")
    app.run(debug=True, port=5000, host='0.0.0.0')
