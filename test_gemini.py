#!/usr/bin/env python3
"""
Test Gemini API setup
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

print("Testing Gemini API setup...")
print(f"GEMINI_API_KEY exists: {bool(os.getenv('GEMINI_API_KEY'))}")

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("\n❌ ERROR: GEMINI_API_KEY not found in environment variables")
    print("Please create a .env file with your Gemini API key:")
    print("GEMINI_API_KEY=your_api_key_here")
    exit(1)

try:
    genai.configure(api_key=api_key)
    print("✅ API key configured")
    
    # Test model creation with correct model name
    model = genai.GenerativeModel('gemini-2.5-flash')
    print("✅ Model created successfully")
    
    # Test a simple generation
    response = model.generate_content("Say hello!")
    print(f"✅ Test response: {response.text}")
    
except Exception as e:
    print(f"❌ Error testing Gemini API: {e}")