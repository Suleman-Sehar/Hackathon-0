"""
MCP: Social Media Poster
Handles Facebook, Instagram, Twitter (X) posting via Playwright with persistent sessions.
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright
import asyncio

# Configuration
MAX_RETRIES = 3
LOGS_DIR = Path(__file__).parent.parent.parent / "Logs"
SESSION_DIR = Path(__file__).parent.parent.parent

def get_audit_log_path():
    """Get today's audit log path."""
    today = datetime.now().strftime("%Y-%m-%d")
    return LOGS_DIR / f"audit_{today}.json"

def log_action(action, status, details=None, error=None):
    """Log every action to audit file."""
    LOGS_DIR.mkdir(exist_ok=True)
    log_path = get_audit_log_path()
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "status": status,
        "details": details or {},
        "error": str(error) if error else None
    }
    
    # Load existing logs or create new
    logs = []
    if log_path.exists():
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except:
            logs = []
    
    logs.append(entry)
    
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)

async def post_facebook(page, content, image_path=None):
    """Post to Facebook."""
    try:
        await page.goto("https://www.facebook.com", timeout=30000)
        await page.wait_for_load_state("networkidle")
        
        # Find the post creation box
        post_box = await page.query_selector('[data-testid="create-post"]')
        if post_box:
            await post_box.click()
            await page.wait_for_timeout(2000)
            
            # Type content
            textarea = await page.query_selector('div[contenteditable="true"]')
            if textarea:
                await textarea.fill(content)
                await page.wait_for_timeout(1000)
                
                # Upload image if provided
                if image_path and os.path.exists(image_path):
                    file_input = await page.query_selector('input[type="file"]')
                    if file_input:
                        await file_input.set_input_files(image_path)
                        await page.wait_for_timeout(2000)
                
                # Click post button
                post_button = await page.query_selector('[aria-label="Post"]')
                if post_button:
                    await post_button.click()
                    return {"success": True, "platform": "facebook"}
        
        return {"success": False, "platform": "facebook", "error": "Post box not found"}
    except Exception as e:
        return {"success": False, "platform": "facebook", "error": str(e)}

async def post_instagram(page, content, image_path=None):
    """Post to Instagram."""
    try:
        await page.goto("https://www.instagram.com", timeout=30000)
        await page.wait_for_load_state("networkidle")
        
        # Click new post button
        new_post = await page.query_selector('svg[aria-label="New post"]')
        if new_post:
            await new_post.click()
            await page.wait_for_timeout(2000)
            
            # Upload image
            if image_path and os.path.exists(image_path):
                file_input = await page.query_selector('input[type="file"]')
                if file_input:
                    await file_input.set_input_files(image_path)
                    await page.wait_for_timeout(3000)
                    
                    # Click next
                    next_btn = await page.query_selector('button:has-text("Next")')
                    if next_btn:
                        await next_btn.click()
                        await page.wait_for_timeout(2000)
                        
                        # Add caption
                        textarea = await page.query_selector('textarea[aria-label="Write a caption..."]')
                        if textarea and content:
                            await textarea.fill(content)
                            await page.wait_for_timeout(1000)
                        
                        # Share
                        share_btn = await page.query_selector('button:has-text("Share")')
                        if share_btn:
                            await share_btn.click()
                            return {"success": True, "platform": "instagram"}
        
        return {"success": False, "platform": "instagram", "error": "Post flow not found"}
    except Exception as e:
        return {"success": False, "platform": "instagram", "error": str(e)}

async def post_twitter(page, content, image_path=None):
    """Post to Twitter (X)."""
    try:
        await page.goto("https://twitter.com/home", timeout=30000)
        await page.wait_for_load_state("networkidle")
        
        # Find tweet box
        tweet_box = await page.query_selector('div[contenteditable="true"][role="textbox"]')
        if tweet_box:
            await tweet_box.fill(content)
            await page.wait_for_timeout(1000)
            
            # Upload image if provided
            if image_path and os.path.exists(image_path):
                file_input = await page.query_selector('input[type="file"]')
                if file_input:
                    await file_input.set_input_files(image_path)
                    await page.wait_for_timeout(2000)
            
            # Click tweet button
            tweet_button = await page.query_selector('button[data-testid="tweetButton"]')
            if tweet_button:
                await tweet_button.click()
                return {"success": True, "platform": "twitter"}
        
        return {"success": False, "platform": "twitter", "error": "Tweet box not found"}
    except Exception as e:
        return {"success": False, "platform": "twitter", "error": str(e)}

async def post_to_multiple_platforms(platforms, content, image_path):
    """
    Post to multiple platforms with graceful degradation.
    If one platform fails, continue with others.
    """
    results = {}
    
    for platform in platforms:
        try:
            log_action("multi_platform_post", "info", {
                "platform": platform,
                "status": "starting"
            })
            
            # Each platform gets its own browser context for isolation
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False)
                context = await browser.new_context(
                    viewport={"width": 1280, "height": 720},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                )
                
                # Load existing session if available
                session_file = SESSION_DIR / f"{platform}_session" / "state.json"
                if session_file.exists():
                    try:
                        await context.storage_state(path=session_file)
                    except:
                        pass
                
                page = await context.new_page()
                
                # Try with retries
                success = False
                for attempt in range(MAX_RETRIES):
                    try:
                        if platform == "facebook":
                            result = await post_facebook(page, content, image_path)
                        elif platform == "instagram":
                            result = await post_instagram(page, content, image_path)
                        elif platform in ["twitter", "x"]:
                            result = await post_twitter(page, content, image_path)
                        else:
                            result = {"success": False, "error": f"Unknown platform: {platform}"}
                        
                        if result.get("success"):
                            # Save session state
                            await context.storage_state(path=session_file)
                            success = True
                            results[platform] = {"status": "success", "result": result}
                            log_action("multi_platform_post", "success", {"platform": platform})
                            break
                        else:
                            log_action("multi_platform_attempt", "warning", {
                                "platform": platform,
                                "attempt": attempt + 1,
                                "error": result.get("error")
                            })
                    except Exception as e:
                        log_action("multi_platform_attempt", "warning", {
                            "platform": platform,
                            "attempt": attempt + 1,
                            "error": str(e)
                        })
                    
                    if attempt < MAX_RETRIES - 1:
                        # Exponential backoff
                        await asyncio.sleep(RETRY_DELAY * (2 ** attempt))
                
                if not success:
                    results[platform] = {"status": "failed", "error": "All retries exhausted"}
                    log_action("multi_platform_post", "failed", {"platform": platform})
                
                await browser.close()
                
        except Exception as e:
            results[platform] = {"status": "failed", "error": str(e)}
            log_action("multi_platform_post", "error", {
                "platform": platform,
                "error": str(e)
            })
    
    return results

async def execute_social_post(input_data):
    """Main execution function for social media posting."""
    platforms = input_data.get("platforms", [])
    platform = input_data.get("platform", "").lower()
    content = input_data.get("content", "")
    image_path = input_data.get("image_path")
    domain = input_data.get("domain", "Personal")
    
    # Support single platform or multiple platforms
    if not platforms and platform:
        platforms = [platform]
    
    log_action("social_post_start", "info", {
        "platforms": platforms,
        "domain": domain,
        "content_length": len(content)
    })

    if not content:
        log_action("social_post", "failed", {"error": "No content provided"})
        return {"status": "failed", "error": "Content is required"}

    if not platforms:
        log_action("social_post", "failed", {"error": "No platform specified"})
        return {"status": "failed", "error": "No platform specified"}

    # Multi-platform posting with graceful degradation
    if len(platforms) > 1:
        results = await post_to_multiple_platforms(platforms, content, image_path)
        
        # Count successes and failures
        successes = [p for p, r in results.items() if r.get("status") == "success"]
        failures = [p for p, r in results.items() if r.get("status") != "success"]
        
        log_action("multi_platform_complete", "info", {
            "successes": successes,
            "failures": failures,
            "total": len(platforms)
        })
        
        # Return success if at least one platform succeeded (graceful degradation)
        if successes:
            return {
                "status": "partial_success" if failures else "success",
                "results": results,
                "successful_platforms": successes,
                "failed_platforms": failures
            }
        else:
            return {"status": "failed", "results": results, "error": "All platforms failed"}
    
    # Single platform posting
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )

        # Load existing session if available
        session_file = SESSION_DIR / f"{platform}_session" / "state.json"
        if session_file.exists():
            try:
                await context.storage_state(path=session_file)
            except:
                pass

        page = await context.new_page()

        for attempt in range(MAX_RETRIES):
            try:
                if platform == "facebook":
                    result = await post_facebook(page, content, image_path)
                elif platform == "instagram":
                    result = await post_instagram(page, content, image_path)
                elif platform in ["twitter", "x"]:
                    result = await post_twitter(page, content, image_path)
                else:
                    result = {"success": False, "error": f"Unknown platform: {platform}"}

                results.append(result)

                if result.get("success"):
                    # Save session state
                    await context.storage_state(path=session_file)
                    log_action("social_post", "success", result)
                    await browser.close()
                    return {"status": "success", "result": result}

            except Exception as e:
                log_action("social_post_attempt", "retry", {
                    "attempt": attempt + 1,
                    "error": str(e)
                })
                if attempt == MAX_RETRIES - 1:
                    log_action("social_post", "failed", {"error": str(e), "max_retries": MAX_RETRIES})

        await browser.close()

    return {"status": "failed", "results": results, "error": "All retries exhausted"}

def main():
    """Entry point - accepts JSON from stdin."""
    try:
        input_json = sys.stdin.read()
        input_data = json.loads(input_json)
        
        result = asyncio.run(execute_social_post(input_data))
        print(json.dumps(result))
        
    except json.JSONDecodeError as e:
        error = {"status": "failed", "error": f"Invalid JSON input: {str(e)}"}
        log_action("social_post", "failed", error)
        print(json.dumps(error))
    except Exception as e:
        error = {"status": "failed", "error": str(e)}
        log_action("social_post", "failed", error)
        print(json.dumps(error))

if __name__ == "__main__":
    main()
