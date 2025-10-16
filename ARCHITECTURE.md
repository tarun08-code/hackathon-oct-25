# System Architecture & Flow Diagrams

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                                                                 │
│  Input: Employee Email (e.g., john.doe@abc-company.com)       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   EMPLOYEE LOOKUP AGENT                         │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Step 1: Validate Email Format                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                    │
│                            ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Step 2: Search Employee Database (Excel)                │  │
│  │  - Filter by email_id                                    │  │
│  │  - Extract employee record                               │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                    │
│                            ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Step 3: Extract Employee Level                          │  │
│  │  - IC / Senior IC / Manager                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                    │
│                            ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Step 4: Lookup Purchase Policy                          │  │
│  │  - Match level to policy rules                           │  │
│  │  - Extract limit & approved items                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                    │
│                            ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Step 5: Generate AI Summary (Gemini)                    │  │
│  │  - Create context-aware prompt                           │  │
│  │  - Call Gemini API                                       │  │
│  │  - Get intelligent response                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                    │
│                            ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Step 6: Format & Return Results                         │  │
│  │  - Compile JSON output                                   │  │
│  │  - Generate display text                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      OUTPUT GENERATION                          │
│                                                                 │
│  1. Console Display (formatted text)                           │
│  2. JSON File (structured data)                                │
│  3. AI-Generated Summary (Gemini response)                     │
└─────────────────────────────────────────────────────────────────┘
```

## 📊 Data Flow Diagram

```
┌──────────────────┐
│  User Input      │
│  (Email)         │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐      ┌─────────────────────┐
│ Employee_Data    │◄─────│ Search & Filter     │
│ Excel File       │      │ Operation           │
└──────────────────┘      └──────────┬──────────┘
                                     │
                          ┌──────────▼──────────┐
                          │ Employee Record     │
                          │ Found               │
                          └──────────┬──────────┘
                                     │
                                     ▼
┌──────────────────┐      ┌─────────────────────┐
│ Asset Purchase   │◄─────│ Policy Lookup       │
│ Policy JSON      │      │ by Level            │
└──────────────────┘      └──────────┬──────────┘
                                     │
                          ┌──────────▼──────────┐
                          │ Eligibility Data    │
                          └──────────┬──────────┘
                                     │
                                     ▼
┌──────────────────┐      ┌─────────────────────┐
│ Google Gemini    │◄─────│ Generate AI         │
│ API              │      │ Summary             │
└──────────────────┘      └──────────┬──────────┘
                                     │
                          ┌──────────▼──────────┐
                          │ Complete Result     │
                          │ Object              │
                          └──────────┬──────────┘
                                     │
                ┌────────────────────┼────────────────────┐
                ▼                    ▼                    ▼
        ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
        │ Console      │    │ JSON File    │    │ Return to    │
        │ Display      │    │ Output       │    │ Caller       │
        └──────────────┘    └──────────────┘    └──────────────┘
```

## 🔄 Sequence Diagram

```
User        Agent           Excel          Policy JSON      Gemini API
 │            │               │                  │              │
 │  email     │               │                  │              │
 ├───────────>│               │                  │              │
 │            │ search email  │                  │              │
 │            ├──────────────>│                  │              │
 │            │   record      │                  │              │
 │            │<──────────────┤                  │              │
 │            │               │                  │              │
 │            │       lookup level               │              │
 │            ├─────────────────────────────────>│              │
 │            │         policy rules             │              │
 │            │<─────────────────────────────────┤              │
 │            │               │                  │              │
 │            │     generate summary             │              │
 │            ├────────────────────────────────────────────────>│
 │            │                AI response                      │
 │            │<────────────────────────────────────────────────┤
 │            │               │                  │              │
 │   result   │               │                  │              │
 │<───────────┤               │                  │              │
 │            │               │                  │              │
```

## 🗂️ Database Schema

### Employee_Data.xlsx Structure

```
┌─────────────┬──────────────┬───────┬──────────────┬────────────────┬────────────┐
│ email_id    │ employee_id  │ name  │ designation  │ employee_level │ department │
├─────────────┼──────────────┼───────┼──────────────┼────────────────┼────────────┤
│ STRING      │ STRING       │STRING │ STRING       │ ENUM           │ STRING     │
│ PRIMARY KEY │ UNIQUE       │       │              │(IC/Senior IC/  │            │
│             │              │       │              │ Manager)       │            │
└─────────────┴──────────────┴───────┴──────────────┴────────────────┴────────────┘
```

### Policy Rules JSON Structure

```json
{
  "policy_rules": {
    "[LEVEL]": {
      "level_name": "STRING",
      "purchase_limit": NUMBER,
      "currency": "STRING",
      "approved_items": ["STRING", ...],
      "approval_required": BOOLEAN,
      "notes": "STRING"
    }
  }
}
```

## 🎯 Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    EMPLOYEE LOOKUP SYSTEM                   │
│                                                             │
│  ┌────────────────────┐      ┌──────────────────────────┐  │
│  │ CLI Interface      │      │ EmployeeLookupAgent      │  │
│  │ - Input Handler    │◄────►│ - find_employee()        │  │
│  │ - Output Display   │      │ - get_eligibility()      │  │
│  │ - Error Messages   │      │ - generate_response()    │  │
│  └────────────────────┘      └──────────┬───────────────┘  │
│                                         │                   │
│                       ┌─────────────────┼──────────────┐    │
│                       │                 │              │    │
│              ┌────────▼────────┐ ┌─────▼──────┐ ┌────▼────┐│
│              │ Data Loader     │ │ Policy     │ │ AI      ││
│              │ (Pandas)        │ │ Engine     │ │ Engine  ││
│              │ - read_excel()  │ │ - match()  │ │(Gemini) ││
│              └─────────────────┘ └────────────┘ └─────────┘│
└─────────────────────────────────────────────────────────────┘
```

## 🔐 Configuration Flow

```
┌──────────────────┐
│ .env File        │
│                  │
│ GEMINI_API_KEY=  │
│ your_key_here    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ python-dotenv    │
│ load_dotenv()    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Environment      │
│ Variables        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ genai.configure()│
│                  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Gemini API       │
│ Ready            │
└──────────────────┘
```

## 📱 Deployment Options

```
┌──────────────────────────────────────────────────────────────┐
│                    CURRENT IMPLEMENTATION                    │
│                   (CLI - Command Line)                       │
└──────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│ FUTURE       │      │ FUTURE       │      │ FUTURE       │
│ Web App      │      │ REST API     │      │ Chatbot      │
│ (Flask)      │      │ (FastAPI)    │      │ (Slack/Team) │
└──────────────┘      └──────────────┘      └──────────────┘
```

## 🎨 User Journey

```
START
  │
  ├─► User runs: python employee_lookup_agent.py
  │
  ├─► System initializes
  │   ├─► Load employee database
  │   ├─► Load policy rules
  │   └─► Configure Gemini API
  │
  ├─► Prompt: "Enter employee email address:"
  │
  ├─► User enters email
  │
  ├─► System processes
  │   ├─► Find employee
  │   ├─► Get eligibility
  │   └─► Generate AI summary
  │
  ├─► Display results
  │   ├─► Employee details
  │   ├─► Purchase limit
  │   ├─► Approved items
  │   └─► AI summary
  │
  ├─► Save JSON file
  │
END
```

## 🏗️ Class Structure

```
EmployeeLookupAgent
├── __init__(excel_path, policy_path)
│   ├─► Load employee data
│   ├─► Load policy data
│   └─► Configure Gemini
│
├── find_employee(email) → Dict
│   └─► Search Excel by email
│
├── get_purchase_eligibility(level) → Dict
│   └─► Lookup policy by level
│
├── generate_intelligent_response(emp, elig) → String
│   └─► Call Gemini API
│
├── lookup_employee(email) → Dict
│   ├─► find_employee()
│   ├─► get_purchase_eligibility()
│   └─► generate_intelligent_response()
│
└── display_result(result)
    └─► Format and print output
```

---

These diagrams explain the complete system architecture, data flow, and component interactions.
