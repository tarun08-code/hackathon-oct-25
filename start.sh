#!/bin/bash

echo "Starting Employee Lookup Agent..."
echo ""
echo "Step 1: Starting Flask API Backend..."
cd "/c/Users/Dineshtarun G/Desktop/ui path"
python api.py &
API_PID=$!

echo "Waiting for API to start..."
sleep 3

echo ""
echo "Step 2: Starting React Frontend..."
cd "/c/Users/Dineshtarun G/Desktop/ui path/frontend"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "================================"
echo "Employee Lookup Agent is running!"
echo "================================"
echo ""
echo "Frontend: http://localhost:5173"
echo "Backend API: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for Ctrl+C
trap "kill $API_PID $FRONTEND_PID; exit" INT
wait
