"""
WhatsApp MCP - Fixed Version with Multiple Selector Support
Also exports process_approved_whatsapp for orchestrator
"""
from playwright.sync_api import sync_playwright
import time
from pathlib import Path
import sys

def p(msg):
    print(msg, flush=True)

# Session directory - use absolute path based on script location
BASE_DIR = Path(__file__).parent.parent.parent
SESSION_DIR = BASE_DIR / "whatsapp_session"
SESSION_DIR.mkdir(exist_ok=True, parents=True)

def main():
    """Main WhatsApp MCP execution."""
    p("="*60)
    p("WhatsApp MCP - Starting...")
    p("="*60)

    # Get test message - use absolute path
    approved_dir = BASE_DIR / "Approved" / "WhatsApp"
    files = list(approved_dir.glob("*.md")) if approved_dir.exists() else []

    if not files:
        p("[ERROR] No files in ../Approved/WhatsApp")
        # Also check in Approved/WhatsApp
        approved_dir2 = BASE_DIR / "Approved" / "WhatsApp"
        files = list(approved_dir2.glob("*.md")) if approved_dir2.exists() else []
    
    if files:
        approved_dir = approved_dir2
        p("[INFO] Found files in Approved/WhatsApp")

    if not files:
        p("[ERROR] No WhatsApp files found to send")
        sys.exit(1)

    file = files[0]
    p(f"[INFO] Processing: {file.name}")

    content = file.read_text()
    phone = None
    message = None

    # Parse phone and message - handle multiple formats
    for line in content.split('\n'):
        line_stripped = line.strip()
        # Format: - **Phone**: +923322580130  or  - Phone: +923001234567
        if '**Phone**' in line or '**To Phone**' in line or line_stripped.startswith('- Phone:') or line_stripped.startswith('- **Phone'):
            phone = line.split(':', 1)[1].strip() if ':' in line else ''
            phone = phone.replace('**', '').strip()
            # Remove any trailing description like "(international format)"
            if '(' in phone:
                phone = phone.split('(')[0].strip()
        # Format: - **Message**: Test message  or  - Message: "Test message"
        elif '**Message**' in line or '**Message Body**' in line or line_stripped.startswith('- Message:'):
            message = line.split(':', 1)[1].strip() if ':' in line else ''
            message = message.replace('**', '').strip()
            # Remove quotes if present
            if message.startswith('"') and message.endswith('"'):
                message = message[1:-1]
        # Also try simple format: Phone: +923322580130
        elif line_stripped.startswith('Phone:') or line_stripped.startswith('To Phone:'):
            phone = line.split(':', 1)[1].strip()
        elif line_stripped.startswith('Message:') or line_stripped.startswith('Message Body:'):
            message = line.split(':', 1)[1].strip()

    if not phone or not message:
        p("[ERROR] Still could not parse - check file format")
        sys.exit(1)

    phone = phone.replace(' ', '').replace('(', '').replace(')', '').replace('-', '').replace('+', '')
    p(f"[INFO] Phone: {phone}")
    p(f"[INFO] Message: {message[:40]}...")

    p("\n[INFO] Launching browser...")

    try:
        with sync_playwright() as pwy:
            # Use persistent context for session storage
            context = pwy.chromium.launch_persistent_context(
                user_data_dir=str(SESSION_DIR),
                headless=False,
                viewport={'width': 1280, 'height': 800},
                args=['--disable-blink-features=AutomationControlled', '--no-sandbox'],
                slow_mo=100
            )

            page = context.pages[0] if context.pages else context.new_page()
        
        p("[INFO] Opening WhatsApp Web...")
        
        # Navigate with longer timeout
        try:
            page.goto("https://web.whatsapp.com/", timeout=90000, wait_until='commit')
            p("[OK] Page loaded")
            time.sleep(5)
        except Exception as e:
            p(f"[WARN] Load issue: {e}")
            p("[INFO] Retrying...")
            try:
                page.reload()
                time.sleep(5)
            except:
                pass
        
        p("\n[INFO] Checking login status...")
        
        # Check if logged in - try multiple selectors
        logged_in = False
        login_selectors = [
            "div[data-testid='chat-list']",
            "div[aria-label='Chat list']",
            "span[data-icon='chat']"
        ]
        
        for sel in login_selectors:
            try:
                if page.is_visible(sel, timeout=3000):
                    p(f"[OK] Already logged in! (found: {sel})")
                    logged_in = True
                    break
            except:
                continue
        
        if not logged_in:
            p("\n[!] QR CODE IS DISPLAYED")
            p("[!] PLEASE SCAN WITH WHATSAPP MOBILE APP NOW")
            p("[!] Waiting 120 seconds...\n")
            
            # Wait for login
            for i in range(40):
                time.sleep(3)
                for sel in login_selectors:
                    try:
                        if page.is_visible(sel, timeout=2000):
                            p(f"\n[OK] LOGIN DETECTED! (found: {sel})")
                            p("[INFO] Waiting for page to initialize...")
                            time.sleep(5)
                            logged_in = True
                            break
                    except:
                        continue
                if logged_in:
                    break
                if i % 10 == 0 and i > 0:
                    p(f"    Still waiting... ({i*3}s)")
            
            if not logged_in:
                p("\n[ERROR] Login timeout!")
                context.close()
                sys.exit(1)
        
        # Send message
        p("\n[INFO] Sending message...")
        clean_phone = phone.replace('+', '')
        
        # Try multiple selectors for search box
        search_selectors = [
            "div[contenteditable='true'][data-tab='3']",
            "div[contenteditable='true'][role='textbox']",
            "div[aria-label='Search or start new chat']",
            "div[xid='search']",
            "label[aria-label='Search']"
        ]
        
        search_box = None
        for sel in search_selectors:
            try:
                if page.is_visible(sel, timeout=3000):
                    search_box = page.locator(sel).first
                    p(f"[OK] Found search box: {sel}")
                    break
            except:
                continue
        
        if search_box:
            try:
                search_box.click()
                time.sleep(1)
                search_box.fill(clean_phone)
                time.sleep(3)
                p(f"[OK] Typed phone: {clean_phone}")
            except Exception as e:
                p(f"[WARN] Could not type in search: {e}")
        else:
            p("[WARN] Could not find search box")
        
        # Try to click the contact
        time.sleep(2)
        contact_selectors = [
            f"span:has-text('{clean_phone}')",
            f"span[title*='{clean_phone}']",
            f"div[role='button'][tabindex='0']:has-text('{clean_phone}')"
        ]
        
        contact_clicked = False
        for cs in contact_selectors:
            try:
                page.click(cs, timeout=5000)
                p(f"[OK] Contact clicked: {cs}")
                contact_clicked = True
                break
            except:
                continue
        
        if not contact_clicked:
            p("[WARN] Could not click contact - trying Enter in search")
            try:
                search_box.press("Enter")
                time.sleep(3)
            except:
                pass
        
        # Wait longer for chat to load
        p("[INFO] Waiting for chat to load...")
        time.sleep(5)
        
        # Try multiple selectors for message input
        msg_selectors = [
            "div[contenteditable='true'][data-tab='10']",
            "div[contenteditable='true'][role='textbox'][tabindex='0']",
            "footer div[contenteditable='true']",
            "div[aria-label='Type a message']",
            "div[data-placeholder='Type a message']",
            "div[contenteditable='true']"
        ]
        
        msg_box = None
        for sel in msg_selectors:
            try:
                if page.is_visible(sel, timeout=3000):
                    msg_box = page.locator(sel).first
                    p(f"[OK] Found message box: {sel}")
                    break
            except:
                continue
        
        if msg_box:
            try:
                msg_box.click()
                time.sleep(1)
                msg_box.fill(message)
                time.sleep(2)
                p("[OK] Message typed")
            except Exception as e:
                p(f"[WARN] Could not type message: {e}")
        else:
            p("[ERROR] Could not find message box")
            p("[INFO] Keeping browser open for manual send...")
            time.sleep(60)
            context.close()
            sys.exit(1)
        
        # Try to send
        send_selectors = [
            "button[data-testid='compose-btn-send']",
            "button[aria-label='Send']",
            "button[data-icon='send']",
            "span[data-icon='send']"
        ]
        
        sent = False
        for sel in send_selectors:
            try:
                page.click(sel, timeout=5000)
                p(f"[OK] Clicked send: {sel}")
                sent = True
                break
            except:
                continue
        
        if not sent:
            p("[INFO] Trying Enter key to send...")
            try:
                msg_box.press("Enter")
                time.sleep(3)
                sent = True
            except:
                pass
        
        if sent:
            p("\n[OK] MESSAGE SENT!")
        else:
            p("[WARN] Could not send - browser open for manual")
            time.sleep(30)

        # Move to Done
        done_dir = Path("../Done")
        done_dir.mkdir(parents=True, exist_ok=True)
        target = done_dir / f"SENT_WHATSAPP_{file.name}"
        try:
            file.replace(target)
            p("[OK] File moved to Done/")
        except Exception as e:
            p(f"[WARN] Could not move file: {e}")

        context.close()
        p("\n[DONE] Complete!")
        
    except Exception as e:
        p(f"[ERROR] Fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


# Orchestrator function - called by orchestrator.py
def process_approved_whatsapp():
    """Process approved WhatsApp messages - called by orchestrator."""
    # Check if there are files to process first
    approved_dir = Path("../Approved/WhatsApp")
    if not approved_dir.exists():
        approved_dir = Path("Approved/WhatsApp")

    files = list(approved_dir.glob("*.md")) if approved_dir.exists() else []

    if not files:
        p("[INFO] No WhatsApp files to process")
        return

    # There are files, run the main logic
    main()


if __name__ == "__main__":
    main()
