# How to Run Employee Lookup Agent

## Quick Start

### Terminal 1 - Backend (Flask API)

```bash
cd "/c/Users/Dineshtarun G/Desktop/ui path"
python api.py
```

**Backend runs on**: http://localhost:5000

### Terminal 2 - Frontend (React)

```bash
cd "/c/Users/Dineshtarun G/Desktop/ui path/frontend"
npm run dev
```

**Frontend runs on**: http://localhost:5174

## Access the App

Open in browser: **http://localhost:5174**

## Test Employees

- john.doe@abc-company.com (Senior IC - $10,000)
- mary.smith@abc-company.com (Manager - $10,000)
- kevin.brown@abc-company.com (IC - $3,000)
- amanda.tan@abc-company.com (Senior IC - $10,000)
- rakesh.patel@abc-company.com (IC - $3,000)

## Troubleshooting

### Backend not starting

1. Make sure you're in the right directory
2. Check if Python is installed: `python --version`
3. Install dependencies: `pip install -r requirements.txt`
4. Check if port 5000 is free

### Frontend not starting

1. Make sure you're in the frontend directory
2. Install dependencies: `npm install`
3. If port 5173 is busy, Vite will use 5174 (or next available)

### Connection errors

1. Make sure backend is running on port 5000
2. Check browser console for errors
3. Try refreshing the page

## Architecture

```
Browser
   ↓
Frontend (React on port 5174)
   ↓
Backend (Flask on port 5000)
   ↓
Employee Lookup Agent
   ↓
Employee_Data.csv + asset_purchase_policy.json
```

## Features

- Chat-style interface
- Real-time employee lookup
- Purchase eligibility check
- Clean, simple design
- Error handling
