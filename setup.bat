@echo off
REM Setup script for Windows users
REM Double-click this file to run setup

echo ======================================================================
echo Employee Lookup Agent - Windows Setup
echo ======================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found!
echo.

REM Run setup script
echo Running setup...
python setup.py

echo.
echo ======================================================================
echo Setup complete! Press any key to exit.
pause >nul
