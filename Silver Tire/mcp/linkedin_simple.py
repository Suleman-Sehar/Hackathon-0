"""
Simple LinkedIn Poster - Opens LinkedIn and helps you post
"""
from playwright.sync_api import sync_playwright
import time
import os
from pathlib import Path

SESSION_DIR = Path("linkedin_session")
SESSION_DIR.mkdir(exist_ok=True)

def post_to_linkedin_simple(message: str):
    """Post to LinkedIn by opening in user's Chrome profile."""
    print("[INFO] Starting LinkedIn post...")
    
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
            if os.path.exists(profile):
                chrome_profile = profile
                break
        
        if chrome_profile:
            print(f"[INFO] Using Chrome profile: {chrome_profile}")
            context = p.chromium.launch_persistent_context(
                user_data_dir=chrome_profile,
                headless=False,
                viewport={'width': 1280, 'height': 800},
                args=['--disable-blink-features=AutomationControlled', '--no-sandbox'],
                slow_mo=100,
                channel='chrome'
            )
        else:
            print("[WARN] Using temporary session")
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(SESSION_DIR),
                headless=False,
                viewport={'width': 1280, 'height': 800},
                args=['--disable-blink-features=AutomationControlled', '--no-sandbox'],
                slow_mo=100,
                channel='chrome'
            )
        
        page = context.new_page()
        
        # Go to LinkedIn
        print("[INFO] Opening LinkedIn...")
        page.goto("https://www.linkedin.com/feed/", timeout=60000)
        time.sleep(5)
        
        # Check if logged in
        if '/login' in page.url:
            print("[ERROR] Not logged in! Please login in the browser.")
            print("[INFO] Waiting 60 seconds for login...")
            for i in range(30):
                time.sleep(2)
                if '/feed' in page.url:
                    print("[OK] Logged in!")
                    break
                if i % 10 == 0:
                    print(f"[INFO] Still waiting... ({i*2}s)")
            
            if '/login' in page.url:
                print("[ERROR] Login timeout!")
                context.close()
                return False
        
        print("[INFO] Looking for post composer...")
        
        # Try to click "Start a post"
        try:
            page.click("button[aria-label='Start a post']", timeout=10000)
            print("[OK] Post composer opened")
            time.sleep(3)
        except:
            print("[WARN] Could not find post button")
            context.close()
            return False
        
        # Find textbox and fill
        print("[INFO] Filling message...")
        try:
            textbox = page.locator("div[contenteditable='true'][role='textbox']").first
            textbox.fill(message)
            time.sleep(2)
            print("[OK] Message filled")
        except Exception as e:
            print(f"[ERROR] Could not fill message: {e}")
            context.close()
            return False
        
        # Click Post button
        print("[INFO] Clicking Post...")
        try:
            post_buttons = page.locator("button:has-text('Post')")
            for i in range(post_buttons.count()):
                btn = post_buttons.nth(i)
                if btn.is_visible():
                    btn.click()
                    print("[OK] Post button clicked!")
                    time.sleep(5)
                    break
            
            print("[SUCCESS] Post should be published!")
            print("[INFO] Keeping browser open for 10 seconds...")
            time.sleep(10)
            context.close()
            return True
            
        except Exception as e:
            print(f"[ERROR] Could not click Post: {e}")
            print("[INFO] Keeping browser open for manual post...")
            time.sleep(10)
            context.close()
            return False

if __name__ == "__main__":
    message = "Test post from simple LinkedIn poster! #AI"
    result = post_to_linkedin_simple(message)
    print(f"\nResult: {'SUCCESS' if result else 'FAILED'}")
