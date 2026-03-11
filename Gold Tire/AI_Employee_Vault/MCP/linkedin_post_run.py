# linkedin_post_run.py
from playwright.sync_api import sync_playwright
import time
import random
from pathlib import Path

SESSION_DIR = Path("linkedin_session")
SESSION_DIR.mkdir(exist_ok=True)

def human_delay(min_sec=1.5, max_sec=4.0):
    time.sleep(random.uniform(min_sec, max_sec))

def post_to_linkedin(message: str, headless=False):
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(SESSION_DIR),
            headless=headless,
            viewport={'width': 1280, 'height': 800},
            slow_mo=150,
            args=['--disable-blink-features=AutomationControlled']
        )

        page = context.new_page()
        page.goto("https://www.linkedin.com/feed/", timeout=60000)
        human_delay(5, 8)

        # Check if logged in
        if page.is_visible("button[aria-label='Start a post']", timeout=10000):
            print("Already logged in!")
        else:
            print("Login required - please login manually in the browser...")
            print("Waiting up to 2 minutes...")
            try:
                page.wait_for_selector("button[aria-label='Start a post']", timeout=120000)
                print("Login detected!")
            except:
                print("Login timeout.")
                context.close()
                return

        # Click Start a post
        page.click("button[aria-label='Start a post']", timeout=20000)
        human_delay(3, 5)
        
        # Wait for modal and type message
        page.wait_for_selector("div[contenteditable='true']", timeout=15000)
        human_delay(1, 2)
        
        # Type message
        textbox = page.locator("div[contenteditable='true']").first
        textbox.fill(message)
        human_delay(2, 3)
        
        # Click Post button
        buttons = page.locator("button")
        for i in range(buttons.count()):
            btn = buttons.nth(i)
            if btn.is_visible() and "post" in btn.text_content().lower():
                btn.click()
                break
        
        human_delay(3, 5)
        print("Post action completed!")
        context.close()

if __name__ == "__main__":
    post_message = """Freelancers: AI agents now save 20+ hours/week on admin tasks!

From email sorting to client follow-ups, autonomous AI employees handle the busy work so you can focus on high-value projects.

The future of freelancing is here.

#AI #Productivity #FreelanceLife #Automation"""
    
    post_to_linkedin(post_message, headless=False)
