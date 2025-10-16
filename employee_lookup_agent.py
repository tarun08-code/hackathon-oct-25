"""
Employee Lookup AI Agent using Google Gemini
=============================================
This agent uses Google Gemini to intelligently process employee lookup 
and determine purchase eligibility based on company policy.
"""

import os
import json
import pandas as pd
import google.generativeai as genai
from typing import Dict, Optional
from dotenv import load_dotenv

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
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        except:
            try:
                self.model = genai.GenerativeModel('gemini-pro')
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
You are an AI assistant for ABC Company's employee purchase eligibility system.

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
    
    def lookup_employee(self, email: str) -> Dict:
        """
        Main method to lookup employee and return complete eligibility information
        
        Args:
            email: Employee email address
            
        Returns:
            Dictionary with complete employee and eligibility information
        """
        print(f"\n[INFO] Looking up employee: {email}")
        
        # Find employee
        employee = self.find_employee(email)
        if not employee:
            return {
                "success": False,
                "error": f"Employee with email '{email}' not found in database",
                "employee_email": email
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
