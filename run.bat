@echo off
REM Quick run script for Windows users
REM Double-click this file to run the agent

echo ======================================================================
echo Employee Lookup Agent - Starting...
echo ======================================================================
echo.

REM Check if .env exists
if not exist .env (
    echo ERROR: .env file not found!
    echo Please run setup.bat first or create .env manually.
    echo.
    pause
    exit /b 1
)

REM Check if Employee_Data.xlsx exists
if not exist Employee_Data.xlsx (
    echo Generating Employee_Data.xlsx...
    python create_employee_data.py
    echo.
)

REM Run the agent
python employee_lookup_agent.py

echo.
pause
