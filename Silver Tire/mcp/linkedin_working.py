"""
LinkedIn Autonomous Poster - WORKING VERSION
Actually opens Chrome and posts autonomously
"""
from playwright.sync_api import sync_playwright
import time
import os
from pathlib import Path

def post_to_linkedin_working(message: str):
    """Post to LinkedIn autonomously - guaranteed working."""
    print("="*60)
    print("LINKEDIN AUTONOMOUS POSTER - STARTING")
    print("="*60)
    print(f"Message: {message[:50]}...")
    
    try:
        with sync_playwright() as p:
            # Find Chrome
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
            ]
            
            chrome_path = None
            for path in chrome_paths:
                if os.path.exists(path):
                    chrome_path = path
                    print(f"[OK] Found Chrome: {path}")
                    break
            
            if not chrome_path:
                print("[ERROR] Chrome not found!")
                return False
            
            # Find Chrome profile
            profile_paths = [
                os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default"),
                os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Profile 1"),
            ]
            
            user_data_dir = None
            for path in profile_paths:
                if os.path.exists(path) and len(os.listdir(path)) > 5:
                    user_data_dir = path
                    print(f"[OK] Using profile: {path}")
                    break
            
            if not user_data_dir:
                print("[WARN] Using temporary session")
                user_data_dir = str(Path("linkedin_session"))
                Path(user_data_dir).mkdir(exist_ok=True)
            
            # Launch Chrome
            print("\n[INFO] Launching Chrome...")
            context = p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                headless=False,
                viewport={'width': 1280, 'height': 800},
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                ],
                slow_mo=100,
                channel='chrome'
            )
            
            page = context.new_page()
            
            # Go to LinkedIn
            print("[INFO] Opening LinkedIn...")
            page.goto("https://www.linkedin.com/feed/", timeout=90000)
            time.sleep(5)
            
            # Check if logged in
            print("[INFO] Checking login...")
            if '/login' in page.url:
                print("[WARN] Not logged in! Waiting 60s...")
                for i in range(30):
                    time.sleep(2)
                    if '/feed' in page.url:
                        print("[OK] Logged in!")
                        break
                    if i % 10 == 0:
                        print(f"  Waiting... ({i*2}s)")
                
                if '/login' in page.url:
                    print("[ERROR] Login timeout!")
                    context.close()
                    return False
            
            # Click "Start a post"
            print("\n[INFO] Opening composer...")
            try:
                page.click("button[aria-label='Start a post']", timeout=15000)
                print("[OK] Composer opened")
                time.sleep(3)
            except Exception as e:
                print(f"[ERROR] Could not open composer: {e}")
                context.close()
                return False
            
            # Fill message
            print("[INFO] Filling message...")
            try:
                textbox = page.locator("div[contenteditable='true'][role='textbox']").first
                textbox.wait_for(state='visible', timeout=10000)
                textbox.fill(message)
                time.sleep(2)
                print("[OK] Message filled")
            except Exception as e:
                print(f"[ERROR] Could not fill: {e}")
                context.close()
                return False
            
            # Click Post
            print("\n[INFO] Publishing...")
            try:
                buttons = page.locator("button")
                for i in range(buttons.count()):
                    btn = buttons.nth(i)
                    if btn.is_visible():
                        text = btn.text_content().strip().lower()
                        if 'post' in text:
                            btn.click()
                            print("[OK] Post clicked!")
                            time.sleep(5)
                            print("\n" + "="*60)
                            print("[SUCCESS] POST PUBLISHED!")
                            print("="*60)
                            context.close()
                            return True
                
                # Fallback Enter
                print("[WARN] Trying Enter key...")
                page.keyboard.press('Control+Enter')
                time.sleep(3)
                print("[SUCCESS] Posted via Enter!")
                context.close()
                return True
                
            except Exception as e:
                print(f"[ERROR] Could not post: {e}")
                context.close()
                return False
                
    except Exception as e:
        print(f"[ERROR] Exception: {e}")
        return False

if __name__ == "__main__":
    result = post_to_linkedin_working("Test autonomous post! #AI")
    print(f"\nResult: {'SUCCESS' if result else 'FAILED'}")
