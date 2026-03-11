"""
WhatsApp MCP - Send WhatsApp messages via browser automation.
Uses WhatsApp Web with persistent session.
"""
from playwright.sync_api import sync_playwright
import time
import random
import json
from pathlib import Path
from datetime import datetime

# Session folder
SESSION_DIR = Path("whatsapp_session")
SESSION_DIR.mkdir(exist_ok=True)

# Configuration
CONFIG_PATH = Path("credential.json")

def load_credentials():
    """Load WhatsApp credentials from config."""
    if not CONFIG_PATH.exists():
        print("[ERROR] credential.json not found")
        return None
    
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def human_delay(min_sec=1.0, max_sec=3.0):
    """Random delay to simulate human behavior."""
    time.sleep(random.uniform(min_sec, max_sec))

def send_whatsapp_message(phone_number: str, message: str, headless=False):
    """
    Send WhatsApp message to specified phone number.
    
    Args:
        phone_number: Full phone number with country code (e.g., +1234567890)
        message: Message text to send
        headless: Whether to run browser in headless mode
    
    Returns:
        bool: True if message sent successfully
    """
    with sync_playwright() as p:
        # Launch browser with persistent context
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(SESSION_DIR),
            headless=headless,
            viewport={'width': 1280, 'height': 800},
            slow_mo=100,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        page = context.new_page()
        
        # Go to WhatsApp Web
        print("[INFO] Opening WhatsApp Web...")
        page.goto("https://web.whatsapp.com/", timeout=60000)
        human_delay(3, 5)
        
        # Check if already logged in - try multiple selectors
        logged_in = False
        search_selectors = [
            'div[contenteditable="true"][data-tab="3"]',
            'div[contenteditable="true"][aria-label="Search or start new chat"]',
            'input[placeholder="Search or start new chat"]'
        ]
        
        for selector in search_selectors:
            try:
                page.wait_for_selector(selector, timeout=10000)
                print(f"[OK] Logged in - found search box")
                logged_in = True
                break
            except:
                continue
        
        if not logged_in:
            print("[INFO] Login required - please scan QR code manually...")
            print("[INFO] Waiting for manual login (60 seconds)...")
            try:
                page.wait_for_selector('div[contenteditable="true"][data-tab="3"]', timeout=60000)
                print("[OK] Login detected!")
            except:
                print("[ERROR] Login timeout. Please try again.")
                context.close()
                return False
        
        human_delay(2, 4)
        
        # Click on search box - try multiple selectors
        search_box = None
        for selector in search_selectors:
            try:
                search_box = page.locator(selector).first
                search_box.click()
                human_delay(1, 2)
                print(f"[OK] Clicked search box")
                break
            except:
                continue
        
        if not search_box:
            print("[ERROR] Could not find search box")
            context.close()
            return False
        
        # Type phone number (without + for search)
        search_number = phone_number.replace('+', '')
        print(f"[INFO] Searching for {phone_number}...")
        
        try:
            search_box.fill(search_number)
        except:
            search_box.type(search_number)
        
        human_delay(2, 4)
        
        # Wait for search results
        human_delay(1, 2)
        
        # Try to find and click the contact - look for various result elements
        contact_found = False
        
        # Method 1: Try to find by exact phone number in title
        try:
            # Look for span with the phone number as title
            contact = page.locator(f'span[title*="{search_number}"]').first
            if contact.is_visible():
                contact.click()
                print("[OK] Found contact by title")
                contact_found = True
        except:
            pass
        
        # Method 2: Try clicking first result in the list
        if not contact_found:
            try:
                # Look for any result in the search list
                results = page.locator('div[class*="_1FOT"]').all()
                if results:
                    results[0].click()
                    print("[OK] Clicked first search result")
                    contact_found = True
            except:
                pass
        
        # Method 3: Try clicking on the chat item
        if not contact_found:
            try:
                chat_item = page.locator('div[class*="_2exMM"]').first
                if chat_item.is_visible():
                    chat_item.click()
                    print("[OK] Clicked chat item")
                    contact_found = True
            except:
                pass
        
        # Method 4: Just press Enter to open the chat with that number
        if not contact_found:
            try:
                search_box.press("Enter")
                human_delay(2, 3)
                print("[OK] Pressed Enter to open chat")
                contact_found = True
            except:
                pass
        
        if not contact_found:
            print("[ERROR] Could not find or open contact")
            print("[NOTE: Make sure the number is saved in your WhatsApp contacts]")
            context.close()
            return False
        
        human_delay(2, 4)
        
        # Wait for message input box - try multiple selectors
        message_box = None
        message_selectors = [
            'div[contenteditable="true"][data-tab="10"]',
            'div[contenteditable="true"][aria-label="Type a message"]',
            'div[class*="复制"][contenteditable="true"]'
        ]
        
        for selector in message_selectors:
            try:
                message_box = page.locator(selector).first
                message_box.click()
                human_delay(1, 2)
                print(f"[OK] Found message box")
                break
            except:
                continue
        
        if not message_box:
            print("[ERROR] Could not find message input box")
            context.close()
            return False
        
        # Type message character by character (human-like)
        print(f"[INFO] Typing message...")
        message_box.click()
        human_delay(0.5, 1)
        
        for char in message:
            message_box.type(char, delay=random.uniform(30, 100))
        
        human_delay(1, 2)
        
        # Click send button - try multiple methods
        sent = False
        
        # Method 1: Click send button
        try:
            send_button = page.locator('span[data-icon="send"]').first
            if send_button.is_visible():
                send_button.click()
                human_delay(2, 4)
                print(f"[OK] Message sent via button")
                sent = True
        except:
            pass
        
        # Method 2: Press Enter
        if not sent:
            try:
                message_box.press("Enter")
                human_delay(2, 4)
                print(f"[OK] Message sent via Enter key")
                sent = True
            except:
                pass
        
        # Method 3: Try Ctrl+Enter
        if not sent:
            try:
                message_box.press("Control+Enter")
                human_delay(2, 4)
                print(f"[OK] Message sent via Ctrl+Enter")
                sent = True
            except:
                pass
        
        context.close()
        return sent

def process_approved_whatsapp():
    """Process all approved WhatsApp requests."""
    approved_dir = Path("Approved/WhatsApp")
    
    if not approved_dir.exists():
        # Try alternative location
        approved_dir = Path("Approved")
        if not approved_dir.exists():
            print("[INFO] No Approved folder")
            return 0
    
    # Find WhatsApp files
    files = []
    if approved_dir.exists():
        files = list(approved_dir.glob("*whatsapp*.md")) + list(approved_dir.glob("*WHATSAPP*.md"))
    
    if not files:
        print("[INFO] No approved WhatsApp messages to send")
        return 0
    
    sent_count = 0
    done_dir = Path("Done")
    done_dir.mkdir(exist_ok=True)
    
    for file in files:
        content = file.read_text()

        # Parse WhatsApp parameters
        phone = None
        message = None

        for line in content.split('\n'):
            # Handle multiple formats: "Phone:", "**Phone**:", "To:", etc.
            line_clean = line.strip().lstrip('-').strip()
            
            if any(line_clean.startswith(kw) for kw in ['**Phone**', 'Phone:', 'To:', 'Number:']):
                phone = line_clean.split(':', 1)[1].strip().strip('**') if ':' in line_clean else None
            elif any(line_clean.startswith(kw) for kw in ['**Message Body**', 'Message:', 'Message Body:', 'Body:']):
                message = line_clean.split(':', 1)[1].strip().strip('**') if ':' in line_clean else None

        # Extract body (everything after ---)
        parts = content.split('---', 1)
        if len(parts) > 1 and not message:
            message = parts[1].strip()
        
        if not phone or not message:
            print(f"[SKIP] Invalid WhatsApp request in {file.name}")
            continue
        
        # Clean phone number
        phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        if not phone.startswith('+'):
            phone = '+' + phone
        
        print(f"Sending WhatsApp to {phone}: {message[:50]}...")
        
        if send_whatsapp_message(phone, message, headless=False):
            # Move to Done
            target = done_dir / f"SENT_{file.name}"
            if target.exists():
                target.unlink()
            file.replace(target)
            sent_count += 1
            
            # Log to Dashboard
            log_whatsapp_sent(phone, message)
        else:
            print(f"[ERROR] Failed to send message to {phone}")
    
    return sent_count

def log_whatsapp_sent(phone: str, message: str):
    """Log sent WhatsApp to Dashboard.md"""
    dashboard_path = Path("Bronze Tire/AI_Employee_Vault/Dashboard.md")
    if not dashboard_path.exists():
        return
    
    content = dashboard_path.read_text()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Add entry
    lines = content.split('\n')
    new_lines = []
    in_section = False
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        if '## WhatsApp Sent Today' in line:
            in_section = True
        elif in_section and line.startswith('| Phone'):
            new_lines.append(f"| {phone} | {message[:40]} | Sent | {timestamp} |")
            in_section = False
    
    try:
        dashboard_path.write_text('\n'.join(new_lines))
        print(f"[LOG] WhatsApp logged to Dashboard")
    except:
        pass

def main():
    """Main entry point."""
    print("=" * 50)
    print("WhatsApp MCP")
    print("=" * 50)
    
    # Process approved messages
    sent = process_approved_whatsapp()
    print(f"[DONE] Sent {sent} WhatsApp message(s)")

if __name__ == "__main__":
    main()
