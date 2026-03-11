"""
Simple Session Login Helper - Gold Tier
========================================
Use this to login and save sessions for Facebook, Instagram, Twitter.

Usage:
    python MCP/social/login_simple.py facebook
    python MCP/social/login_simple.py instagram
    python MCP/social/login_simple.py twitter
"""

import json
import sys
from pathlib import Path
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Playwright not installed. Run: pip install playwright && playwright install chromium")
    sys.exit(1)

# Configuration
ROOT_DIR = Path(__file__).parent.parent.parent
SESSION_DIR = ROOT_DIR


def login_and_save(platform: str, url: str, verify_selector: str):
    """Generic login and save function."""
    print(f"\n{'='*60}")
    print(f"{platform.upper()} LOGIN")
    print(f"{'='*60}")
    print(f"\n1. Browser will open")
    print(f"2. Login to your {platform} account")
    print(f"3. WAIT until you see your feed/home page")
    print(f"4. Press Enter to save session")
    print(f"\nOpening browser...")
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            page = context.new_page()
            
            # Navigate
            print(f"Loading {platform}...")
            page.goto(url, timeout=120000, wait_until="networkidle")
            
            # Wait for user to login
            input("\n⏹️  Press Enter after you've logged in...")
            
            # Wait for page to stabilize
            page.wait_for_timeout(5000)
            
            # Save session
            session_folder = SESSION_DIR / f"{platform}_session"
            session_folder.mkdir(exist_ok=True)
            state_file = session_folder / "state.json"
            
            context.storage_state(path=str(state_file))
            print(f"\n✅ Session saved to: {state_file}")
            
            # Test session
            print("Testing session...")
            try:
                page.reload(wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(3000)
                
                # Check if still logged in
                if page.query_selector(verify_selector):
                    print("✅ Session verified! You can now use autonomous posting.")
                else:
                    print("⚠️  Session saved but verification failed. Try posting to test.")
            except:
                print("⚠️  Session saved. Test with a post.")
            
            browser.close()
            print("\n🎉 Done!")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Try again or check if browser is already open.")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python MCP/social/login_simple.py facebook")
        print("  python MCP/social/login_simple.py instagram")
        print("  python MCP/social/login_simple.py twitter")
        print("\nOr just run without arguments for interactive mode.")
        
        choice = input("\nLogin to (facebook/instagram/twitter): ").strip().lower()
    else:
        choice = sys.argv[1].strip().lower()
    
    if choice == "facebook":
        login_and_save(
            "facebook",
            "https://www.facebook.com",
            '[data-testid="create-post"]'
        )
    elif choice == "instagram":
        login_and_save(
            "instagram",
            "https://www.instagram.com",
            'svg[aria-label="New post"]'
        )
    elif choice == "twitter":
        login_and_save(
            "twitter",
            "https://twitter.com/home",
            'div[contenteditable="true"][role="textbox"]'
        )
    else:
        print(f"Unknown platform: {choice}")
        print("Use: facebook, instagram, or twitter")


if __name__ == "__main__":
    main()
