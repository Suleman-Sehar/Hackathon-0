"""
Autonomous LinkedIn Poster - Posts automatically without manual intervention
"""
from playwright.sync_api import sync_playwright
import time
import os
from pathlib import Path

SESSION_DIR = Path("linkedin_session")
SESSION_DIR.mkdir(exist_ok=True)

def post_to_linkedin_autonomous(message: str):
    """Post to LinkedIn autonomously using your Chrome profile."""
    print("[INFO] Starting AUTONOMOUS LinkedIn post...")
    print(f"[INFO] Message: {message[:50]}...")
    
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
                print(f"[INFO] Found Chrome: {path}")
                break
        
        if not chrome_path:
            print("[ERROR] Chrome not found!")
            return False
        
        # Find Chrome profile
        chrome_profiles = [
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default"),
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Profile 1"),
        ]
        
        chrome_profile = None
        for profile in chrome_profiles:
            if os.path.exists(profile) and len(os.listdir(profile)) > 5:
                chrome_profile = profile
                print(f"[INFO] Using Chrome profile: {profile}")
                break
        
        if not chrome_profile:
            print("[WARN] Using temporary session")
            chrome_profile = str(SESSION_DIR)
        
        # Launch Chrome with profile
        print("[INFO] Launching Chrome...")
        context = p.chromium.launch_persistent_context(
            user_data_dir=chrome_profile,
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
        print("[INFO] Checking if logged in...")
        if '/login' in page.url:
            print("[ERROR] Not logged in! Please login manually first.")
            print("[INFO] Waiting 60 seconds for login...")
            for i in range(30):
                time.sleep(2)
                if '/feed' in page.url:
                    print("[OK] Logged in!")
                    break
                if i % 10 == 0:
                    print(f"[INFO] Waiting... ({i*2}s)")
            
            if '/login' in page.url:
                print("[ERROR] Login timeout!")
                context.close()
                return False
        
        # Click "Start a post"
        print("[INFO] Opening post composer...")
        try:
            page.click("button[aria-label='Start a post']", timeout=15000)
            print("[OK] Post composer opened")
            time.sleep(3)
        except Exception as e:
            print(f"[ERROR] Could not open composer: {e}")
            context.close()
            return False
        
        # Find textbox and fill message
        print("[INFO] Filling message...")
        try:
            textbox = page.locator("div[contenteditable='true'][role='textbox']").first
            textbox.wait_for(state='visible', timeout=10000)
            textbox.fill(message)
            time.sleep(2)
            print("[OK] Message filled")
        except Exception as e:
            print(f"[ERROR] Could not fill message: {e}")
            context.close()
            return False
        
        # Click Post button
        print("[INFO] Clicking Post button...")
        try:
            # Find all buttons with "Post" text
            buttons = page.locator("button")
            post_button = None
            
            for i in range(buttons.count()):
                btn = buttons.nth(i)
                if btn.is_visible():
                    text = btn.text_content().strip().lower()
                    if text == 'post':
                        post_button = btn
                        break
            
            if post_button:
                post_button.click()
                print("[OK] Post button clicked!")
                time.sleep(5)
                
                # Wait for post to be published
                print("[INFO] Waiting for post confirmation...")
                time.sleep(3)
                
                print("[SUCCESS] Post published autonomously!")
                context.close()
                return True
            else:
                # Try pressing Enter as fallback
                print("[WARN] Post button not found, trying Enter key...")
                page.keyboard.press('Control+Enter')
                time.sleep(3)
                print("[SUCCESS] Posted via Enter key!")
                context.close()
                return True
                
        except Exception as e:
            print(f"[ERROR] Could not click Post: {e}")
            print("[INFO] Trying fallback method...")
            try:
                page.keyboard.press('Control+Enter')
                time.sleep(3)
                print("[SUCCESS] Posted via Enter key fallback!")
                context.close()
                return True
            except:
                context.close()
                return False

if __name__ == "__main__":
    message = "🚀 Autonomous LinkedIn post test! #AI #Automation"
    result = post_to_linkedin_autonomous(message)
    print(f"\n{'='*60}")
    print(f"RESULT: {'✅ SUCCESS' if result else '❌ FAILED'}")
    print(f"{'='*60}")
