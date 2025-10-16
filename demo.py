"""
Demo Script - Test all employees in the database
=================================================
This script demonstrates the Employee Lookup Agent by testing
all employees in the database automatically.
"""

import json
from employee_lookup_agent import EmployeeLookupAgent


def run_demo():
    """Run demonstration for all employees"""
    print("="*70)
    print("EMPLOYEE LOOKUP AGENT - DEMO MODE")
    print("="*70)
    
    try:
        # Initialize agent
        agent = EmployeeLookupAgent()
        
        # Get all employee emails
        employee_emails = agent.employee_df['email_id'].tolist()
        
        print(f"\n[INFO] Testing {len(employee_emails)} employees...")
        
        results = []
        
        for i, email in enumerate(employee_emails, 1):
            print(f"\n{'='*70}")
            print(f"Test {i}/{len(employee_emails)}")
            print(f"{'='*70}")
            
            # Perform lookup
            result = agent.lookup_employee(email)
            results.append(result)
            
            # Display result
            agent.display_result(result)
            
            if i < len(employee_emails):
                input("\n[Press Enter to continue to next employee...]")
        
        # Summary
        print("\n" + "="*70)
        print("DEMO SUMMARY")
        print("="*70)
        print(f"Total Lookups: {len(results)}")
        print(f"Successful: {sum(1 for r in results if r.get('success'))}")
        print(f"Failed: {sum(1 for r in results if not r.get('success'))}")
        
        # Save all results
        with open('demo_results_all.json', 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n[INFO] All results saved to: demo_results_all.json")
        
        print("\n[INFO] Demo completed successfully!")
        
    except Exception as e:
        print(f"\n[ERROR] Demo Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_demo()
