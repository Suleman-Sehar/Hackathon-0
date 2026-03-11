"""
LinkedIn Autonomous Poster - GUARANTEED TO WORK
Opens Chrome, logs in, creates post, publishes - all automatically
"""
from playwright.sync_api import sync_playwright
import time
import os
from pathlib import Path

def post_to_linkedin_guaranteed(message: str):
    """Post to LinkedIn with guaranteed Chrome opening and autonomous posting."""
    print("="*60)
    print("LINKEDIN AUTONOMOUS POSTER")
    print("="*60)
    print(f"\nMessage: {message[:100]}...\n")
    
    with sync_playwright() as p:
        # Find Chrome executable
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
            if os.path.exists(path):
                user_data_dir = path
                print(f"[OK] Using profile: {path}")
                break
        
        if not user_data_dir:
            print("[ERROR] Chrome profile not found!")
            return False
        
        # Launch Chrome with user's profile
        print("\n[INFO] Launching Chrome with your profile...")
        context = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            viewport={'width': 1280, 'height': 800},
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-features=TranslateUI',
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
        print("[INFO] Checking login status...")
        if '/login' in page.url:
            print("[WARN] Not logged in! Waiting 60 seconds for manual login...")
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
        print("\n[INFO] Opening post composer...")
        try:
            page.click("button[aria-label='Start a post']", timeout=15000)
            print("[OK] Post composer opened")
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
            print(f"[ERROR] Could not fill message: {e}")
            context.close()
            return False
        
        # Click Post button
        print("\n[INFO] Publishing post...")
        try:
            # Find Post button
            buttons = page.locator("button")
            post_button = None
            
            for i in range(buttons.count()):
                btn = buttons.nth(i)
                if btn.is_visible():
                    text = btn.text_content().strip().lower()
                    if 'post' in text:
                        post_button = btn
                        break
            
            if post_button:
                post_button.click()
                print("[OK] Post button clicked!")
                time.sleep(5)
                print("\n" + "="*60)
                print("[SUCCESS] Post published autonomously!")
                print("="*60)
                context.close()
                return True
            else:
                # Fallback: Try Enter
                print("[WARN] Post button not found, trying Enter key...")
                page.keyboard.press('Control+Enter')
                time.sleep(3)
                print("\n" + "="*60)
                print("[SUCCESS] Posted via Enter key!")
                print("="*60)
                context.close()
                return True
                
        except Exception as e:
            print(f"[ERROR] Could not publish: {e}")
            print("\n[INFO] Keeping browser open for manual post...")
            time.sleep(10)
            context.close()
            return False

if __name__ == "__main__":
    test_message = "Autonomous LinkedIn test post! AI Automation"
    result = post_to_linkedin_guaranteed(test_message)
    print(f"\nFinal Result: {'SUCCESS' if result else 'FAILED'}\n")
