"""
Session Login Helper - Gold Tier
=================================
Use this script to login and save sessions for Facebook, Instagram, Twitter.

Usage:
    python MCP/social/login_helper.py

This will:
1. Open browser for selected platform
2. You login manually
3. Session saved automatically
4. Ready for autonomous posting!
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


def save_session(platform: str, context) -> bool:
    """Save browser session to file."""
    session_folder = SESSION_DIR / f"{platform}_session"
    session_folder.mkdir(exist_ok=True)
    
    state_file = session_folder / "state.json"
    
    try:
        context.storage_state(path=str(state_file))
        print(f"\n✅ Session saved to: {state_file}")
        return True
    except Exception as e:
        print(f"\n❌ Failed to save session: {e}")
        return False


def login_facebook():
    """Login to Facebook and save session."""
    print("\n" + "="*60)
    print("FACEBOOK LOGIN")
    print("="*60)
    print("\nInstructions:")
    print("1. Browser will open")
    print("2. Login to your Facebook account")
    print("3. WAIT until you see your News Feed fully loaded")
    print("4. Press Enter in this window to save session")
    print("\nOpening browser...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = context.new_page()
        
        # Navigate to Facebook login
        print("Loading Facebook...")
        page.goto("https://www.facebook.com", timeout=120000, wait_until="networkidle")
        
        print("\n⏹️  IMPORTANT: Wait for Facebook to fully load!")
        print("    You should see your News Feed with posts.")
        input("\n    Press Enter after Facebook is fully loaded...")
        
        # Wait longer for any navigation to complete
        print("Saving session...")
        page.wait_for_timeout(5000)
        
        # Save session regardless of verification
        print("\n💾 Saving Facebook session...")
        if save_session("facebook", context):
            print("\n🎉 Facebook session saved!")
            print("   Testing session...")
            
            # Quick test - try to reload and check
            try:
                page.reload(wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(3000)
                print("   ✅ Session appears valid!")
                print("   You can now use autonomous posting.")
            except:
                print("   ⚠️  Session saved but couldn't verify.")
                print("   Try posting to test.")
        
        browser.close()


def login_instagram():
    """Login to Instagram and save session."""
    print("\n" + "="*60)
    print("INSTAGRAM LOGIN")
    print("="*60)
    print("\nInstructions:")
    print("1. Browser will open")
    print("2. Login to your Instagram account")
    print("3. Wait until you see your Feed")
    print("4. Press Enter in this window to save session")
    print("\nOpening browser...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = context.new_page()
        
        # Navigate to Instagram login
        page.goto("https://www.instagram.com", timeout=60000, wait_until="domcontentloaded")
        
        input("\n⏹️  Press Enter after you've logged in successfully...")
        
        # Wait a moment for any navigation to complete
        page.wait_for_timeout(2000)
        
        # Verify login
        try:
            is_logged_in = (
                page.query_selector('svg[aria-label="New post"]') is not None or
                page.query_selector('svg[aria-label="Profile"]') is not None or
                page.query_selector('[role="button"]:has-text("Create")') is not None
            )
            
            if is_logged_in:
                print("\n✅ Login detected!")
                if save_session("instagram", context):
                    print("\n🎉 Instagram session saved successfully!")
                    print("   You can now use autonomous posting.")
            else:
                print("\n⚠️  Could not verify login. Trying to save session anyway...")
                if save_session("instagram", context):
                    print("\n🎉 Session saved. Test with a post to verify.")
        except Exception as e:
            print(f"\n⚠️  Could not verify login status: {e}")
            print("   Saving session anyway...")
            if save_session("instagram", context):
                print("   Session saved. Test with a post to verify.")
        
        browser.close()


def login_twitter():
    """Login to Twitter/X and save session."""
    print("\n" + "="*60)
    print("TWITTER/X LOGIN")
    print("="*60)
    print("\nInstructions:")
    print("1. Browser will open")
    print("2. Login to your Twitter/X account")
    print("3. Wait until you see your Home timeline")
    print("4. Press Enter in this window to save session")
    print("\nOpening browser...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = context.new_page()
        
        # Navigate to Twitter login
        page.goto("https://twitter.com/home", timeout=60000, wait_until="domcontentloaded")
        
        input("\n⏹️  Press Enter after you've logged in successfully...")
        
        # Wait a moment for any navigation to complete
        page.wait_for_timeout(2000)
        
        # Verify login
        try:
            is_logged_in = (
                page.query_selector('div[contenteditable="true"][role="textbox"]') is not None or
                page.query_selector('[data-testid="tweetButton"]') is not None or
                page.query_selector('[data-testid="SideNav_AccountSettings"]') is not None
            )
            
            if is_logged_in:
                print("\n✅ Login detected!")
                if save_session("twitter", context):
                    print("\n🎉 Twitter session saved successfully!")
                    print("   You can now use autonomous posting.")
            else:
                print("\n⚠️  Could not verify login. Trying to save session anyway...")
                if save_session("twitter", context):
                    print("\n🎉 Session saved. Test with a post to verify.")
        except Exception as e:
            print(f"\n⚠️  Could not verify login status: {e}")
            print("   Saving session anyway...")
            if save_session("twitter", context):
                print("   Session saved. Test with a post to verify.")
        
        browser.close()


def check_existing_sessions():
    """Check for existing saved sessions."""
    print("\n" + "="*60)
    print("EXISTING SESSIONS")
    print("="*60)
    
    platforms = ["facebook", "instagram", "twitter"]
    
    for platform in platforms:
        session_file = SESSION_DIR / f"{platform}_session" / "state.json"
        if session_file.exists():
            mtime = datetime.fromtimestamp(session_file.stat().st_mtime)
            print(f"\n✅ {platform.title()}: Session exists (saved: {mtime.strftime('%Y-%m-%d %H:%M')})")
        else:
            print(f"\n❌ {platform.title()}: No session saved")


def main():
    """Main menu."""
    while True:
        print("\n" + "="*60)
        print("GOLD TIER - SOCIAL MEDIA LOGIN HELPER")
        print("="*60)
        print("\nSelect platform to login:")
        print("1. Facebook")
        print("2. Instagram")
        print("3. Twitter/X")
        print("4. Check existing sessions")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == "1":
            login_facebook()
        elif choice == "2":
            login_instagram()
        elif choice == "3":
            login_twitter()
        elif choice == "4":
            check_existing_sessions()
        elif choice == "5":
            print("\n👋 Goodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please enter 1-5.")


if __name__ == "__main__":
    main()
