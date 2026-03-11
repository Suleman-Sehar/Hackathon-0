"""Test WhatsApp directly"""
from mcp.whatsapp_mcp import send_whatsapp_message

print("="*60)
print("TESTING WHATSAPP")
print("="*60)

phone = "923322580130"
message = "Test message from debug script"

print(f"\nPhone: {phone}")
print(f"Message: {message[:40]}...")
print("\nStarting WhatsApp...")

try:
    result = send_whatsapp_message(phone, message, headless=False)
    print(f"\nResult: {result}")
    if result:
        print("✅ SUCCESS!")
    else:
        print("❌ FAILED!")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
