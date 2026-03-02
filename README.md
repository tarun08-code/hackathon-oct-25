# Employee Lookup AI Agent

An AI-powered agent that automates employee purchase eligibility validation using Google Gemini API.

## Overview

This project automates ABC Company's employee purchase eligibility validation process. The agent:

1. Takes employee email as input
2. Retrieves employee data from CSV database
3. Determines purchase eligibility from policy rules
4. Uses Google Gemini AI to generate intelligent responses
5. Returns structured JSON output with employee details and purchase limits

## Features

- AI-Powered Responses using Google Gemini
- Structured Data Processing (CSV and JSON)
- Complete Employee Lookup
- Policy-Based Eligibility Determination
- JSON Output for Integration
- Simple Command-Line Interface

## Project Structure

```
├── employee_lookup_agent.py      # Main AI agent script
├── Employee_Data.csv              # Employee database
├── asset_purchase_policy.json    # Purchase policy rules
├── create_employee_data.py       # Script to generate data file
├── demo.py                        # Demo script
├── test_agent.py                  # Test script
├── requirements.txt               # Python dependencies
├── .env                          # API keys
└── README.md                     # Documentation
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Google Gemini API Key

### Setup

1. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

2. Set up your Gemini API Key

   Create a `.env` file:

   ```bash
   GEMINI_API_KEY=your_api_key_here
   ```

3. Generate employee data (if needed)

   ```bash
   python create_employee_data.py
   ```

## Usage

### Run the Agent

```bash
python employee_lookup_agent.py
```

Enter an employee email when prompted:

- john.doe@abc-company.com
- mary.smith@abc-company.com
- kevin.brown@abc-company.com

### Run Demo

Test all employees automatically:

```bash
python demo.py
```

## Example Output

```
======================================================================
EMPLOYEE PURCHASE ELIGIBILITY REPORT
======================================================================

Email: john.doe@abc-company.com
Name: John Doe
Employee ID: EMP001
Designation: Senior Consultant
Level: Senior IC
Department: IT

Purchase Limit: USD $10,000

Approved Items:
   - Apple MacBook for development and engineering activities
   - Company Car (with business justification and approval)

[NOTE] Approval Required: Yes
======================================================================
```

## JSON Output Format

```json
{
  "success": true,
  "employee_email": "john.doe@abc-company.com",
  "employee_id": "EMP001",
  "employee_name": "John Doe",
  "designation": "Senior Consultant",
  "employee_level": "Senior IC",
  "department": "IT",
  "purchase_limit": 10000,
  "currency": "USD",
  "approved_items": [
    "Apple MacBook for development and engineering activities",
    "Company Car (with business justification and approval)"
  ],
  "approval_required": true
}
```

## Employee Levels

| Level     | Purchase Limit | Approved Items                             |
| --------- | -------------- | ------------------------------------------ |
| IC        | $3,000         | Lenovo Laptop (standard spec)              |
| Senior IC | $10,000        | Apple MacBook, Company Car (with approval) |
| Manager   | $10,000        | Apple MacBook, Company Car                 |

## Sample Employees

1. john.doe@abc-company.com - Senior IC, IT
2. mary.smith@abc-company.com - Manager, Engineering
3. kevin.brown@abc-company.com - IC, IT
4. amanda.tan@abc-company.com - Senior IC, Operations
5. rakesh.patel@abc-company.com - IC, Finance

## Customization

### Add New Employees

Edit `Employee_Data.csv`:

```csv
email_id,employee_id,name,designation,employee_level,department
new.employee@abc-company.com,EMP006,New Employee,Developer,IC,Engineering
```

### Modify Purchase Policy

Edit `asset_purchase_policy.json`:

```json
{
  "policy_rules": {
    "IC": {
      "purchase_limit": 5000,
      "approved_items": ["Laptop", "Monitor"]
    }
  }
}
```

## Troubleshooting

**GEMINI_API_KEY not found**

- Create `.env` file with your API key

**Employee not found**

- Check email spelling
- Verify email exists in Employee_Data.csv

**Import errors**

- Run `pip install -r requirements.txt`

**CSV file not found**

- Run `python create_employee_data.py`

## Technical Stack

- Python 3
- Google Gemini AI (gemini-1.5-flash)
- pandas
- google-generativeai
- python-dotenv

## License

Educational/Hackathon Project
