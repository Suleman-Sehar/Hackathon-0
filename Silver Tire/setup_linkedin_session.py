"""
LinkedIn Session Setup - Login and save session
"""
from playwright.sync_api import sync_playwright
import time
from pathlib import Path

SESSION_DIR = Path("linkedin_session")
SESSION_DIR.mkdir(exist_ok=True)

print("="*60)
print("  LINKEDIN SESSION SETUP")
print("="*60)
print()
print("Browser will open in 3 seconds...")
time.sleep(3)

with sync_playwright() as p:
    # Launch browser with persistent context
    print("[INFO] Launching browser...")
    context = p.chromium.launch_persistent_context(
        user_data_dir=str(SESSION_DIR),
        headless=False,
        viewport={'width': 1280, 'height': 800},
        slow_mo=100,
        args=[
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox',
            '--disable-dev-shm-usage'
        ]
    )
    
    page = context.new_page()
    
    # Go to LinkedIn
    print("[INFO] Opening LinkedIn...")
    page.goto("https://www.linkedin.com/", timeout=60000)
    time.sleep(5)
    
    print()
    print("="*60)
    print("  PLEASE LOGIN TO LINKEDIN")
    print("="*60)
    print()
    print("Steps:")
    print("1. Enter your email and password")
    print("2. Click 'Sign in'")
    print("3. Complete any verification")
    print("4. Wait for your feed to load")
    print("5. Check 'Keep me signed in' if asked")
    print()
    print("After you see your LinkedIn feed:")
    print("- Navigate to your home feed")
    print("- Wait 10 seconds for cookies to save")
    print("- Then close the browser manually")
    print()
    print("Waiting for you to login...")
    print("(Press Enter in this terminal after you've logged in and closed the browser)")
    print()
    
    # Wait for user to login
    try:
        input("Press Enter after you've logged in and the browser closed...")
    except:
        pass
    
    print()
    print("[INFO] Checking if session was saved...")
    
    # Verify session was saved
    session_files = list(SESSION_DIR.glob("*"))
    if len(session_files) > 5:
        print(f"[OK] Session saved! ({len(session_files)} files)")
        print()
        print("Next time LinkedIn will auto-login!")
    else:
        print("[WARN] Session may not be saved properly")
        print("Please try again and make sure to stay logged in for 10 seconds")
    
    print()
    print("="*60)
