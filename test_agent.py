"""
Demo script to test the Employee Lookup Agent
"""
from employee_lookup_agent import EmployeeLookupAgent
import json

def test_agent():
    print("="*70)
    print("🧪 TESTING EMPLOYEE LOOKUP AI AGENT")
    print("="*70)
    
    # Initialize agent
    agent = EmployeeLookupAgent()
    
    # Test cases
    test_emails = [
        'john.doe@abc-company.com',      # Senior IC
        'mary.smith@abc-company.com',    # Manager
        'kevin.brown@abc-company.com',   # IC
        'invalid@example.com'             # Not found
    ]
    
    for email in test_emails:
        print(f"\n{'='*70}")
        print(f"Testing: {email}")
        print('='*70)
        
        result = agent.lookup_employee(email)
        agent.display_result(result)
        
        # Save each result
        if result.get('success'):
            filename = f"test_result_{result['employee_id']}.json"
            with open(filename, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\n💾 Saved to: {filename}")
        
        print("\n" + "="*70)
        input("Press Enter to continue to next test...")

if __name__ == "__main__":
    test_agent()
