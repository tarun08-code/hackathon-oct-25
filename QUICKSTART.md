# 🚀 Quick Start Guide for Beginners

This is a step-by-step guide for complete beginners to get the Employee Lookup Agent running.

## ⚡ 5-Minute Setup

### Step 1: Get a Google Gemini API Key

1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (it looks like: `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXX`)

### Step 2: Install Python (if not installed)

- **Windows**: Download from https://www.python.org/downloads/
- **Mac**: Usually pre-installed. Check by running `python3 --version` in terminal
- **Linux**: Usually pre-installed

### Step 3: Run the Setup Script

Open a terminal/command prompt in this folder and run:

```bash
python setup.py
```

This will:

- Check your Python version
- Install all required packages
- Create the employee database
- Help you set up your API key

### Step 4: Run the Agent

```bash
python employee_lookup_agent.py
```

Then enter an employee email like: `john.doe@abc-company.com`

## 🎯 Test Employees

Try these emails to test the agent:

1. `john.doe@abc-company.com` - Senior IC with $10,000 limit
2. `mary.smith@abc-company.com` - Manager with $25,000 limit
3. `kevin.brown@abc-company.com` - IC with $3,000 limit
4. `amanda.tan@abc-company.com` - Senior IC in Operations
5. `rakesh.patel@abc-company.com` - IC in Finance

## 🎬 Run Demo Mode

To test all employees automatically:

```bash
python demo.py
```

## 🐛 Common Issues

### "GEMINI_API_KEY not found"

**Solution**: Create a `.env` file with your API key:

1. Create a new file called `.env` (note the dot at the start)
2. Add this line: `GEMINI_API_KEY=your_actual_api_key_here`
3. Save the file in the project folder

### "No module named 'google.generativeai'"

**Solution**: Install dependencies:

```bash
pip install -r requirements.txt
```

### "Employee_Data.xlsx not found"

**Solution**: Generate the Excel file:

```bash
python create_employee_data.py
```

## 📖 Understanding the Code

### Main Components

1. **employee_lookup_agent.py** - The AI agent that does the work
2. **Employee_Data.xlsx** - Employee database (like your screenshot)
3. **asset_purchase_policy.json** - Rules for purchase limits
4. **.env** - Your secret API key (don't share this!)

### How It Works

```
User enters email
    ↓
Agent searches Employee_Data.xlsx
    ↓
Finds employee record
    ↓
Looks up policy in asset_purchase_policy.json
    ↓
Gemini AI generates friendly summary
    ↓
Shows result + saves JSON file
```

## 🎨 Customization Ideas

### Add More Employees

Edit `create_employee_data.py` and add to the lists:

```python
employee_data = {
    'email_id': [
        'existing@abc-company.com',
        'new.person@abc-company.com'  # Add here
    ],
    'employee_id': ['EMP001', 'EMP006'],  # Add here
    # ... and so on
}
```

Then run: `python create_employee_data.py`

### Change Purchase Limits

Edit `asset_purchase_policy.json`:

```json
{
  "IC": {
    "purchase_limit": 5000, // Change this
    "approved_items": ["Add new items here"]
  }
}
```

## 🏆 For the Hackathon

### What Makes This Special?

1. ✨ **Uses AI**: Google Gemini generates intelligent responses
2. 🎯 **Solves Real Problem**: Automates actual business process
3. 📊 **Complete Solution**: Works end-to-end with real data
4. 🧹 **Clean Code**: Well-organized and documented
5. 🚀 **Easy to Demo**: Just run and show results

### Demo Tips

1. **Start with setup.py** - Shows how easy it is to install
2. **Run for John Doe** - Senior IC with good benefits
3. **Show the AI summary** - Highlight the intelligent response
4. **Show JSON output** - Prove it's integration-ready
5. **Run demo.py** - Show it works for all employees

### Talking Points

- "This uses Google's latest Gemini AI"
- "It automatically parses employee data and company policies"
- "The AI generates context-aware, human-friendly responses"
- "Output is both user-friendly AND machine-readable"
- "Can be extended to a web app, API, or chatbot"

## 🎓 Learning Resources

- **Google Gemini**: https://ai.google.dev/docs
- **Pandas (Excel handling)**: https://pandas.pydata.org/docs/
- **Python Basics**: https://docs.python.org/3/tutorial/

## 💡 Extension Ideas

After the hackathon, you could add:

- 🌐 Web interface (Flask/Streamlit)
- 📧 Email notifications
- 🗄️ Real database (PostgreSQL)
- 🔐 User authentication
- 📱 Mobile app
- 🤖 Chatbot interface (Discord/Slack)
- 📊 Analytics dashboard
- 📄 PDF report generation

## 🤝 Getting Help

If you're stuck:

1. Check the error message carefully
2. Look in README.md for troubleshooting
3. Make sure all files are in the same folder
4. Verify your .env file has the correct API key
5. Try running setup.py again

## ✅ Pre-Demo Checklist

- [ ] .env file created with valid API key
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Employee_Data.xlsx exists
- [ ] Tested with at least one employee email
- [ ] Practiced your demo presentation
- [ ] Screenshots/recordings ready (optional)

## 🎉 You're Ready!

You now have a working AI agent. Good luck with your hackathon! 🏆

---

**Remember**: The key to winning is not just the code, but how you present it.
Focus on the problem you're solving and how AI makes it better!
