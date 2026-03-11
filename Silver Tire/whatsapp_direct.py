"""
WhatsApp Direct Sender - Uses your already-open Chrome browser
This will work if you're already logged into WhatsApp Web in Chrome
"""
import subprocess
import time
import sys

def send_via_chrome():
    """Send WhatsApp message using already-open Chrome with WhatsApp Web."""
    
    print("="*60)
    print("WHATSAPP DIRECT SENDER")
    print("="*60)
    print()
    print("This will open WhatsApp Web in your Chrome browser.")
    print("Since you're already logged in, it should work immediately!")
    print()
    
    phone = "923322580130"
    message = "Test message from Silver Tier Dashboard!"
    
    # Open WhatsApp Web with direct chat link
    whatsapp_url = f"https://web.whatsapp.com/send?phone={phone}&text={message.replace(' ', '%20')}"
    
    print(f"Opening: {whatsapp_url}")
    print()
    
    # Try to open in Chrome
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    
    chrome_path = None
    for path in chrome_paths:
        import os
        if os.path.exists(path):
            chrome_path = path
            break
    
    if chrome_path:
        print(f"Found Chrome: {chrome_path}")
        subprocess.Popen([chrome_path, whatsapp_url])
        print("[OK] Chrome opened with WhatsApp Web!")
        print()
        print("Next steps:")
        print("1. WhatsApp Web should load in Chrome")
        print("2. Since you're already logged in, it will open the chat")
        print("3. Message will be pre-filled")
        print("4. Press Enter to send")
        print()
        return True
    else:
        # Fallback to default browser
        import webbrowser
        webbrowser.open(whatsapp_url)
        print("[OK] Opened in default browser!")
        print()
        return True

if __name__ == "__main__":
    send_via_chrome()
