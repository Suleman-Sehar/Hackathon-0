"""
WhatsApp MCP - Minimal Working Version
"""
from playwright.sync_api import sync_playwright
import time
from pathlib import Path
import sys

# Force flush prints
def p(msg):
    print(msg, flush=True)

SESSION_DIR = Path("whatsapp_session")
SESSION_DIR.mkdir(exist_ok=True, parents=True)

p("="*60)
p("WhatsApp MCP - Starting...")
p("="*60)

# Get test message
approved_dir = Path("Approved/WhatsApp")
files = list(approved_dir.glob("*.md")) if approved_dir.exists() else []

if not files:
    p("[ERROR] No files in Approved/WhatsApp")
    sys.exit(1)

file = files[0]
p(f"[INFO] Processing: {file.name}")

content = file.read_text()
phone = None
message = None

for line in content.split('\n'):
    if 'Phone:' in line:
        phone = line.split(':', 1)[1].strip()
    elif 'Message:' in line:
        message = line.split(':', 1)[1].strip()

if not phone or not message:
    p("[ERROR] Could not parse phone/message")
    sys.exit(1)

phone = phone.replace(' ', '').replace('(', '').replace(')', '').replace('-', '')
p(f"[INFO] Phone: {phone}")
p(f"[INFO] Message: {message[:40]}...")

# Launch browser
p("\n[1/4] Launching browser...")
try:
    with sync_playwright() as pwy:
        p("[2/4] Opening WhatsApp Web...")
        context = pwy.chromium.launch_persistent_context(
            user_data_dir=str(SESSION_DIR),
            headless=False,
            viewport={'width': 1280, 'height': 800}
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        page.goto("https://web.whatsapp.com/", timeout=60000)
        
        p("[3/4] Waiting for login (scan QR if shown)...")
        p("[ACTION] If QR code appears, scan it with your phone!")
        
        # Wait for login (max 2 minutes)
        logged_in = False
        for i in range(40):
            time.sleep(3)
            try:
                if page.is_visible("div[data-testid='chat-list']", timeout=2000):
                    p("[OK] Login detected!")
                    time.sleep(3)
                    logged_in = True
                    break
                if i % 10 == 0:
                    p(f"    Waiting... ({i*3}s)")
            except:
                pass
        
        if not logged_in:
            p("[ERROR] Login timeout!")
            context.close()
            sys.exit(1)
        
        # Send message
        p("[4/4] Sending message...")
        clean_phone = phone.replace('+', '')
        
        try:
            # Search
            page.click("div[contenteditable='true'][data-tab='3']")
            time.sleep(1)
            page.fill("div[contenteditable='true'][data-tab='3']", clean_phone)
            time.sleep(3)
            
            # Select contact
            page.click(f"span:has-text('{clean_phone}')")
            time.sleep(2)
            
            # Type
            page.fill("div[contenteditable='true'][data-tab='10']", message)
            time.sleep(2)
            
            # Send
            page.click("button[data-testid='compose-btn-send']")
            time.sleep(3)
            
            p("[OK] Message sent!")
            
            # Move to Done
            done_dir = Path("Done")
            done_dir.mkdir(exist_ok=True)
            target = done_dir / f"SENT_WHATSAPP_{file.name}"
            file.replace(target)
            p(f"[OK] File moved to Done/")
            
        except Exception as e:
            p(f"[ERROR] Send failed: {e}")
            p("[INFO] Browser will stay open for manual send...")
            time.sleep(10)
        
        context.close()
        p("\n[DONE] Complete!")
        
except Exception as e:
    p(f"[ERROR] {e}")
    sys.exit(1)
