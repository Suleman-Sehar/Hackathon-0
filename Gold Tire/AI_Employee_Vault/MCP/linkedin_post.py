# linkedin_post.py
# LinkedIn Post MCP - Post content to LinkedIn using browser automation
from playwright.sync_api import sync_playwright
import time
import random
import json
from pathlib import Path
from datetime import datetime

# Session folder (will be created automatically)
SESSION_DIR = Path("linkedin_session")
SESSION_DIR.mkdir(exist_ok=True)

def human_delay(min_sec=1.5, max_sec=4.0):
    """Random delay to simulate human-like behavior."""
    time.sleep(random.uniform(min_sec, max_sec))

def random_mouse_move(page):
    """Simple human-like mouse movement."""
    viewport = page.viewport_size
    if viewport:
        x = random.randint(100, viewport['width'] - 100)
        y = random.randint(100, viewport['height'] - 100)
        page.mouse.move(x, y)
        human_delay(0.3, 0.8)

def post_to_linkedin(message: str, headless=False):
    """
    Post a message to LinkedIn.

    Args:
        message: The text content to post
        headless: Run browser in headless mode (False recommended for first login)

    Returns:
        bool: True if post was successful
    """
    with sync_playwright() as p:
        # Persistent context = reuse cookies/storage
        print("[INFO] Launching browser...")
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(SESSION_DIR),
            headless=headless,
            viewport={'width': 1280, 'height': 800},
            slow_mo=100,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-web-security',
                '--features=NetworkService'
            ],
            ignore_default_args=['--enable-automation']
        )

        page = context.new_page()

        # Go to LinkedIn homepage first (more reliable than feed)
        print("[INFO] Opening LinkedIn...")
        try:
            page.goto("https://www.linkedin.com/", timeout=60000)
            human_delay(3, 6)
            
            # Navigate to feed if on homepage
            try:
                page.goto("https://www.linkedin.com/feed/", timeout=30000)
                human_delay(2, 4)
            except:
                print("[WARN] Feed navigation timeout, continuing...")
        except Exception as e:
            print(f"[ERROR] Failed to open LinkedIn: {e}")
            context.close()
            return False

        # Check if logged in - look for multiple possible indicators
        logged_in = False
        
        # Try different selectors for the start post button
        selectors = [
            "button[aria-label='Start a post']",
            "div[aria-label='Start a post']",
            "button:has-text('Start a post')",
            "[data-control-name='create_post']"
        ]
        
        for selector in selectors:
            try:
                if page.is_visible(selector, timeout=5000):
                    print(f"[OK] Logged in - found post button: {selector}")
                    logged_in = True
                    break
            except:
                continue
        
        if not logged_in:
            print("[INFO] Login required - please login manually now...")
            print("[INFO] After login, close browser manually to save session.")
            input("Press Enter after manual login and session is saved...")
            context.close()
            return False

        # Click the Start a post button
        post_button_clicked = False
        for selector in selectors:
            try:
                page.click(selector, timeout=10000)
                print(f"[OK] Clicked post button: {selector}")
                post_button_clicked = True
                human_delay(2, 5)
                break
            except:
                continue
        
        if not post_button_clicked:
            print("[ERROR] Could not find post button")
            context.close()
            return False

        # Wait for the post composer to appear
        # Try different selectors for the text input
        textbox_selectors = [
            "div[role='textbox']",
            "div[contenteditable='true']",
            "p[placeholder='What do you want to talk about?']"
        ]
        
        textbox_found = False
        for selector in textbox_selectors:
            try:
                page.wait_for_selector(selector, timeout=10000)
                textbox = page.locator(selector).first
                textbox.click()
                human_delay(1, 3)
                print(f"[OK] Found textbox: {selector}")
                textbox_found = True
                break
            except:
                continue
        
        if not textbox_found:
            print("[ERROR] Could not find post textbox")
            context.close()
            return False

        # Type message using fill (faster and more reliable)
        print("[INFO] Typing post content...")
        try:
            textbox.fill(message)
            human_delay(1, 2)
            print(f"[OK] Content filled ({len(message)} chars)")
        except Exception as e:
            print(f"[WARN] Fill failed, trying type: {e}")
            # Fallback: type character by character
            for char in message[:100]:  # Limit to 100 chars for fallback
                try:
                    textbox.type(char, delay=random.uniform(30, 80))
                except:
                    break
            human_delay(2, 4)

        random_mouse_move(page)

        # Click Post button - try multiple selectors
        post_button_selectors = [
            "button:has-text('Post')",
            "span:has-text('Post')",
            "button[aria-label='Post']",
            "button[type='submit']",
            "div[role='button']:has-text('Post')"
        ]
        
        post_published = False
        for selector in post_button_selectors:
            try:
                page.click(selector, timeout=5000)
                print(f"[OK] Clicked Post button: {selector}")
                human_delay(3, 7)
                post_published = True
                break
            except:
                continue
        
        # Try pressing Enter as fallback
        if not post_published:
            try:
                page.keyboard.press("Enter")
                print("[OK] Pressed Enter to post")
                human_delay(3, 7)
                post_published = True
            except:
                pass
        
        if post_published:
            print(f"[OK] Posted successfully: '{message[:50]}...'")
            # Log to dashboard
            log_linkedin_post(message)
        else:
            print("[WARNING] Post may not have been published")

        context.close()
        return post_published

def log_linkedin_post(message: str):
    """Log LinkedIn post to Dashboard.md"""
    dashboard_path = Path("Bronze Tire/AI_Employee_Vault/Dashboard.md")
    if not dashboard_path.exists():
        return
    
    content = dashboard_path.read_text()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    lines = content.split('\n')
    new_lines = []
    in_section = False
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        if '## LinkedIn Posts Today' in line:
            in_section = True
        elif in_section and line.startswith('| Content'):
            new_lines.append(f"| {message[:40]} | Published | {timestamp} |")
            in_section = False
    
    try:
        dashboard_path.write_text('\n'.join(new_lines))
        print(f"[LOG] LinkedIn post logged to Dashboard")
    except:
        pass

def process_approved_linkedin():
    """Process all approved LinkedIn posts."""
    approved_dir = Path("Approved/LinkedIn")
    
    if not approved_dir.exists():
        approved_dir = Path("Approved")
    
    if not approved_dir.exists():
        print("[INFO] No Approved folder")
        return 0
    
    files = list(approved_dir.glob("*linkedin*.md")) + list(approved_dir.glob("*LINKEDIN*.md"))
    
    if not files:
        print("[INFO] No approved LinkedIn posts to publish")
        return 0
    
    sent_count = 0
    done_dir = Path("Done")
    done_dir.mkdir(exist_ok=True)
    
    for file in files:
        content = file.read_text()
        
        # Extract post content
        post_content = None
        
        # Look for content after --- or after specific markers
        if '---' in content:
            parts = content.split('---', 1)
            post_content = parts[1].strip()
        else:
            # Try to extract from # LinkedIn Post section
            lines = content.split('\n')
            in_post = False
            post_lines = []
            for line in lines:
                if line.startswith('# LinkedIn Post'):
                    in_post = True
                    continue
                if in_post:
                    post_lines.append(line)
            if post_lines:
                post_content = '\n'.join(post_lines).strip()
        
        if not post_content:
            print(f"[SKIP] No content found in {file.name}")
            continue
        
        print(f"Publishing LinkedIn post: {post_content[:50]}...")
        
        if post_to_linkedin(post_content, headless=False):
            target = done_dir / f"SENT_{file.name}"
            if target.exists():
                target.unlink()
            file.replace(target)
            sent_count += 1
    
    return sent_count

# Example usage
if __name__ == "__main__":
    post_message = """
    Excited to share: Building autonomous AI employees with local-first tools! 
    #AI #Automation #Hackathon2026
    """
    post_to_linkedin(post_message, headless=False)  # First time: False, after login: True
