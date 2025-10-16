import pandas as pd

# Employee data from the screenshot
employee_data = {
    'email_id': [
        'john.doe@abc-company.com',
        'mary.smith@abc-company.com',
        'kevin.brown@abc-company.com',
        'amanda.tan@abc-company.com',
        'rakesh.patel@abc-company.com'
    ],
    'employee_id': ['EMP001', 'EMP002', 'EMP003', 'EMP004', 'EMP005'],
    'name': ['John Doe', 'Mary Smith', 'Kevin Brown', 'Amanda Tan', 'Rakesh Patel'],
    'designation': [
        'Senior Consultant',
        'Engineering Manager',
        'Software Engineer',
        'Lead Consultant',
        'Associate Consultant'
    ],
    'employee_level': ['Senior IC', 'Manager', 'IC', 'Senior IC', 'IC'],
    'department': ['IT', 'Engineering', 'IT', 'Operations', 'Finance']
}

# Create DataFrame
df = pd.DataFrame(employee_data)

# Save to CSV (easier to open and edit)
df.to_csv('Employee_Data.csv', index=False)
print("[INFO] Employee_Data.csv created successfully!")

# Also save to Excel if openpyxl is available
try:
    df.to_excel('Employee_Data.xlsx', index=False, sheet_name='Employees')
    print("[INFO] Employee_Data.xlsx created successfully!")
except ImportError:
    print("[WARN] openpyxl not installed, skipping Excel file")

print(f"\n[INFO] Created {len(df)} employee records:")
print(df)
