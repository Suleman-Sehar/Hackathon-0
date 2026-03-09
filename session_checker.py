"""
Session Checker & Login Helper
===============================
Check and manage sessions for all social media platforms.

Usage:
    python session_checker.py              # Check all sessions
    python session_checker.py --login facebook    # Login to Facebook
    python session_checker.py --test linkedin     # Test LinkedIn session
"""

import json
import sys
import time
from pathlib import Path
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️  Playwright not installed!")
    print("   Install with: pip install playwright && playwright install chromium")

# Configuration
ROOT_DIR = Path(__file__).parent
SESSION_FOLDERS = {
    'linkedin': ROOT_DIR / 'linkedin_session',
    'whatsapp': ROOT_DIR / 'whatsapp_session',
    'facebook': ROOT_DIR / 'facebook_session',
    'instagram': ROOT_DIR / 'instagram_session',
    'twitter': ROOT_DIR / 'twitter_session'
}

# Platform URLs and verification selectors
PLATFORM_INFO = {
    'facebook': {
        'url': 'https://www.facebook.com',
        'verify_selector': '[data-testid="create-post"]',
        'name': 'Facebook'
    },
    'instagram': {
        'url': 'https://www.instagram.com',
        'verify_selector': 'svg[aria-label="New post"]',
        'name': 'Instagram'
    },
    'twitter': {
        'url': 'https://twitter.com/home',
        'verify_selector': 'div[contenteditable="true"][role="textbox"]',
        'name': 'Twitter/X'
    },
    'linkedin': {
        'url': 'https://www.linkedin.com/feed/',
        'verify_selectors': [
            "button[aria-label='Start a post']",
            "div[aria-label='Start a post']",
            "button:has-text('Start a post')",
            "[data-control-name='create_post']",
            "nav[aria-label='Main navigation']",
            "div[class*='feed-shared-update-v2']",
        ],
        'name': 'LinkedIn'
    },
    'whatsapp': {
        'url': 'https://web.whatsapp.com',
        'verify_selector': 'div[contenteditable="true"][data-tab="3"]',
        'name': 'WhatsApp'
    }
}


def check_session(platform: str) -> dict:
    """Check if a platform session exists and is valid."""
    folder = SESSION_FOLDERS.get(platform)
    if not folder:
        return {'exists': False, 'valid': False, 'error': 'Unknown platform'}

    state_file = folder / 'state.json'

    # Check for state.json format (new format)
    if state_file.exists():
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)

            # Check if session has cookies
            cookies = session_data.get('cookies', [])
            if not cookies:
                return {'exists': True, 'valid': False, 'error': 'Empty session'}

            # Check cookie expiration
            now = time.time()
            expired = [c for c in cookies if c.get('expirationDate', now + 86400) < now]
            if len(expired) == len(cookies):
                return {'exists': True, 'valid': False, 'error': 'All cookies expired'}

            return {'exists': True, 'valid': True, 'cookies': len(cookies)}

        except Exception as e:
            return {'exists': True, 'valid': False, 'error': str(e)}

    # Check for browser profile format (old format - LinkedIn/WhatsApp style)
    # Look for Default folder which contains cookies
    default_folder = folder / 'Default'
    if default_folder.exists():
        cookies_file = default_folder / 'Cookies'
        if cookies_file.exists():
            # Has browser profile with cookies - likely valid session
            return {'exists': True, 'valid': True, 'cookies': 'profile'}

    return {'exists': False, 'valid': False, 'error': 'No valid session found'}


def test_session(platform: str):
    """Test a session by loading it and checking if logged in."""
    if platform not in PLATFORM_INFO:
        print(f"❌ Unknown platform: {platform}")
        return

    info = PLATFORM_INFO[platform]
    folder = SESSION_FOLDERS.get(platform)
    state_file = folder / 'state.json' if folder else None

    print(f"\n{'='*60}")
    print(f"Testing {info['name']} Session")
    print(f"{'='*60}")

    if not state_file or not state_file.exists():
        print(f"❌ No session file found at: {state_file}")
        print(f"   Run: python session_checker.py --login {platform}")
        return

    if not PLAYWRIGHT_AVAILABLE:
        print("❌ Playwright not available")
        return

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                viewport={"width": 1280, "height": 720},
                storage_state=str(state_file)
            )
            page = context.new_page()

            print(f"Loading {info['name']}...")
            page.goto(info['url'], timeout=60000, wait_until="networkidle")
            page.wait_for_timeout(5000)

            # Check if logged in - handle multiple selectors for LinkedIn
            logged_in = False
            
            if platform == 'linkedin' and isinstance(info.get('verify_selectors'), list):
                # Try each LinkedIn selector
                for selector in info['verify_selectors']:
                    try:
                        if page.query_selector(selector):
                            print(f"✅ Session is VALID - Logged in to {info['name']} (found: {selector})")
                            logged_in = True
                            break
                    except:
                        continue
            else:
                # Single selector (original behavior)
                logged_in = page.query_selector(info['verify_selector']) is not None

            if logged_in:
                print(f"✅ Session is VALID - Logged in to {info['name']}")
            else:
                print(f"❌ Session is INVALID - Not logged in")
                print(f"   Run: python session_checker.py --login {platform}")

            browser.close()

    except Exception as e:
        print(f"❌ Error testing session: {e}")


def login_to_platform(platform: str):
    """Login to a platform and save session."""
    if platform not in PLATFORM_INFO:
        print(f"❌ Unknown platform: {platform}")
        print(f"   Available: {', '.join(PLATFORM_INFO.keys())}")
        return

    info = PLATFORM_INFO[platform]
    folder = SESSION_FOLDERS.get(platform)
    if folder:
        folder.mkdir(exist_ok=True)
    state_file = folder / 'state.json' if folder else None

    print(f"\n{'='*60}")
    print(f"{info['name']} LOGIN")
    print(f"{'='*60}")
    print(f"\n1. Browser will open")
    print(f"2. Login to your {info['name']} account")
    print(f"3. WAIT until you see your feed/home page")
    print(f"4. Press Enter to save session")
    print(f"\nOpening browser...")

    if not PLAYWRIGHT_AVAILABLE:
        print("❌ Playwright not available")
        print("   Install with: pip install playwright && playwright install chromium")
        return

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            page = context.new_page()

            # Navigate
            print(f"Loading {info['name']}...")
            page.goto(info['url'], timeout=120000, wait_until="networkidle")

            # Wait for user to login
            input("\n⏹️  Press Enter after you've logged in...")

            # Wait for page to stabilize
            page.wait_for_timeout(5000)

            # Save session
            if state_file:
                context.storage_state(path=str(state_file))
                print(f"\n✅ Session saved to: {state_file}")

                # Verify session
                print("Testing session...")
                try:
                    page.reload(wait_until="domcontentloaded", timeout=30000)
                    page.wait_for_timeout(3000)

                    # Check verification with proper selectors
                    logged_in = False
                    if platform == 'linkedin' and isinstance(info.get('verify_selectors'), list):
                        for selector in info['verify_selectors']:
                            try:
                                if page.query_selector(selector):
                                    print(f"✅ Session verified! (found: {selector})")
                                    logged_in = True
                                    break
                            except:
                                continue
                    else:
                        if page.query_selector(info['verify_selector']):
                            print("✅ Session verified! You can now use autonomous posting.")
                            logged_in = True
                    
                    if not logged_in:
                        print("⚠️  Session saved but verification failed. Try again if posting fails.")
                except:
                    print("⚠️  Session saved. Test with a post.")
            else:
                print("❌ Could not save session - folder not configured")

            browser.close()
            print("\n🎉 Done!")

    except Exception as e:
        print(f"\n❌ Error: {e}")


def print_status():
    """Print status of all sessions."""
    print(f"\n{'='*60}")
    print(f"SESSION STATUS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    print()

    if not PLAYWRIGHT_AVAILABLE:
        print("[WARN] Playwright not installed!")
        print("   Install with: pip install playwright && playwright install chromium")
        print()

    all_valid = True

    for platform, info in PLATFORM_INFO.items():
        result = check_session(platform)

        icon = "[?]"
        status = ""

        if not result['exists']:
            icon = "[FAIL]"
            status = "Not logged in"
            all_valid = False
        elif not result['valid']:
            icon = "[WARN]"
            status = f"Invalid ({result.get('error', 'unknown')})"
            all_valid = False
        else:
            icon = "[OK]"
            status = f"Active ({result.get('cookies', 0)} cookies)"

        print(f"{icon} {info['name']:12} - {status}")

    print()
    print(f"{'='*60}")

    if all_valid:
        print("[OK] All sessions are active!")
    else:
        print("[WARN] Some sessions need attention")
        print()
        print("To login to a platform:")
        print("  python session_checker.py --login facebook")
        print("  python session_checker.py --login instagram")
        print("  python session_checker.py --login twitter")
        print("  python session_checker.py --login linkedin")
        print("  python session_checker.py --login whatsapp")
        print()
        print("To test a session:")
        print("  python session_checker.py --test facebook")
        print("  python session_checker.py --test linkedin")
        print()

    print(f"{'='*60}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Session Checker & Login Helper')
    parser.add_argument('--login', type=str, help='Login to platform (facebook/instagram/twitter/linkedin/whatsapp)')
    parser.add_argument('--test', type=str, help='Test platform session')
    parser.add_argument('--status', action='store_true', help='Show all session status')

    args = parser.parse_args()

    if args.login:
        login_to_platform(args.login)
    elif args.test:
        test_session(args.test)
    else:
        print_status()


if __name__ == "__main__":
    main()
