"""
Flask API for Employee Lookup Agent
Provides REST endpoint for the frontend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from employee_lookup_agent import EmployeeLookupAgent
import traceback

app = Flask(__name__)
CORS(app)

# Initialize agent once
try:
    agent = EmployeeLookupAgent()
    print("Employee Lookup Agent initialized successfully")
except Exception as e:
    print(f"Error initializing agent: {e}")
    agent = None

@app.route('/api/lookup', methods=['POST'])
def lookup_employee():
    """Lookup employee by email"""
    try:
        if not agent:
            return jsonify({
                'success': False,
                'error': 'Agent not initialized'
            }), 500
        
        data = request.json
        email = data.get('email', '').strip()
        
        if not email:
            return jsonify({
                'success': False,
                'error': 'Email is required'
            }), 400
        
        # Perform lookup
        result = agent.lookup_employee(email)
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error in lookup: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'agent_ready': agent is not None
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
