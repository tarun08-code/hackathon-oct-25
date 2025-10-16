"""
Employee Lookup AI Agent using Google Gemini with Session Memory
================================================================
This agent uses Google Gemini to intelligently process employee lookup 
and determine purchase eligibility based on company policy.
Now includes session management and conversation memory.
"""

import os
import json
import pandas as pd
import google.generativeai as genai
from typing import Dict, Optional
from dotenv import load_dotenv
from session_manager import session_manager, require_authentication

# Load environment variables
load_dotenv()


class EmployeeLookupAgent:
    """AI Agent for employee lookup and purchase eligibility determination"""
    
    def __init__(self, data_path: str = "Employee_Data.csv", 
                 policy_path: str = "asset_purchase_policy.json"):
        """
        Initialize the Employee Lookup Agent
        
        Args:
            data_path: Path to employee data file (CSV or Excel)
            policy_path: Path to asset purchase policy JSON file
        """
        # Configure Gemini API
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables. "
                           "Please set it in .env file")
        
        genai.configure(api_key=api_key)
        # Try different model versions, fallback if not available
        try:
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        except:
            try:
                self.model = genai.GenerativeModel('gemini-flash-latest')
            except:
                try:
                    self.model = genai.GenerativeModel('gemini-pro-latest')
                except:
                    self.model = None
                    print("[WARN] Gemini model not available, using fallback responses")
        
        # Load employee data (supports CSV and Excel)
        if data_path.endswith('.csv'):
            self.employee_df = pd.read_csv(data_path)
        else:
            self.employee_df = pd.read_excel(data_path)
        print(f"[INFO] Loaded {len(self.employee_df)} employee records")
        
        # Load policy data
        with open(policy_path, 'r') as f:
            self.policy_data = json.load(f)
        print(f"[INFO] Loaded asset purchase policy")
        
    def find_employee(self, email: str) -> Optional[Dict]:
        """
        Find employee by email ID
        
        Args:
            email: Employee email address
            
        Returns:
            Dictionary with employee details or None if not found
        """
        # Filter employee data
        employee = self.employee_df[
            self.employee_df['email_id'].str.lower() == email.lower()
        ]
        
        if employee.empty:
            return None
        
        # Convert to dictionary
        return employee.iloc[0].to_dict()
    
    def get_purchase_eligibility(self, employee_level: str) -> Optional[Dict]:
        """
        Get purchase eligibility based on employee level
        
        Args:
            employee_level: Employee level (IC, Senior IC, Manager)
            
        Returns:
            Dictionary with purchase limit and approved items
        """
        policy_rules = self.policy_data.get('policy_rules', {})
        return policy_rules.get(employee_level)
    
    def generate_intelligent_response(self, employee_data: Dict, 
                                     eligibility_data: Dict) -> str:
        """
        Use Gemini to generate an intelligent, context-aware response
        
        Args:
            employee_data: Employee details
            eligibility_data: Purchase eligibility details
            
        Returns:
            AI-generated human-friendly response
        """
        prompt = f"""
You are an AI assistant for PaperShare's employee purchase eligibility system.

Employee Information:
- Name: {employee_data['name']}
- Email: {employee_data['email_id']}
- Employee ID: {employee_data['employee_id']}
- Designation: {employee_data['designation']}
- Employee Level: {employee_data['employee_level']}
- Department: {employee_data['department']}

Purchase Eligibility:
- Purchase Limit: ${eligibility_data['purchase_limit']:,}
- Approved Items: {', '.join(eligibility_data['approved_items'])}
- Approval Required: {'Yes' if eligibility_data.get('approval_required') else 'No'}

Generate a friendly, professional summary explaining this employee's purchase eligibility. 
Make it clear, concise, and helpful. Include:
1. A greeting with the employee's name
2. Their purchase limit
3. What items they can purchase
4. Any special notes or requirements
5. A helpful closing statement

Keep it under 200 words.
"""
        
        try:
            if self.model is None:
                return self._generate_fallback_response(employee_data, eligibility_data)
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Warning: Gemini API error - {e}")
            return self._generate_fallback_response(employee_data, eligibility_data)
    
    def _generate_fallback_response(self, employee_data: Dict, 
                                   eligibility_data: Dict) -> str:
        """Generate a basic response if Gemini API fails"""
        return f"""
Hello {employee_data['name']},

Based on your employee level ({employee_data['employee_level']}), here is your purchase eligibility:

Purchase Limit: ${eligibility_data['purchase_limit']:,}

Approved Items:
{chr(10).join('• ' + item for item in eligibility_data['approved_items'])}

{'Note: Approval required from ' + eligibility_data.get('approval_level', 'supervisor') if eligibility_data.get('approval_required') else 'No special approval required.'}

For any questions, please contact your department manager.
"""
    
    def _generate_fallback_search_response(self, query: str, search_analysis: Dict, search_results: Dict) -> str:
        """Generate fallback response when Gemini API fails but we have search results"""
        response_parts = [f"🔍 **Search Results for:** {query}"]
        
        # Add employee results
        if 'employees' in search_results and search_results['employees']:
            response_parts.append("\n👥 **Matching Employees:**")
            for result in search_results['employees'][:2]:
                emp = result['employee']
                response_parts.append(f"• {emp['name']} ({emp['email_id']}) - {emp['department']}")
        
        # Add asset results
        if 'assets' in search_results and search_results['assets']:
            response_parts.append("\n🛒 **Matching Assets:**")
            for result in search_results['assets'][:3]:
                asset = result['asset']
                response_parts.append(f"• {asset['name']} - ${asset['price']:,}")
        
        # Add suggestions
        if search_analysis['suggested_searches']:
            response_parts.append("\n💡 **Try these searches:**")
            for suggestion in search_analysis['suggested_searches'][:3]:
                response_parts.append(f"• {suggestion}")
        
        return '\n'.join(response_parts) if len(response_parts) > 1 else "I can help you search for employees, assets, or policies. Try asking about a specific employee or item!"
    
    def handle_natural_language_query(self, query: str) -> str:
        """
        Use Gemini to handle natural language queries with smart search capabilities
        
        Args:
            query: User's natural language query
            
        Returns:
            AI-generated helpful response with search results
        """
        if not self.model:
            return "I'm sorry, I can only process employee email addresses. Please provide a valid email address (e.g., john.doe@abc-company.com)"
        
        # Initialize smart search if not already done
        if not hasattr(self, 'smart_search'):
            from smart_search_mcp import SmartSearchMCP
            self.smart_search = SmartSearchMCP()
        
        # Use smart search to understand the query
        search_analysis = self.smart_search.smart_query_understanding(query)
        
        # Get available employees and assets for context
        employee_emails = self.employee_df['email_id'].tolist()
        all_assets = self.smart_search.all_assets
        
        # Create comprehensive context for Gemini
        context_info = {
            'employees': employee_emails,
            'available_assets': [asset['name'] for asset in all_assets[:10]],  # Top 10 for brevity
            'asset_categories': list(set(asset['category'] for asset in all_assets)),
            'departments': list(set(emp['department'] for emp in self.employee_df.to_dict('records'))),
            'employee_levels': list(set(emp['employee_level'] for emp in self.employee_df.to_dict('records')))
        }
        
        # Perform smart searches based on detected intent
        search_results = {}
        if 'employee_search' in search_analysis['detected_types']:
            search_results['employees'] = self.smart_search.search_employees(query)[:3]
        
        if 'asset_search' in search_analysis['detected_types']:
            search_results['assets'] = self.smart_search.search_assets(query)[:5]
        
        prompt = f"""You are PaperShare's AI Assistant - a smart, helpful agent similar to Perplexity AI that can search and provide information about employees, company assets, and policies.

USER QUERY: "{query}"

SEARCH ANALYSIS:
- Detected Intent: {', '.join(search_analysis['detected_types'])}
- Mentioned Entities: {json.dumps(search_analysis['entities'], indent=2)}
- Confidence: {search_analysis['confidence']:.2f}

AVAILABLE CONTEXT:
- Employees: {len(context_info['employees'])} total ({', '.join(context_info['employees'][:3])}...)
- Asset Categories: {', '.join(context_info['asset_categories'])}
- Departments: {', '.join(context_info['departments'])}
- Employee Levels: {', '.join(context_info['employee_levels'])}

SEARCH RESULTS:
{json.dumps(search_results, indent=2) if search_results else "No specific search results"}

SUGGESTED SEARCHES:
{chr(10).join('• ' + suggestion for suggestion in search_analysis['suggested_searches'])}

Please provide a helpful, comprehensive response that:

1. **Acknowledge their query** - Show understanding of what they're asking
2. **Provide relevant information** - Use the search results if available
3. **Offer specific suggestions** - Give them actionable next steps
4. **Be conversational** - Like Perplexity, be friendly and informative
5. **Keep it concise** - Under 150 words

If they're asking about:
- **Employees**: Show matching employees and their details
- **Assets**: List relevant items with prices and suitability
- **Budgets**: Explain policy limits and eligibility
- **General questions**: Provide helpful guidance

Format your response with emojis and clear sections for better readability.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._generate_fallback_search_response(query, search_analysis, search_results)
    
    def lookup_employee_with_session(self, query: str, session_id: str) -> Dict:
        """
        Session-aware employee lookup with memory and authentication
        
        Args:
            query: Employee email address or natural language query
            session_id: User session ID for memory management
            
        Returns:
            Dictionary with complete response including session context
        """
        print(f"\n[INFO] Processing query with session: {query}")
        
        # Check if it looks like an email for authentication
        if '@' not in query or '.' not in query:
            # Check if user is authenticated for natural language queries
            auth_check = require_authentication(session_id)
            if not auth_check['success']:
                return auth_check
            
            # Handle authenticated natural language query
            ai_response = self.handle_natural_language_query_with_session(query, session_id)
            
            # Log the interaction
            session_manager.add_conversation_message(session_id, {
                'type': 'user',
                'content': query
            })
            session_manager.add_conversation_message(session_id, {
                'type': 'bot',
                'content': ai_response
            })
            
            return {
                "success": False,
                "query": query,
                "ai_response": ai_response,
                "type": "natural_language",
                "session_id": session_id
            }
        
        # Handle email input - check if it's for authentication
        if not session_manager.is_user_authenticated(session_id):
            return self.authenticate_user(query, session_id)
        
        # Authenticated user looking up another employee
        return self.lookup_employee_for_authenticated_user(query, session_id)
    
    def authenticate_user(self, email: str, session_id: str) -> Dict:
        """Authenticate user with their email"""
        employee = self.find_employee(email)
        
        if not employee:
            available_emails = self.employee_df['email_id'].tolist()
            return {
                "success": False,
                "requires_auth": True,
                "error": f"Email '{email}' not found. Please use one of these valid emails: {', '.join(available_emails[:3])}...",
                "type": "auth_failed",
                "session_id": session_id
            }
        
        # Authenticate the user
        session_manager.authenticate_user(session_id, email, employee)
        
        # Get purchase eligibility
        eligibility = self.get_purchase_eligibility(employee['employee_level'])
        
        # Generate personalized welcome message
        if self.model:
            try:
                # Initialize smart search for user context
                if not hasattr(self, 'smart_search'):
                    from smart_search_mcp import SmartSearchMCP
                    self.smart_search = SmartSearchMCP()
                
                # Get personalized asset suggestions
                suggestions = self.smart_search.get_purchase_suggestions(email, "")
                
                welcome_prompt = f"""Generate a personalized welcome message for {employee['name']} who just logged into PaperShare.

Employee Details:
- Name: {employee['name']}
- Role: {employee['designation']}
- Level: {employee['employee_level']}
- Department: {employee['department']}
- Budget: ${eligibility['purchase_limit']:,}

Make it:
1. Warm and welcoming
2. Mention their budget and what they can buy
3. Offer to help with searches
4. Include 2-3 relevant product suggestions
5. Keep it under 120 words
6. Use emojis appropriately

Format with clear sections and be helpful like a personal assistant."""
                
                response = self.model.generate_content(welcome_prompt)
                welcome_message = response.text
            except:
                welcome_message = f"Welcome {employee['name']}! I'm your PaperShare assistant. You have a ${eligibility['purchase_limit']:,} budget. How can I help you find the right equipment today?"
        else:
            welcome_message = f"Welcome {employee['name']}! You're authenticated. Budget: ${eligibility['purchase_limit']:,}"
        
        # Log authentication
        session_manager.add_conversation_message(session_id, {
            'type': 'user',
            'content': email
        })
        session_manager.add_conversation_message(session_id, {
            'type': 'bot',
            'content': welcome_message
        })
        
        return {
            "success": True,
            "authenticated": True,
            "employee_email": employee['email_id'],
            "employee_name": employee['name'],
            "welcome_message": welcome_message,
            "user_context": {
                "budget": eligibility['purchase_limit'],
                "level": employee['employee_level'],
                "department": employee['department']
            },
            "session_id": session_id,
            "type": "authentication_success"
        }
    
    def lookup_employee_for_authenticated_user(self, email: str, session_id: str) -> Dict:
        """Lookup another employee for an authenticated user"""
        user_context = session_manager.get_user_context(session_id)
        user_email = session_manager.get_user_email(session_id)
        
        # Use the original lookup method
        result = self.lookup_employee(email)
        
        # Add session context
        result["session_id"] = session_id
        result["requested_by"] = user_email
        
        # Log the interaction
        session_manager.add_conversation_message(session_id, {
            'type': 'user',
            'content': email
        })
        
        if result.get('success'):
            session_manager.add_conversation_message(session_id, {
                'type': 'bot',
                'content': result.get('ai_summary', 'Employee information retrieved.')
            })
        
        return result
    
    def handle_natural_language_query_with_session(self, query: str, session_id: str) -> str:
        """Handle natural language queries with session context and memory"""
        if not self.model:
            return "I'm sorry, natural language processing is not available right now."
        
        # Get user context and conversation history
        user_context = session_manager.get_user_context(session_id)
        conversation_history = session_manager.get_conversation_history(session_id, limit=5)
        user_email = session_manager.get_user_email(session_id)
        
        # Initialize smart search
        if not hasattr(self, 'smart_search'):
            from smart_search_mcp import SmartSearchMCP
            self.smart_search = SmartSearchMCP()
        
        # Analyze the query
        search_analysis = self.smart_search.smart_query_understanding(query)
        
        # Perform searches based on intent
        search_results = {}
        if 'asset_search' in search_analysis['detected_types']:
            search_results['assets'] = self.smart_search.search_assets(
                query, 
                user_context.get('employee_data', {}).get('employee_level'),
                user_context.get('employee_data', {}).get('purchase_limit')
            )[:5]
        
        # Get personalized suggestions if looking for products
        personalized_suggestions = {}
        if user_email and ('asset_search' in search_analysis['detected_types'] or 'recommendation' in search_analysis['detected_types']):
            personalized_suggestions = self.smart_search.get_purchase_suggestions(user_email, query)
        
        # Create comprehensive prompt with memory
        prompt = f"""You are {user_context.get('employee_data', {}).get('name', 'User')}'s personal PaperShare assistant. You have context and memory of our conversation.

CURRENT USER: {user_context.get('employee_data', {}).get('name', 'User')} ({user_context.get('employee_data', {}).get('employee_level', 'Unknown')})
BUDGET: ${user_context.get('employee_data', {}).get('purchase_limit', 0):,}
DEPARTMENT: {user_context.get('employee_data', {}).get('department', 'Unknown')}

CURRENT QUERY: "{query}"

CONVERSATION CONTEXT:
{chr(10).join([f"- {msg.get('type', 'unknown')}: {msg.get('content', '')[:50]}..." for msg in conversation_history[-3:]]) if conversation_history else "First conversation"}

SEARCH ANALYSIS:
- Intent: {', '.join(search_analysis['detected_types'])}
- Entities Found: {json.dumps(search_analysis['entities'])}

SEARCH RESULTS:
{json.dumps(search_results, indent=2) if search_results else "No specific product searches"}

PERSONALIZED SUGGESTIONS:
{json.dumps(personalized_suggestions.get('matching_assets', [])[:3], indent=2) if personalized_suggestions.get('matching_assets') else "No personalized suggestions"}

Please provide a helpful, personalized response that:

1. **Shows you remember me** - Reference our conversation or my details
2. **Answers the query** - Use search results and context
3. **Includes product links** - When showing products, include clickable URLs
4. **Stays within budget** - Remind me of budget constraints if relevant
5. **Offers next steps** - Suggest related searches or actions
6. **Be conversational** - Like a helpful personal assistant

When mentioning products, format like:
**Product Name** - $Price
[View Product](URL) | Specs: details

Keep response under 200 words and be helpful!"""
        
        try:
            response = self.model.generate_content(prompt)
            
            # Add search to history
            if search_results:
                session_manager.add_search_to_history(session_id, query, search_results)
            
            return response.text
            
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._generate_fallback_search_response_with_session(query, search_analysis, search_results, user_context)
    
    def _generate_fallback_search_response_with_session(self, query: str, search_analysis: Dict, search_results: Dict, user_context: Dict) -> str:
        """Generate fallback response with session context when Gemini fails"""
        user_name = user_context.get('employee_data', {}).get('name', 'there')
        budget = user_context.get('employee_data', {}).get('purchase_limit', 0)
        
        response_parts = [f"Hi {user_name}! 🔍 Here's what I found for: {query}"]
        
        if 'assets' in search_results and search_results['assets']:
            response_parts.append(f"\n💻 **Products within your ${budget:,} budget:**")
            for result in search_results['assets'][:3]:
                asset = result['asset']
                affordable = "✅" if result.get('affordable', True) else "⚠️"
                response_parts.append(f"{affordable} **{asset['name']}** - ${asset['price']:,}")
                if asset.get('url'):
                    response_parts.append(f"[View Product]({asset['url']})")
        
        if not search_results:
            response_parts.append(f"\n💡 Try asking about: 'MacBook options', 'company cars', or 'tablets for presentations'")
        
        return '\n'.join(response_parts)
    
    def lookup_employee(self, email: str) -> Dict:
        """
        Main method to lookup employee and return complete eligibility information
        (Legacy method - now wrapped by session-aware version)
        
        Args:
            email: Employee email address or natural language query
            
        Returns:
            Dictionary with complete employee and eligibility information
        """
        print(f"\n[INFO] Processing query: {email}")
        
        # Check if it looks like an email
        if '@' not in email or '.' not in email:
            # Handle as natural language query
            ai_response = self.handle_natural_language_query(email)
            return {
                "success": False,
                "query": email,
                "ai_response": ai_response,
                "type": "natural_language"
            }
        
        # Find employee
        employee = self.find_employee(email)
        if not employee:
            # Generate natural language response for not found
            if self.model:
                try:
                    available_emails = self.employee_df['email_id'].tolist()
                    prompt = f"""The user searched for employee email: {email}

This email was not found in the PaperShare database.

Available employees are:
{', '.join(available_emails)}

Generate a friendly, helpful response (under 80 words) that:
1. Politely tells them the email wasn't found
2. Suggests they check the spelling
3. Offers to help with one of the available emails
4. Be professional but warm"""
                    
                    response = self.model.generate_content(prompt)
                    ai_message = response.text
                except:
                    ai_message = f"Employee with email '{email}' not found in database. Please check the email address and try again."
            else:
                ai_message = f"Employee with email '{email}' not found in database. Please check the email address and try again."
            
            return {
                "success": False,
                "error": ai_message,
                "employee_email": email,
                "type": "not_found"
            }
        
        print(f"[INFO] Found employee: {employee['name']}")
        
        # Get purchase eligibility
        eligibility = self.get_purchase_eligibility(employee['employee_level'])
        if not eligibility:
            return {
                "success": False,
                "error": f"No policy found for employee level: {employee['employee_level']}",
                "employee_email": email,
                "employee_name": employee['name']
            }
        
        print(f"[INFO] Retrieved purchase eligibility for level: {employee['employee_level']}")
        
        # Generate AI response
        print(f"[INFO] Generating intelligent response using Gemini...")
        ai_summary = self.generate_intelligent_response(employee, eligibility)
        
        # Compile complete response
        result = {
            "success": True,
            "employee_email": employee['email_id'],
            "employee_id": employee['employee_id'],
            "employee_name": employee['name'],
            "designation": employee['designation'],
            "employee_level": employee['employee_level'],
            "department": employee['department'],
            "purchase_limit": eligibility['purchase_limit'],
            "currency": eligibility.get('currency', 'USD'),
            "approved_items": eligibility['approved_items'],
            "approval_required": eligibility.get('approval_required', False),
            "ai_summary": ai_summary
        }
        
        return result
    
    def display_result(self, result: Dict):
        """
        Display the lookup result in a formatted way
        
        Args:
            result: Result dictionary from lookup_employee
        """
        print("\n" + "="*70)
        print("EMPLOYEE PURCHASE ELIGIBILITY REPORT")
        print("="*70)
        
        if not result.get('success'):
            print(f"\n[ERROR] {result.get('error')}")
            return
        
        print(f"\nEmail: {result['employee_email']}")
        print(f"Name: {result['employee_name']}")
        print(f"Employee ID: {result['employee_id']}")
        print(f"Designation: {result['designation']}")
        print(f"Level: {result['employee_level']}")
        print(f"Department: {result['department']}")
        print(f"\nPurchase Limit: {result['currency']} ${result['purchase_limit']:,}")
        print(f"\nApproved Items:")
        for item in result['approved_items']:
            print(f"   - {item}")
        
        if result.get('approval_required'):
            print(f"\n[NOTE] Approval Required: Yes")
        
        print(f"\n{'='*70}")
        print("AI-GENERATED SUMMARY")
        print("="*70)
        print(result['ai_summary'])
        print("="*70)


def main():
    """Main execution function"""
    print("="*70)
    print("EMPLOYEE LOOKUP AI AGENT (Powered by Google Gemini)")
    print("="*70)
    
    try:
        # Initialize agent
        agent = EmployeeLookupAgent()
        
        # Get user input
        print("\n" + "-"*70)
        email = input("Enter employee email address: ").strip()
        
        if not email:
            print("[ERROR] Email address is required")
            return
        
        # Perform lookup
        result = agent.lookup_employee(email)
        
        # Display result
        agent.display_result(result)
        
        # Save to JSON
        output_file = f"lookup_result_{result.get('employee_id', 'unknown')}.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\n[INFO] Result saved to: {output_file}")
        
    except FileNotFoundError as e:
        print(f"\n[ERROR] Required file not found - {e}")
        print("Please ensure Employee_Data.csv and asset_purchase_policy.json exist")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
