# Employee Lookup Agent - Web UI

Simple chat-like interface for the Employee Lookup Agent built with React, TypeScript, and Tailwind CSS.

## Architecture

```
Backend (Flask)           Frontend (React)
Port: 5000                Port: 5173
│                         │
├─ /api/lookup           ├─ Chat Interface
├─ /api/health           └─ Employee Lookup
└─ Employee Agent
```

## Running the Application

### Option 1: Run Both Servers

**Terminal 1 - Backend:**

```bash
cd "c:\Users\Dineshtarun G\Desktop\ui path"
python api.py
```

**Terminal 2 - Frontend:**

```bash
cd "c:\Users\Dineshtarun G\Desktop\ui path\frontend"
npm run dev
```

Then open: http://localhost:5173

### Option 2: Use the Start Script (Linux/Mac)

```bash
./start.sh
```

## Features

- Clean chat interface
- Real-time employee lookup
- Displays employee details, purchase limits, and approved items
- Error handling for invalid emails
- Loading states
- Simple and professional design

## Tech Stack

- **Frontend:** React 19, TypeScript, Tailwind CSS, Vite
- **Backend:** Python, Flask, Flask-CORS
- **AI:** Google Gemini API

## API Endpoints

### POST /api/lookup

Lookup employee by email

```json
{
  "email": "john.doe@abc-company.com"
}
```

Response:

```json
{
  "success": true,
  "employee_name": "John Doe",
  "employee_email": "john.doe@abc-company.com",
  "employee_level": "Senior IC",
  "purchase_limit": 10000,
  "approved_items": ["MacBook", "Company Car"],
  "department": "IT",
  "designation": "Senior Consultant"
}
```

### GET /api/health

Health check endpoint

## Development

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
pip install -r requirements.txt
python api.py
```

## Build for Production

```bash
cd frontend
npm run build
```

The build output will be in `frontend/dist/`

## Troubleshooting

**Backend not connecting:**

- Make sure Flask is running on port 5000
- Check that Employee_Data.csv exists
- Verify Gemini API key is in .env file

**Frontend errors:**

- Run `npm install` in the frontend folder
- Clear browser cache
- Check browser console for errors

**CORS errors:**

- flask-cors is installed and configured
- Backend allows requests from localhost:5173

## Project Structure

```
frontend/
├── src/
│   ├── App.tsx           # Main chat component
│   ├── index.css         # Tailwind styles
│   └── main.tsx          # Entry point
├── package.json
├── tailwind.config.js
└── vite.config.ts

api.py                     # Flask backend
employee_lookup_agent.py   # AI agent
Employee_Data.csv          # Employee database
```

## Usage

1. Start both servers
2. Open http://localhost:5173
3. Enter an employee email (e.g., john.doe@abc-company.com)
4. Click "Send"
5. View employee details and purchase eligibility

## Sample Emails to Test

- john.doe@abc-company.com (Senior IC)
- mary.smith@abc-company.com (Manager)
- kevin.brown@abc-company.com (IC)
- amanda.tan@abc-company.com (Senior IC)
- rakesh.patel@abc-company.com (IC)
