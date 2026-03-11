"""
Social MCP - Facebook/Instagram/Twitter Posting
Version: 0.3 Gold Tier - Phase 2
Owner: Suleman AI Employee v0.3

Accepts JSON input and posts to social media platforms using Playwright
with persistent session storage and human-like behavior.

Usage:
    echo '{"action": "post_facebook", "message": "Hello!", "media_path": null}' | python MCP/social/social_mcp.py
"""

import json
import sys
import os
import asyncio
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# Try to import playwright
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

# Configuration
ROOT_DIR = Path(__file__).parent.parent.parent
LOGS_DIR = ROOT_DIR / "Logs"
SESSION_DIR = ROOT_DIR

# Ensure directories exist
LOGS_DIR.mkdir(exist_ok=True)

# Human-like delay ranges (milliseconds)
DELAY_PAGE_LOAD = (2000, 5000)
DELAY_TYPING = (50, 150)
DELAY_BEFORE_CLICK = (1000, 3000)
DELAY_AFTER_POST = (3000, 8000)
DELAY_MOUSE_MOVE = (200, 800)


def get_audit_log_path() -> Path:
    """Get today's audit log file path."""
    today = datetime.now().strftime("%Y-%m-%d")
    return LOGS_DIR / f"audit_{today}.json"


def log_action(action: str, status: str, details: Optional[Dict] = None, error: Optional[str] = None):
    """Log every action to audit JSON file."""
    log_path = get_audit_log_path()
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "status": status,
        "details": details or {},
        "error": error
    }
    
    # Load existing logs
    logs = []
    if log_path.exists():
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except (json.JSONDecodeError, IOError):
            logs = []
    
    logs.append(entry)
    
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)


def human_delay(min_ms: int, max_ms: int):
    """Add human-like delay with random variation."""
    delay = random.uniform(min_ms, max_ms) / 1000
    time.sleep(delay)


def random_mouse_move(page):
    """Simulate random mouse movement for human-like behavior."""
    try:
        # Move mouse to random position
        x = random.randint(100, 800)
        y = random.randint(100, 600)
        page.mouse.move(x, y)
        human_delay(*DELAY_MOUSE_MOVE)
    except:
        pass


def type_slowly(page, selector: str, text: str):
    """Type text character by character with human-like delays."""
    try:
        # Click to focus
        page.click(selector)
        human_delay(*DELAY_BEFORE_CLICK)
        
        # Type in chunks
        chunk_size = random.randint(3, 8)
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i + chunk_size]
            page.keyboard.type(chunk, delay=random.randint(*DELAY_TYPING))
            human_delay(100, 300)  # Small pause between chunks
            
            # Random mouse movement while typing
            if random.random() > 0.7:
                random_mouse_move(page)
                
    except Exception as e:
        log_action("type_slowly", "error", {"error": str(e)})
        raise


def check_logged_in(page, platform: str) -> bool:
    """Check if user is logged in to the platform."""
    try:
        if platform == "facebook":
            # Look for create post box or profile menu
            return page.query_selector('[data-testid="create-post"]') is not None
        elif platform == "instagram":
            # Look for new post button or profile
            return page.query_selector('svg[aria-label="New post"]') is not None
        elif platform == "twitter":
            # Look for tweet box
            return page.query_selector('div[contenteditable="true"][role="textbox"]') is not None
        return False
    except:
        return False


def post_facebook(page, message: str, media_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Post to Facebook using persistent session.
    
    Args:
        page: Playwright page object
        message: Post content
        media_path: Optional path to image/video
    
    Returns:
        Dict with status and result
    """
    log_action("post_facebook", "info", {"status": "starting", "message_length": len(message)})
    
    try:
        # Navigate to Facebook
        page.goto("https://www.facebook.com", timeout=60000)
        human_delay(*DELAY_PAGE_LOAD)
        
        # Random mouse movement
        random_mouse_move(page)
        
        # Check if logged in
        if not check_logged_in(page, "facebook"):
            log_action("post_facebook", "warning", {"status": "not_logged_in"})
            print("\n[WARNING] Manual login required for Facebook")
            print("Please login to Facebook in the browser window...")
            input("Press Enter after you've logged in...")
            human_delay(2000, 3000)
        
        # Find and click create post box
        post_box = page.query_selector('[data-testid="create-post"]')
        if post_box:
            post_box.click()
            human_delay(*DELAY_BEFORE_CLICK)
        
        # Find textarea and type message
        # Facebook uses contenteditable divs
        textarea = page.query_selector('div[contenteditable="true"][role="textbox"]')
        if textarea:
            textarea.click()
            human_delay(*DELAY_BEFORE_CLICK)
            
            # Clear any existing text first
            page.keyboard.press("Control+A")
            human_delay(200, 500)
            page.keyboard.press("Delete")
            human_delay(200, 500)
            
            # Type message
            type_slowly(page, 'div[contenteditable="true"][role="textbox"]', message)
            human_delay(*DELAY_BEFORE_CLICK)
            
            # Handle media upload if provided
            if media_path and os.path.exists(media_path):
                log_action("post_facebook", "info", {"uploading_media": media_path})
                # Find and click photo/video button
                photo_btn = page.query_selector('input[type="file"]')
                if photo_btn:
                    photo_btn.set_input_files(media_path)
                    human_delay(3000, 5000)
            
            # Click Post button
            post_button = page.query_selector('[aria-label="Post"], button:has-text("Post")')
            if post_button:
                post_button.click()
                human_delay(*DELAY_AFTER_POST)
                
                log_action("post_facebook", "success", {"platform": "facebook"})
                return {
                    "status": "success",
                    "platform": "facebook",
                    "url": "https://facebook.com/posts/..."
                }
        
        log_action("post_facebook", "error", {"error": "Post elements not found"})
        return {"status": "error", "error": "Could not find post elements"}
        
    except Exception as e:
        log_action("post_facebook", "error", {"error": str(e)})
        raise


def post_instagram(page, message: str, media_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Post to Instagram using persistent session.
    Note: Instagram requires media for posts.
    
    Args:
        page: Playwright page object
        message: Post caption
        media_path: Path to image (required)
    
    Returns:
        Dict with status and result
    """
    log_action("post_instagram", "info", {"status": "starting", "has_media": media_path is not None})
    
    try:
        # Navigate to Instagram
        page.goto("https://www.instagram.com", timeout=60000)
        human_delay(*DELAY_PAGE_LOAD)
        
        random_mouse_move(page)
        
        # Check if logged in
        if not check_logged_in(page, "instagram"):
            log_action("post_instagram", "warning", {"status": "not_logged_in"})
            print("\n[WARNING] Manual login required for Instagram")
            print("Please login to Instagram in the browser window...")
            input("Press Enter after you've logged in...")
            human_delay(2000, 3000)
        
        # Instagram requires media - skip if not provided
        if not media_path or not os.path.exists(media_path):
            log_action("post_instagram", "error", {"error": "Media required for Instagram"})
            return {"status": "error", "error": "Instagram requires media upload"}
        
        # Click new post button
        new_post_btn = page.query_selector('svg[aria-label="New post"], div[role="button"]:has-text("New")')
        if new_post_btn:
            new_post_btn.click()
            human_delay(*DELAY_BEFORE_CLICK)
        
        # Upload media
        file_input = page.query_selector('input[type="file"]')
        if file_input:
            file_input.set_input_files(media_path)
            human_delay(3000, 5000)
            
            # Click Next
            next_btn = page.query_selector('button:has-text("Next")')
            if next_btn:
                next_btn.click()
                human_delay(2000, 4000)
                
                # Add caption if provided
                if message:
                    caption_area = page.query_selector('textarea[aria-label="Write a caption..."]')
                    if caption_area:
                        caption_area.click()
                        human_delay(*DELAY_BEFORE_CLICK)
                        type_slowly(page, 'textarea[aria-label="Write a caption..."]', message)
                        human_delay(*DELAY_BEFORE_CLICK)
                
                # Click Share
                share_btn = page.query_selector('button:has-text("Share")')
                if share_btn:
                    share_btn.click()
                    human_delay(*DELAY_AFTER_POST)
                    
                    log_action("post_instagram", "success", {"platform": "instagram"})
                    return {
                        "status": "success",
                        "platform": "instagram",
                        "url": "https://instagram.com/p/..."
                    }
        
        log_action("post_instagram", "error", {"error": "Post flow failed"})
        return {"status": "error", "error": "Instagram post flow failed"}
        
    except Exception as e:
        log_action("post_instagram", "error", {"error": str(e)})
        raise


def post_twitter(page, message: str, media_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Post to Twitter (X) using persistent session.
    
    Args:
        page: Playwright page object
        message: Tweet content (max 280 chars for free accounts)
        media_path: Optional path to image/video
    
    Returns:
        Dict with status and result
    """
    log_action("post_twitter", "info", {"status": "starting", "message_length": len(message)})
    
    try:
        # Check message length
        if len(message) > 280:
            log_action("post_twitter", "warning", {"error": "Message too long"})
            message = message[:277] + "..."
        
        # Navigate to Twitter
        page.goto("https://twitter.com/home", timeout=60000)
        human_delay(*DELAY_PAGE_LOAD)
        
        random_mouse_move(page)
        
        # Check if logged in
        if not check_logged_in(page, "twitter"):
            log_action("post_twitter", "warning", {"status": "not_logged_in"})
            print("\n[WARNING] Manual login required for Twitter")
            print("Please login to Twitter in the browser window...")
            input("Press Enter after you've logged in...")
            human_delay(2000, 3000)
        
        # Find tweet box
        tweet_box = page.query_selector('div[contenteditable="true"][role="textbox"]')
        if tweet_box:
            tweet_box.click()
            human_delay(*DELAY_BEFORE_CLICK)
            
            # Clear existing text
            page.keyboard.press("Control+A")
            human_delay(200, 500)
            page.keyboard.press("Delete")
            human_delay(200, 500)
            
            # Type tweet
            type_slowly(page, 'div[contenteditable="true"][role="textbox"]', message)
            human_delay(*DELAY_BEFORE_CLICK)
            
            # Handle media upload if provided
            if media_path and os.path.exists(media_path):
                log_action("post_twitter", "info", {"uploading_media": media_path})
                # Click media button then upload
                media_btn = page.query_selector('input[type="file"]')
                if media_btn:
                    media_btn.set_input_files(media_path)
                    human_delay(2000, 4000)
            
            # Click Tweet/Post button
            tweet_button = page.query_selector('button[data-testid="tweetButton"], button:has-text("Post")')
            if tweet_button:
                tweet_button.click()
                human_delay(*DELAY_AFTER_POST)
                
                log_action("post_twitter", "success", {"platform": "twitter"})
                return {
                    "status": "success",
                    "platform": "twitter",
                    "url": "https://twitter.com/status/..."
                }
        
        log_action("post_twitter", "error", {"error": "Tweet box not found"})
        return {"status": "error", "error": "Could not find tweet box"}
        
    except Exception as e:
        log_action("post_twitter", "error", {"error": str(e)})
        raise


def execute_social_action(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main execution function for social media actions.
    
    Args:
        input_data: JSON with action, message, media_path
    
    Returns:
        Dict with status and results
    """
    if not PLAYWRIGHT_AVAILABLE:
        return {"status": "error", "error": "Playwright not installed. Run: pip install playwright"}
    
    action = input_data.get("action", "")
    message = input_data.get("message", "")
    media_path = input_data.get("media_path")
    
    if not message:
        return {"status": "error", "error": "Message is required"}
    
    # Map action to platform and function
    platform_map = {
        "post_facebook": ("facebook", post_facebook),
        "post_instagram": ("instagram", post_instagram),
        "post_twitter": ("twitter", post_twitter),
        "post_x": ("twitter", post_twitter)
    }
    
    if action not in platform_map:
        return {"status": "error", "error": f"Unknown action: {action}"}
    
    platform, post_func = platform_map[action]
    
    try:
        with sync_playwright() as p:
            # Launch browser with persistent context for session persistence
            session_folder = SESSION_DIR / f"{platform}_session"
            session_folder.mkdir(exist_ok=True)
            
            # Use persistent context to maintain login sessions
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(session_folder),
                headless=False,
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                locale="en-US",
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-dev-shm-usage'
                ],
                ignore_default_args=['--enable-automation']
            )

            page = context.new_page()
            
            # Execute post
            result = post_func(page, message, media_path)
            
            # Session is automatically persisted with persistent context
            # No need to manually save storage_state
            
            context.close()
            
            return result
            
    except Exception as e:
        log_action(action, "error", {"error": str(e)})
        return {"status": "error", "error": str(e)}


def main():
    """Entry point - reads JSON from stdin and executes action."""
    try:
        input_text = sys.stdin.read()
        
        if not input_text.strip():
            result = {"status": "error", "error": "No input provided"}
            print(json.dumps(result, indent=2, ensure_ascii=False).encode('utf-8').decode())
            return
        
        input_data = json.loads(input_text)
        result = execute_social_action(input_data)
        print(json.dumps(result, indent=2, ensure_ascii=False).encode('utf-8').decode())
        
    except json.JSONDecodeError as e:
        error_result = {"status": "error", "error": f"Invalid JSON input: {str(e)}"}
        log_action("social_mcp", "error", error_result)
        print(json.dumps(error_result, indent=2, ensure_ascii=False).encode('utf-8').decode())
    except Exception as e:
        error_result = {"status": "error", "error": str(e)}
        log_action("social_mcp", "error", error_result)
        print(json.dumps(error_result, indent=2, ensure_ascii=False).encode('utf-8').decode())


if __name__ == "__main__":
    main()
