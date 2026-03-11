"""
Silver Tier Integration Test Script
Test all MCP integrations independently of the dashboard UI.
"""

import sys
from pathlib import Path

# Change to Silver Tire directory
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

print("="*60)
print("  SILVER TIER INTEGRATION TEST")
print("="*60)
print()

# Test 1: Email MCP
print("[TEST 1] Email MCP")
print("-" * 40)
try:
    from mcp.email_mcp import send_email, load_credentials
    
    creds = load_credentials()
    if creds:
        print(f"[OK] Credentials loaded: {creds['email']}")
    else:
        print("[FAIL] Failed to load credentials")
    
    # Send test email
    print("Sending test email...")
    result = send_email(
        to="solemanseher@gmail.com",
        subject="Silver Tier Test - Manual Script",
        body="This is a test email from the integration test script."
    )
    
    if result:
        print("[OK] Email sent successfully!")
    else:
        print("[FAIL] Email send failed")
        
except Exception as e:
    print(f"[FAIL] Error: {e}")

print()

# Test 2: WhatsApp MCP
print("[TEST 2] WhatsApp MCP")
print("-" * 40)
try:
    from mcp.whatsapp_mcp import send_whatsapp_message
    
    print("Sending test WhatsApp message...")
    print("NOTE: Browser will open. First time requires QR scan.")
    
    result = send_whatsapp_message(
        phone_number="+923322580130",
        message="Test message from Silver Tier integration script!",
        headless=False
    )
    
    if result:
        print("[OK] WhatsApp message sent successfully!")
    else:
        print("[FAIL] WhatsApp send failed (or requires QR login)")
        
except Exception as e:
    print(f"[FAIL] Error: {e}")

print()

# Test 3: LinkedIn MCP
print("[TEST 3] LinkedIn MCP")
print("-" * 40)
try:
    from mcp.linkedin_post import post_to_linkedin
    
    print("Creating test LinkedIn post...")
    print("NOTE: Browser will open. First time requires login.")
    
    result = post_to_linkedin(
        message="Test post from Silver Tier integration script! #AI #Automation",
        headless=False
    )
    
    if result:
        print("[OK] LinkedIn post published successfully!")
    else:
        print("[FAIL] LinkedIn post failed (or requires login)")
        
except Exception as e:
    print(f"[FAIL] Error: {e}")

print()

# Test 4: Dashboard API
print("[TEST 4] Dashboard API")
print("-" * 40)
try:
    import requests
    
    # Health check
    response = requests.get("http://localhost:8001/api/v1/health")
    if response.status_code == 200:
        print(f"[OK] API Health: {response.json()['status']}")
    else:
        print("[FAIL] API not responding")
    
    # Test email endpoint
    print("Testing email endpoint...")
    response = requests.post(
        "http://localhost:8001/api/v1/test/email",
        json={
            "to": "solemanseher@gmail.com",
            "subject": "API Test",
            "body": "Test from API"
        }
    )
    if response.status_code == 200:
        print(f"[OK] API Email: {response.json()['message']}")
    else:
        print(f"[FAIL] API Email failed: {response.status_code}")
        
except Exception as e:
    print(f"[FAIL] API Error: {e}")

print()
print("="*60)
print("  TEST COMPLETE")
print("="*60)
print()
print("Next Steps:")
print("1. Check your email inbox for test messages")
print("2. If WhatsApp/LinkedIn failed, complete login and retry")
print("3. Open dashboard at: http://localhost:8001")
print()
