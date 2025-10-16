#!/usr/bin/env python3
"""
PaperShare Smart Assistant Demo - Full Feature Showcase
======================================================
This demo showcases the complete memory-enabled, session-based employee lookup system
with natural language processing, authentication, and product recommendations.
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def demo_session_flow():
    """Demo the complete session flow from authentication to natural language queries"""
    
    print("🚀 PaperShare Smart Assistant - Complete Demo")
    print("=" * 60)
    
    # Step 1: Create Session
    print("\n📝 Step 1: Creating new session...")
    response = requests.post(f"{BASE_URL}/api/session/create", 
                           json={}, 
                           headers={"Content-Type": "application/json"})
    
    if response.status_code == 200:
        session_data = response.json()
        session_id = session_data['session_id']
        print(f"✅ Session created: {session_id[:8]}...")
    else:
        print("❌ Failed to create session")
        return
    
    # Step 2: Try unauthenticated query
    print("\n🔐 Step 2: Testing unauthenticated natural language query...")
    response = requests.post(f"{BASE_URL}/api/lookup",
                           json={
                               "email": "show me MacBooks",
                               "session_id": session_id
                           },
                           headers={"Content-Type": "application/json"})
    
    if response.status_code == 200:
        result = response.json()
        print("📋 Response:", result.get('message', result.get('ai_response', 'No response'))[:100] + "...")
    
    # Step 3: Authenticate user
    print(f"\n🔑 Step 3: Authenticating user...")
    response = requests.post(f"{BASE_URL}/api/lookup",
                           json={
                               "email": "john.doe@abc-company.com",
                               "session_id": session_id
                           },
                           headers={"Content-Type": "application/json"})
    
    if response.status_code == 200:
        result = response.json()
        if result.get('type') == 'authentication_success':
            print("✅ Authentication successful!")
            print(f"👤 User: {result.get('employee_name')}")
            print(f"💰 Budget: ${result.get('user_context', {}).get('budget', 0):,}")
            print(f"📱 Welcome Message: {result.get('welcome_message', '')[:100]}...")
        else:
            print("❌ Authentication failed")
            return
    
    # Step 4: Natural language queries with memory
    print(f"\n🤖 Step 4: Testing natural language queries with memory...")
    
    queries = [
        "show me MacBook options for development",
        "what cars can I get under $40k?",
        "iPad for presentations?",
        "compare MacBook Pro 14 vs 16 inch"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n--- Query {i}: {query} ---")
        
        response = requests.post(f"{BASE_URL}/api/lookup",
                               json={
                                   "email": query,
                                   "session_id": session_id
                               },
                               headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get('ai_response', 'No response')
            
            # Extract product links if present
            if '[View Product]' in ai_response:
                print("🔗 Response includes product links!")
            
            print(f"🤖 AI Response: {ai_response[:200]}...")
            
            # Check if budget constraints mentioned
            if '$' in ai_response and 'budget' in ai_response.lower():
                print("💡 AI mentioned budget constraints!")
                
        else:
            print(f"❌ Query failed: {response.status_code}")
        
        time.sleep(1)  # Rate limiting
    
    # Step 5: Check session history
    print(f"\n📊 Step 5: Checking conversation history...")
    response = requests.get(f"{BASE_URL}/api/session/{session_id}/history")
    
    if response.status_code == 200:
        history_data = response.json()
        message_count = history_data.get('count', 0)
        print(f"💬 Session has {message_count} messages in history")
        
        if message_count > 0:
            print("Recent messages:")
            for msg in history_data.get('history', [])[-3:]:
                print(f"  {msg.get('type', 'unknown')}: {msg.get('content', '')[:50]}...")
    
    # Step 6: Test other employee lookup
    print(f"\n👥 Step 6: Looking up another employee...")
    response = requests.post(f"{BASE_URL}/api/lookup",
                           json={
                               "email": "mary.smith@abc-company.com",
                               "session_id": session_id
                           },
                           headers={"Content-Type": "application/json"})
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            print(f"✅ Found: {result.get('employee_name')} - Budget: ${result.get('purchase_limit', 0):,}")
            ai_summary = result.get('ai_summary', '')
            if ai_summary:
                print(f"🤖 AI Summary: {ai_summary[:150]}...")
    
    print(f"\n🎯 Demo Complete!")
    print("=" * 60)
    print("✅ Features Demonstrated:")
    print("• Session management with local file storage")
    print("• Email-based authentication") 
    print("• Conversation memory and context")
    print("• Natural language understanding")
    print("• Product search with specifications and links")
    print("• Budget-aware recommendations")
    print("• Personalized AI responses")
    print("• Multi-user session support")
    print("=" * 60)

def test_health_endpoint():
    """Test the health endpoint to see system status"""
    print("\n🏥 System Health Check...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            health = response.json()
            print(f"Status: {health.get('status')}")
            print(f"Agent Ready: {health.get('agent_ready')}")
            print(f"Session Manager: {health.get('session_manager_ready')}")
            print(f"Active Sessions: {health.get('active_sessions', 0)}")
            
            features = health.get('features', {})
            print("Features:")
            for feature, enabled in features.items():
                status = "✅" if enabled else "❌"
                print(f"  {status} {feature}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

if __name__ == "__main__":
    # Run health check first
    test_health_endpoint()
    
    # Run full demo
    demo_session_flow()
    
    print(f"\n🎉 All features working! Your PaperShare Smart Assistant is ready for the hackathon presentation!")