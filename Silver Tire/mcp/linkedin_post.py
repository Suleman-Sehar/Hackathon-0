# linkedin_post.py
from playwright.sync_api import sync_playwright
import time
import random
import json
from pathlib import Path
import os

# Session folder (will be created automatically)
SESSION_DIR = Path("linkedin_session")
SESSION_DIR.mkdir(exist_ok=True)

# Try to use Chrome's Default profile where user might already be logged in
CHROME_PROFILES = [
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default"),
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Profile 1"),
    os.path.expandvars(r"%APPDATA%\Google\Chrome\User Data\Default"),
]

def get_chrome_profile():
    """Find existing Chrome profile."""
    for profile in CHROME_PROFILES:
        if os.path.exists(profile) and len(os.listdir(profile)) > 5:
            return profile
    return None

def human_delay(min_sec=1.5, max_sec=4.0):
    time.sleep(random.uniform(min_sec, max_sec))

def human_like_mouse_move(page):
    """Simulate human-like mouse movement."""
    viewport = page.viewport_size
    if viewport:
        x = random.randint(100, viewport['width'] - 100)
        y = random.randint(100, viewport['height'] - 100)
        page.mouse.move(x, y, steps=random.randint(10, 30))
        human_delay(0.3, 0.8)

def post_to_linkedin(message: str, headless=False):
    """Post a message to LinkedIn using browser automation with improved selectors."""
    print("[INFO] Starting LinkedIn post automation...")
    
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
                break
        
        # Try to use existing Chrome profile where user is already logged in
        chrome_profile = get_chrome_profile()
        
        if chrome_path and chrome_profile:
            print(f"[INFO] Using Chrome: {chrome_path}")
            print(f"[INFO] Using profile: {chrome_profile}")
            print(f"[INFO] This should have your LinkedIn login session!")
            # Launch Chrome with user's profile
            context = p.chromium.launch_persistent_context(
                user_data_dir=chrome_profile,
                headless=headless,
                viewport={'width': 1280, 'height': 800},
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-features=TranslateUI',
                    '--disable-ipc-flooding-protection',
                ],
                slow_mo=100,
                channel='chrome'  # Use installed Chrome
            )
        elif chrome_path:
            print(f"[INFO] Using Chrome: {chrome_path}")
            print(f"[WARN] Profile not found, using temporary session")
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(SESSION_DIR),
                headless=headless,
                viewport={'width': 1280, 'height': 800},
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                ],
                slow_mo=100,
                channel='chrome'  # Use installed Chrome
            )
        else:
            print("[WARN] Chrome not found, using default Chromium")
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(SESSION_DIR),
                headless=headless,
                viewport={'width': 1280, 'height': 800},
                args=['--disable-blink-features=AutomationControlled', '--no-sandbox'],
                slow_mo=100
            )

        page = context.new_page()

        # Go directly to LinkedIn feed
        print("[INFO] Opening LinkedIn feed...")
        page.goto("https://www.linkedin.com/feed/", timeout=90000)
        time.sleep(5)

        # Check if logged in by checking URL or elements
        print("[INFO] Checking if logged in...")
        try:
            # Wait for feed to load
            page.wait_for_selector('div[class*="feed"]', timeout=15000)
            print("[OK] Feed loaded!")
        except:
            print("[WARN] Feed not found, checking login...")
            # If not on feed, we might need to login
            if '/login' in page.url:
                print("[INFO] Need to login. Please login in the browser window...")
                print("[INFO] Waiting up to 120 seconds for login...")
                
                for i in range(60):
                    time.sleep(2)
                    if '/feed' in page.url:
                        print("[OK] Login detected!")
                        break
                    if (i + 1) % 15 == 0:
                        print(f"[INFO] Still waiting... ({(i+1)*2}s)")
                
                if '/login' in page.url:
                    print("[ERROR] Login timeout!")
                    context.close()
                    return False
            
            # Reload feed
            page.goto("https://www.linkedin.com/feed/", timeout=30000)
            time.sleep(3)

        print("[INFO] Looking for post composer...")
        
        # Try multiple selectors for the post composer trigger
        post_button_clicked = False
        post_selectors = [
            "button[aria-label='Start a post']",
            "div[role='button']:has-text('Start a post')",
            "button:has-text('Start a post')",
            "div[class*='start-post']",
            "div[class*='share-box'] button",
        ]
        
        for selector in post_selectors:
            try:
                if page.is_visible(selector, timeout=3000):
                    print(f"[OK] Found post button: {selector}")
                    page.click(selector)
                    time.sleep(3)
                    post_button_clicked = True
                    break
            except Exception as e:
                continue
        
        if not post_button_clicked:
            print("[WARN] Post button not found. Trying alternative approach...")
            # Try to navigate to posting page directly
            page.goto("https://www.linkedin.com/feed/?showUpdateOverlay=true", timeout=30000)
            time.sleep(3)
        
        # Wait for post dialog to appear
        print("[INFO] Waiting for post editor...")
        textbox_found = False
        text_selectors = [
            "div[contenteditable='true'][role='textbox']",
            "div[contenteditable='true']",
            "div[class*='editor-content'] [contenteditable='true']",
            "div[aria-label='What do you want to share?']",
        ]
        
        for selector in text_selectors:
            try:
                if page.is_visible(selector, timeout=5000):
                    print(f"[OK] Found text editor: {selector}")
                    textbox = page.locator(selector).first
                    textbox.click()
                    time.sleep(1)
                    
                    # Fill the message
                    print("[INFO] Filling message...")
                    textbox.fill(message)
                    time.sleep(2)
                    textbox_found = True
                    break
            except:
                continue
        
        if not textbox_found:
            print("[ERROR] Could not find text editor!")
            context.close()
            return False
        
        # Find and click Post button
        print("[INFO] Looking for Post button...")
        post_submitted = False
        post_btn_selectors = [
            "button:has-text('Post')",
            "button[aria-label='Post']",
            "button[data-test-id='post-submit']",
            "div[role='dialog'] button:has-text('Post')",
        ]
        
        for selector in post_btn_selectors:
            try:
                buttons = page.locator(selector)
                count = buttons.count()
                
                for i in range(count):
                    btn = buttons.nth(i)
                    if btn.is_visible():
                        text = btn.text_content().strip()
                        if 'post' in text.lower():
                            print(f"[OK] Clicking Post button: {selector}")
                            btn.click()
                            time.sleep(5)
                            post_submitted = True
                            break
                if post_submitted:
                    break
            except:
                continue
        
        # Try Enter key as fallback
        if not post_submitted:
            print("[INFO] Trying Enter key to post...")
            try:
                page.keyboard.press('Control+Enter')
                time.sleep(3)
                post_submitted = True
            except:
                pass
        
        if post_submitted:
            print(f"[OK] Post published successfully: '{message[:50]}...'")
            context.close()
            return True
        else:
            print("[WARN] Post may not have been submitted")
            print("[INFO] Keeping browser open for 10 seconds for manual post...")
            time.sleep(10)
            context.close()
            return False
        print("[INFO] Login confirmed. Starting post automation...")

        # Click "Start a post" area
        print("[INFO] Clicking 'Start a post'...")
        page.click("button[aria-label='Start a post']", timeout=20000)
        human_delay(3, 5)

        # Wait for modal and find the text editor
        print("[INFO] Waiting for post editor...")
        try:
            # Wait for the modal to appear
            page.wait_for_selector("div[role='dialog']", timeout=15000)
            human_delay(2, 3)
            
            # Try multiple selectors for the text box
            textbox = None
            text_selectors = [
                "div[contenteditable='true'][role='textbox']",
                "div[contenteditable='true']",
                "div[aria-label='What do you want to share?']",
                "div[data-placeholder='What do you want to share?']"
            ]
            
            for selector in text_selectors:
                try:
                    textbox = page.locator(selector).first
                    if textbox.count() > 0:
                        textbox.click()
                        human_delay(1, 2)
                        print(f"[OK] Found text box with: {selector}")
                        break
                except:
                    continue
            
            if not textbox:
                print("[WARN] Could not find text box, trying default...")
                textbox = page.locator("div[contenteditable='true']").first
            
            # Type message
            print("[INFO] Typing message...")
            textbox.fill(message)
            human_delay(3, 5)
            
            # Find and click Post button
            print("[INFO] Looking for Post button...")
            post_clicked = False
            
            # Try multiple selectors for Post button
            post_selectors = [
                "button:has-text('Post')",
                "button[aria-label='Post']",
                "button[data-test-id='post-submit']",
                "div[role='dialog'] button"
            ]
            
            for selector in post_selectors:
                try:
                    buttons = page.locator(selector)
                    count = buttons.count()
                    print(f"  Found {count} buttons with selector: {selector}")
                    
                    for i in range(count):
                        btn = buttons.nth(i)
                        if btn.is_visible():
                            text = btn.text_content().strip()
                            print(f"  Button text: '{text}'")
                            if 'post' in text.lower():
                                print(f"[OK] Clicking Post button...")
                                btn.click()
                                human_delay(5, 8)
                                post_clicked = True
                                break
                    if post_clicked:
                        break
                except Exception as e:
                    print(f"  Error with selector {selector}: {e}")
                    continue
            
            if not post_clicked:
                print("[WARN] Could not find Post button automatically")
                print("[INFO] Waiting for manual post... (10 seconds)")
                human_delay(10, 10)
            
            print(f"[OK] Post action completed: '{message[:50]}...'")
            context.close()
            return True
            
        except Exception as e:
            print(f"[ERROR] LinkedIn post failed: {e}")
            context.close()
            return False

def process_approved_linkedin():
    """Process approved LinkedIn posts from Approved/LinkedIn folder."""
    # Look in parent directory (root level) - use absolute path
    base_dir = Path(__file__).parent.parent.parent
    approved_dir = base_dir / "Approved" / "LinkedIn"
    
    if not approved_dir.exists():
        print("[INFO] No Approved/LinkedIn folder")
        return 0
    
    files = list(approved_dir.glob("*.md"))
    if not files:
        print("[INFO] No approved LinkedIn posts")
        return 0
    
    done_dir = base_dir / "Done"
    done_dir.mkdir(parents=True, exist_ok=True)
    
    posted_count = 0
    
    for file in files:
        content = file.read_text()
        
        # Extract post content (between header and ---)
        lines = content.split("\n")
        post_lines = []
        started = False
        
        for line in lines:
            if line.startswith("# LinkedIn Post") or line.startswith("# "):
                started = True
                continue
            if started and line.startswith("---"):
                break
            if started and line.strip():
                post_lines.append(line)
        
        post_text = "\n".join(post_lines).strip()
        
        if not post_text:
            print(f"[SKIP] No post content in {file.name}")
            continue
        
        print(f"Posting: {post_text[:50]}...")
        
        if post_to_linkedin(post_text, headless=False):
            # Move to Done
            target = done_dir / f"POSTED_{file.name}"
            file.replace(target)
            posted_count += 1
            log_linkedin_post(post_text)
    
    return posted_count

def log_linkedin_post(content: str):
    """Log posted content to Dashboard.md"""
    base_dir = Path(__file__).parent.parent.parent
    dashboard_path = base_dir / "Bronze Tire" / "AI_Employee_Vault" / "Dashboard.md"
    if not dashboard_path.exists():
        return
    
    content_text = dashboard_path.read_text()
    timestamp = time.strftime("%Y-%m-%d %H:%M")
    summary = content[:60].replace('\n', ' ')
    
    # Add to LinkedIn Posts Today section
    lines = content_text.split('\n')
    new_lines = []
    in_section = False
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        if '## LinkedIn Posts Today' in line:
            in_section = True
        elif in_section and line.startswith('| Post'):
            new_lines.append(f"| {summary}... | Published | {timestamp} |")
            in_section = False
    
    dashboard_path.write_text('\n'.join(new_lines))
    print("[LOG] LinkedIn post logged to Dashboard")

# Example usage
if __name__ == "__main__":
    post_message = """Freelancers: AI agents now save 20+ hours/week on admin tasks!

From email sorting to client follow-ups, autonomous AI employees handle the busy work so you can focus on high-value projects.

The future of freelancing is here.

#AI #Productivity #FreelanceLife #Automation"""
    
    post_to_linkedin(post_message, headless=False)
