"""
FIX ALL SESSIONS - Universal Login Script
==========================================
This will fix authentication for ALL platforms:
- LinkedIn
- WhatsApp
- Facebook
- Instagram
- Twitter/X

Usage:
    python fix_all_sessions.py
"""

import sys
import time
from pathlib import Path
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("❌ Playwright not installed!")
    print("   Install with: pip install playwright && playwright install chromium")
    sys.exit(1)

# Configuration
ROOT_DIR = Path(__file__).parent

# All platforms with their info
PLATFORMS = {
    'linkedin': {
        'name': 'LinkedIn',
        'url': 'https://www.linkedin.com/feed/',
        'verify_selectors': [
            "button[aria-label='Start a post']",
            "div[aria-label='Start a post']",
            "button:has-text('Start a post')",
            "[data-control-name='create_post']",
            # Fallback: if we see these, user is logged in
            "nav[aria-label='Main navigation']",
            "div[class*='feed-shared-update-v2']",
        ],
        'folder': ROOT_DIR / 'linkedin_session'
    },
    'whatsapp': {
        'name': 'WhatsApp',
        'url': 'https://web.whatsapp.com',
        'verify_selector': 'div[contenteditable="true"][data-tab="3"]',
        'folder': ROOT_DIR / 'whatsapp_session'
    },
    'facebook': {
        'name': 'Facebook',
        'url': 'https://www.facebook.com',
        'verify_selector': '[data-testid="create-post"]',
        'folder': ROOT_DIR / 'facebook_session'
    },
    'instagram': {
        'name': 'Instagram',
        'url': 'https://www.instagram.com',
        'verify_selector': 'svg[aria-label="New post"]',
        'folder': ROOT_DIR / 'instagram_session'
    },
    'twitter': {
        'name': 'Twitter/X',
        'url': 'https://twitter.com/home',
        'verify_selector': 'div[contenteditable="true"][role="textbox"]',
        'folder': ROOT_DIR / 'twitter_session'
    }
}


def fix_session(platform: str):
    """Fix session for a specific platform using Chrome profile format."""
    if platform not in PLATFORMS:
        print(f"❌ Unknown platform: {platform}")
        print(f"   Available: {', '.join(PLATFORMS.keys())}")
        return False

    info = PLATFORMS[platform]
    session_folder = info['folder']
    
    # Create session folder
    session_folder.mkdir(exist_ok=True, parents=True)
    
    print(f"\n{'='*70}")
    print(f"FIXING {info['name'].upper()} SESSION")
    print(f"{'='*70}")
    print(f"\n📁 Session folder: {session_folder}")
    print(f"\nInstructions:")
    print(f"1. Browser will open with {info['name']}")
    print(f"2. Login to your {info['name']} account")
    print(f"3. WAIT until you see your feed/home page")
    print(f"4. DO NOT close the browser - it will close automatically")
    print(f"5. Session will be saved automatically to Chrome profile")
    print(f"\n✅ After successful login, the browser will close and session is saved!")
    
    input("\nPress Enter to continue...")
    
    try:
        with sync_playwright() as p:
            # Launch with PERSISTENT context - this is the key!
            # Session auto-saves to user_data_dir folder
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(session_folder),
                headless=False,  # MUST be False for visual login
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                locale="en-US",
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-web-security',
                    '--features=NetworkService'
                ],
                ignore_default_args=['--enable-automation'],
                slow_mo=100  # Slower actions for debugging
            )
            
            page = context.pages[0] if context.pages else context.new_page()
            
            # Navigate to platform
            print(f"\n🌐 Loading {info['name']}...")
            try:
                page.goto(info['url'], timeout=120000, wait_until="networkidle")
                print(f"✅ {info['name']} loaded")
            except Exception as e:
                print(f"⚠️  Navigation error (continuing anyway): {e}")
            
            print(f"\n{'='*70}")
            print(f"PLEASE LOGIN NOW")
            print(f"{'='*70}")
            print(f"\n👉 Login to {info['name']} in the browser window...")
            print(f"👉 Complete any 2FA verification if required")
            print(f"👉 Wait until you see your feed/home page")
            print(f"\n⏳ Waiting for manual login...")
            
            # Wait for user to login (max 5 minutes)
            login_timeout = 300  # seconds
            start_time = time.time()
            
            logged_in = False
            check_interval = 3  # Check every 3 seconds
            
            while time.time() - start_time < login_timeout:
                time.sleep(check_interval)
                
                # Check if logged in - try all selectors for this platform
                try:
                    # Handle platforms with multiple selectors (like LinkedIn)
                    if isinstance(info.get('verify_selectors'), list):
                        for selector in info['verify_selectors']:
                            try:
                                if page.query_selector(selector):
                                    print(f"\n✅ LOGIN DETECTED for {info['name']}! (found: {selector})")
                                    logged_in = True
                                    break
                            except:
                                continue
                        if logged_in:
                            break
                    else:
                        # Single selector (original behavior)
                        if page.query_selector(info['verify_selector']):
                            print(f"\n✅ LOGIN DETECTED for {info['name']}!")
                            logged_in = True
                            break
                except:
                    pass
                
                # Progress indicator
                elapsed = int(time.time() - start_time)
                if elapsed % 30 == 0 and elapsed > 0:
                    print(f"⏳ Still waiting... ({elapsed}/{login_timeout}s)")
            
            # Close browser - session auto-saved to user_data_dir
            print(f"\n💾 Saving session to Chrome profile...")
            context.close()
            
            if logged_in:
                print(f"\n{'='*70}")
                print(f"✅ {info['name'].upper()} SESSION FIXED!")
                print(f"{'='*70}")
                print(f"📁 Session saved to: {session_folder}")
                print(f"✅ You can now use autonomous {info['name']} posting!")
                print(f"\n📝 Session format: Chrome Profile (most reliable)")
                return True
            else:
                print(f"\n{'='*70}")
                print(f"⚠️  {info['name'].upper()} LOGIN TIMEOUT")
                print(f"{'='*70}")
                print(f"❌ Login not detected within {login_timeout} seconds")
                print(f"\nTry again:")
                print(f"  python fix_all_sessions.py {platform}")
                return False
                
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print(f"\nTroubleshooting:")
        print(f"1. Close any open Chrome browsers")
        print(f"2. Make sure no other script is using the session folder")
        print(f"3. Try again")
        return False


def check_all_sessions():
    """Check status of all sessions."""
    print(f"\n{'='*70}")
    print(f"SESSION STATUS CHECK - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*70}\n")
    
    if not PLAYWRIGHT_AVAILABLE:
        print("[WARN] Playwright not installed!")
        return
    
    all_ok = True
    
    for platform, info in PLATFORMS.items():
        folder = info['folder']
        
        # Check if folder exists and has data
        if not folder.exists():
            status = "[FAIL] Not configured"
            all_ok = False
        elif list(folder.glob("*")):
            # Folder has data - assume valid for now
            status = "[OK]   Has session data"
        else:
            status = "[FAIL] Empty folder"
            all_ok = False
        
        print(f"{status}  {info['name']:12} ({folder.name})")
    
    print(f"\n{'='*70}")
    
    if all_ok:
        print("[OK] All platforms have session data!")
    else:
        print("[WARN] Some platforms need attention")
        print("\nTo fix a specific platform:")
        print("  python fix_all_sessions.py <platform>")
        print("\nPlatforms: linkedin, whatsapp, facebook, instagram, twitter")
    
    print(f"{'='*70}")


def main_menu():
    """Show main menu."""
    while True:
        print(f"\n{'='*70}")
        print("FIX ALL SESSIONS - Universal Login")
        print(f"{'='*70}")
        print("\nSelect an option:")
        print("1. Check all session status")
        print("2. Fix LinkedIn session")
        print("3. Fix WhatsApp session")
        print("4. Fix Facebook session")
        print("5. Fix Instagram session")
        print("6. Fix Twitter/X session")
        print("7. Fix ALL sessions (one by one)")
        print("0. Exit")
        
        choice = input("\nEnter choice (0-7): ").strip()
        
        if choice == '1':
            check_all_sessions()
        elif choice == '2':
            fix_session('linkedin')
        elif choice == '3':
            fix_session('whatsapp')
        elif choice == '4':
            fix_session('facebook')
        elif choice == '5':
            fix_session('instagram')
        elif choice == '6':
            fix_session('twitter')
        elif choice == '7':
            print("\nFixing ALL sessions one by one...")
            for platform in PLATFORMS.keys():
                fix_session(platform)
                input("\nPress Enter to continue to next platform...")
        elif choice == '0':
            print("\n👋 Goodbye!")
            break
        else:
            print("\n❌ Invalid choice. Enter 0-7.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command line argument provided
        platform = sys.argv[1].lower()
        if platform in PLATFORMS:
            fix_session(platform)
        else:
            print(f"❌ Unknown platform: {platform}")
            print(f"   Available: {', '.join(PLATFORMS.keys())}")
    else:
        # Interactive menu
        main_menu()
