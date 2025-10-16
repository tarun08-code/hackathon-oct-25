# 🤖 Employee Lookup AI Agent (Google Gemini)

A hackathon-winning AI-powered agent that automates employee purchase eligibility validation using **Google Gemini API**.

## 📋 Overview

This project automates ABC Company's employee purchase eligibility validation process. Instead of manually checking employee profiles and company policies, this intelligent agent:

1. ✅ Takes employee email as input
2. ✅ Retrieves employee data from Excel database
3. ✅ Determines purchase eligibility from policy rules
4. ✅ Uses Google Gemini AI to generate intelligent, context-aware responses
5. ✅ Returns structured JSON output with employee details and purchase limits

## 🎯 Features

- **AI-Powered Responses**: Uses Google Gemini to generate intelligent, human-friendly summaries
- **Structured Data Processing**: Reads from Excel and JSON for easy data management
- **Complete Employee Lookup**: Retrieves all employee details in one query
- **Policy-Based Eligibility**: Automatically determines purchase limits and approved items
- **JSON Output**: Saves results in structured format for integration
- **User-Friendly CLI**: Simple command-line interface

## 📁 Project Structure

```
ui path/
├── employee_lookup_agent.py      # Main AI agent script
├── Employee_Data.xlsx             # Employee database
├── asset_purchase_policy.json    # Purchase policy rules
├── create_employee_data.py       # Script to generate Excel file
├── requirements.txt               # Python dependencies
├── .env                          # API keys (create this)
├── .env.example                  # Template for .env file
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API Key ([Get it here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone or download this project**

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Generate Employee Data Excel file**

   ```bash
   python create_employee_data.py
   ```

4. **Set up your Gemini API Key**

   Create a `.env` file in the project root:

   ```bash
   GEMINI_API_KEY=your_api_key_here
   ```

   Or use the example file:

   ```bash
   cp .env.example .env
   # Then edit .env and add your API key
   ```

### Running the Agent

```bash
python employee_lookup_agent.py
```

Then enter an employee email when prompted, for example:

- `john.doe@abc-company.com`
- `mary.smith@abc-company.com`

## 💡 Example Usage

### Input

```
Enter employee email address: john.doe@abc-company.com
```

### Output

```
======================================================================
EMPLOYEE PURCHASE ELIGIBILITY REPORT
======================================================================

📧 Email: john.doe@abc-company.com
👤 Name: John Doe
🆔 Employee ID: EMP001
💼 Designation: Senior Consultant
📊 Level: Senior IC
🏢 Department: IT

💰 Purchase Limit: USD $10,000

✅ Approved Items:
   • MacBook Pro
   • Multiple monitors
   • Premium peripherals
   • Company car & associated expenses
   • Professional development tools

======================================================================
AI-GENERATED SUMMARY
======================================================================
Hello John Doe,

As a Senior Individual Contributor at ABC Company, you have enhanced
purchase benefits. Your purchase limit is $10,000, giving you access to
premium equipment and resources.

You can purchase high-quality items including a MacBook Pro, multiple
monitors, premium peripherals, and even access company car benefits with
associated expenses. Additionally, you're eligible for professional
development tools to further your career growth.

No special approval is required for purchases within your limit. Simply
ensure all purchases are work-related and keep receipts for reimbursement.

If you have any questions about specific purchases, feel free to reach
out to your department manager.
======================================================================
```

### JSON Output

The result is also saved as `lookup_result_EMP001.json`:

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
    "MacBook Pro",
    "Multiple monitors",
    "Premium peripherals",
    "Company car & associated expenses",
    "Professional development tools"
  ],
  "approval_required": false,
  "ai_summary": "..."
}
```

## 📊 Employee Levels & Purchase Limits

| Level                       | Purchase Limit | Key Benefits                                       |
| --------------------------- | -------------- | -------------------------------------------------- |
| IC (Individual Contributor) | $3,000         | Standard laptop, monitor, peripherals              |
| Senior IC                   | $10,000        | MacBook Pro, multiple monitors, company car        |
| Manager                     | $25,000        | All Senior IC benefits + team budget + conferences |

## 🎓 Sample Employee Data

The project includes 5 sample employees:

1. **John Doe** (john.doe@abc-company.com) - Senior IC, IT
2. **Mary Smith** (mary.smith@abc-company.com) - Manager, Engineering
3. **Kevin Brown** (kevin.brown@abc-company.com) - IC, IT
4. **Amanda Tan** (amanda.tan@abc-company.com) - Senior IC, Operations
5. **Rakesh Patel** (rakesh.patel@abc-company.com) - IC, Finance

## 🔧 Customization

### Adding New Employees

Edit `Employee_Data.xlsx` or modify `create_employee_data.py` and regenerate:

```python
employee_data = {
    'email_id': ['new.employee@abc-company.com'],
    'employee_id': ['EMP006'],
    'name': ['New Employee'],
    'designation': ['Software Engineer'],
    'employee_level': ['IC'],
    'department': ['Engineering']
}
```

### Modifying Purchase Policy

Edit `asset_purchase_policy.json` to change limits or approved items:

```json
{
  "IC": {
    "purchase_limit": 5000,
    "approved_items": ["Laptop", "Monitor", "..."]
  }
}
```

## 🤝 Why This Wins Hackathons

✨ **AI Integration**: Uses Google Gemini for intelligent responses
✨ **Complete Solution**: End-to-end working prototype
✨ **Real-World Problem**: Solves actual business automation need
✨ **Clean Code**: Well-structured, documented, and maintainable
✨ **Easy Demo**: Simple CLI interface for quick demonstrations
✨ **Extensible**: Easy to add web UI, database, or API layer
✨ **Professional Output**: Both JSON and human-readable formats

## 🚀 Future Enhancements

- [ ] Web interface using Flask/Streamlit
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] REST API for system integration
- [ ] Email notifications
- [ ] Approval workflow automation
- [ ] Multi-language support
- [ ] Voice input using Gemini multimodal
- [ ] PDF report generation

## 📝 License

This is a hackathon project for educational purposes.

## 👥 Team

Built by beginners aiming to win the hackathon! 🏆

## 🆘 Troubleshooting

### "GEMINI_API_KEY not found"

Make sure you created a `.env` file with your API key.

### "Employee not found"

Check the email address spelling and ensure it exists in `Employee_Data.xlsx`.

### Import errors

Run: `pip install -r requirements.txt`

### Excel file not found

Run: `python create_employee_data.py` to generate the employee database.

## 📞 Support

For questions or issues, please check:

- Google Gemini API docs: https://ai.google.dev/docs
- Pandas documentation: https://pandas.pydata.org/docs/

---

**Happy Hacking! 🎉**
# hackathon-oct-25
