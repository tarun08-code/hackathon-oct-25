"""
Setup Script for Employee Lookup Agent
======================================
This script helps you set up the project quickly.
"""

import os
import subprocess
import sys


def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(text)
    print("="*70)


def check_python_version():
    """Check if Python version is adequate"""
    print_header("📋 Checking Python Version")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        return False
    
    print("✓ Python version is adequate")
    return True


def install_dependencies():
    """Install required packages"""
    print_header("📦 Installing Dependencies")
    
    try:
        print("Installing packages from requirements.txt...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✓ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def create_employee_data():
    """Generate Employee_Data.xlsx"""
    print_header("📊 Creating Employee Database")
    
    if os.path.exists("Employee_Data.xlsx"):
        response = input("Employee_Data.xlsx already exists. Recreate? (y/n): ")
        if response.lower() != 'y':
            print("Skipping employee data creation")
            return True
    
    try:
        print("Running create_employee_data.py...")
        subprocess.check_call([sys.executable, "create_employee_data.py"])
        print("✓ Employee database created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create employee data: {e}")
        return False


def setup_env_file():
    """Guide user through .env setup"""
    print_header("🔑 Setting Up API Key")
    
    if os.path.exists(".env"):
        print("⚠️  .env file already exists")
        response = input("Do you want to update it? (y/n): ")
        if response.lower() != 'y':
            print("Skipping .env setup")
            return True
    
    print("\nTo use this agent, you need a Google Gemini API key.")
    print("Get one here: https://makersuite.google.com/app/apikey")
    print("\nOnce you have your API key:")
    
    api_key = input("\nEnter your Gemini API key (or press Enter to skip): ").strip()
    
    if not api_key:
        print("\n⚠️  Skipping API key setup")
        print("You'll need to create a .env file manually with:")
        print("GEMINI_API_KEY=your_api_key_here")
        return True
    
    try:
        with open(".env", "w") as f:
            f.write(f"GEMINI_API_KEY={api_key}\n")
        print("✓ .env file created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False


def verify_files():
    """Verify all required files exist"""
    print_header("✅ Verifying Project Files")
    
    required_files = [
        "employee_lookup_agent.py",
        "asset_purchase_policy.json",
        "requirements.txt",
        "README.md"
    ]
    
    all_present = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"❌ {file} - MISSING")
            all_present = False
    
    return all_present


def main():
    """Main setup function"""
    print("="*70)
    print("🚀 EMPLOYEE LOOKUP AGENT - SETUP WIZARD")
    print("="*70)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Verify files
    if not verify_files():
        print("\n❌ Some required files are missing!")
        return
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed at dependency installation")
        return
    
    # Create employee data
    if not create_employee_data():
        print("\n❌ Setup failed at employee data creation")
        return
    
    # Setup .env
    if not setup_env_file():
        print("\n⚠️  Setup completed with warnings")
    
    # Success!
    print_header("🎉 Setup Complete!")
    print("\nYour Employee Lookup Agent is ready to use!")
    print("\nNext steps:")
    print("1. Make sure you have added your GEMINI_API_KEY to the .env file")
    print("2. Run the agent: python employee_lookup_agent.py")
    print("3. Or run the demo: python demo.py")
    print("\nFor more information, see README.md")


if __name__ == "__main__":
    main()
