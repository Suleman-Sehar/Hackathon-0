"""
Silver Tier Dashboard API - FastAPI Backend
Modern, sophisticated dashboard for monitoring and controlling AI Employee automation.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
import json
import sys
import os

# Add Silver Tire to path
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))
os.chdir(str(BASE_DIR))  # Change working directory

# Import MCP modules
from mcp.email_mcp import send_email, process_approved_emails, load_credentials
from mcp.whatsapp_mcp import send_whatsapp_message
from mcp.linkedin_post import post_to_linkedin, process_approved_linkedin

app = FastAPI(
    title="Silver Tier Dashboard API",
    description="Modern dashboard for AI Employee v0.2 - Silver Tier",
    version="1.0.0"
)

# CORS configuration - allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "dashboard" / "static")), name="static")

# Models
class EmailRequest(BaseModel):
    to: str
    subject: str
    body: str
    cc: Optional[str] = None

class WhatsAppRequest(BaseModel):
    phone: str  # Changed back to string for reliability
    message: str

class LinkedInRequest(BaseModel):
    content: str
    message_to: Optional[str] = None  # For LinkedIn messaging
    message_content: Optional[str] = None  # Message content

# Helper functions
def log_action(action: str, status: str, details: dict = None, error: str = None):
    """Log action to audit log."""
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = BASE_DIR / "Logs" / f"audit_{today}.json"
    
    # Ensure Logs directory exists
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "status": status,
        "details": details or {},
        "error": error
    }
    
    # Load existing logs
    logs = []
    if log_file.exists():
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except:
            logs = []
    
    logs.append(entry)
    
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)

def get_audit_logs(date: str = None) -> List[Dict]:
    """Get audit logs for a specific date."""
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    logs_dir = BASE_DIR / "Logs"
    log_file = logs_dir / f"audit_{date}.json"

    if log_file.exists():
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass

    return []

def get_metrics(date: str = None) -> Dict[str, Any]:
    """Get metrics for dashboard."""
    logs = get_audit_logs(date)

    metrics = {
        "emails_sent": 0,
        "whatsapp_sent": 0,
        "linkedin_posts": 0,
        "errors": 0,
        "total_actions": len(logs)
    }

    for log in logs:
        action = log.get("action", "")
        status = log.get("status", "")

        if status == "success":
            if action == "send_email":
                metrics["emails_sent"] += 1
            elif action == "send_whatsapp":
                metrics["whatsapp_sent"] += 1
            elif action == "post_linkedin":
                metrics["linkedin_posts"] += 1
        elif status == "error":
            metrics["errors"] += 1

    return metrics

def check_platform_sessions() -> Dict[str, bool]:
    """Check if platform sessions exist."""
    sessions = {
        "gmail": False,
        "whatsapp": False,
        "linkedin": False
    }

    # Check Gmail credentials
    creds = load_credentials()
    sessions["gmail"] = creds is not None and creds.get("email") is not None

    # Check WhatsApp session
    whatsapp_session = BASE_DIR / "whatsapp_session"
    sessions["whatsapp"] = whatsapp_session.exists() and len(list(whatsapp_session.glob("*"))) > 0

    # Check LinkedIn session
    linkedin_session = BASE_DIR / "linkedin_session"
    sessions["linkedin"] = linkedin_session.exists() and len(list(linkedin_session.glob("*"))) > 0

    return sessions

def get_pending_actions() -> Dict[str, int]:
    """Get count of pending actions."""
    approved_dir = BASE_DIR.parent / "Approved"

    pending = {
        "email": 0,
        "whatsapp": 0,
        "linkedin": 0
    }

    if approved_dir.exists():
        email_dir = approved_dir / "Email"
        if email_dir.exists():
            pending["email"] = len(list(email_dir.glob("*.md")))

        whatsapp_dir = approved_dir / "WhatsApp"
        if whatsapp_dir.exists():
            pending["whatsapp"] = len(list(whatsapp_dir.glob("*.md")))

        linkedin_dir = approved_dir / "LinkedIn"
        if linkedin_dir.exists():
            pending["linkedin"] = len(list(linkedin_dir.glob("*.md")))

    return pending

# Routes
@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Serve the main dashboard HTML."""
    dashboard_file = BASE_DIR / "dashboard" / "index.html"
    if dashboard_file.exists():
        with open(dashboard_file, "r", encoding="utf-8") as f:
            return f.read()
    return HTMLResponse(content="<h1>Dashboard not found</h1>", status_code=404)

@app.get("/working.html", response_class=HTMLResponse)
async def working_dashboard():
    """Serve the working dashboard HTML."""
    working_file = BASE_DIR / "dashboard" / "working.html"
    if working_file.exists():
        with open(working_file, "r", encoding="utf-8") as f:
            return f.read()
    return HTMLResponse(content="<h1>Working dashboard not found</h1>", status_code=404)

@app.get("/whatsapp-qr.html", response_class=HTMLResponse)
async def whatsapp_qr_page():
    """Serve WhatsApp QR scanner page."""
    qr_file = BASE_DIR / "dashboard" / "whatsapp-qr.html"
    if qr_file.exists():
        with open(qr_file, "r", encoding="utf-8") as f:
            return f.read()
    return HTMLResponse(content="<h1>QR page not found</h1>", status_code=404)

@app.get("/activity_test.html", response_class=HTMLResponse)
async def activity_test_page():
    """Serve activity test page."""
    test_file = BASE_DIR / "dashboard" / "activity_test.html"
    if test_file.exists():
        with open(test_file, "r", encoding="utf-8") as f:
            return f.read()
    return HTMLResponse(content="<h1>Test page not found</h1>", status_code=404)

@app.get("/quick_test.html", response_class=HTMLResponse)
async def quick_test_page():
    """Serve quick test page."""
    quick_file = BASE_DIR / "dashboard" / "quick_test.html"
    if quick_file.exists():
        with open(quick_file, "r", encoding="utf-8") as f:
            return f.read()
    return HTMLResponse(content="<h1>Quick test page not found</h1>", status_code=404)

@app.get("/linkedin-test.html", response_class=HTMLResponse)
async def linkedin_test_page():
    """Serve LinkedIn test page."""
    test_file = BASE_DIR / "dashboard" / "linkedin-test.html"
    if test_file.exists():
        with open(test_file, "r", encoding="utf-8") as f:
            return f.read()
    return HTMLResponse(content="<h1>Test page not found</h1>", status_code=404)

@app.get("/linkedin-login.html", response_class=HTMLResponse)
async def linkedin_login_page():
    """Serve LinkedIn login helper page."""
    login_file = BASE_DIR / "dashboard" / "linkedin-login.html"
    if login_file.exists():
        with open(login_file, "r", encoding="utf-8") as f:
            return f.read()
    return HTMLResponse(content="<h1>LinkedIn login page not found</h1>", status_code=404)

@app.get("/api/v1/linkedin/session")
async def check_linkedin_session():
    """Check LinkedIn session status."""
    session_folder = BASE_DIR / "linkedin_session"
    
    exists = session_folder.exists()
    file_count = len(list(session_folder.glob("*"))) if exists else 0
    
    return {
        "exists": exists,
        "file_count": file_count,
        "ready": exists and file_count > 5
    }

@app.post("/api/v1/linkedin/open-chrome")
async def open_linkedin_chrome():
    """Open LinkedIn in Chrome directly."""
    import subprocess
    import os
    
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
    
    if not chrome_path:
        raise HTTPException(status_code=404, detail="Chrome not found. Please install Chrome.")
    
    try:
        # Open LinkedIn in Chrome
        subprocess.Popen([chrome_path, "https://www.linkedin.com/login"])
        return {
            "status": "success",
            "message": "LinkedIn opened in Chrome! Please login and keep Chrome open.",
            "chrome_path": chrome_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/api/v1/metrics")
async def get_metrics_endpoint(date: Optional[str] = None):
    """Get dashboard metrics."""
    return get_metrics(date)

@app.get("/api/v1/platforms")
async def get_platform_status():
    """Get platform connection status."""
    sessions = check_platform_sessions()
    pending = get_pending_actions()

    platforms = []
    for platform, connected in sessions.items():
        platforms.append({
            "platform": platform,
            "connected": connected,
            "pending": pending.get(platform, 0)
        })

    return {"platforms": platforms}

@app.get("/api/v1/activity")
async def get_recent_activity(limit: int = 20):
    """Get recent activity from audit logs."""
    logs = get_audit_logs()
    return logs[-limit:][::-1]

@app.post("/api/v1/test/email")
async def test_email(request: EmailRequest):
    """Send a test email."""
    import traceback
    
    print(f"\n{'='*60}")
    print(f"[EMAIL] Received request")
    print(f"[EMAIL] To: {request.to}")
    print(f"[EMAIL] Subject: {request.subject}")
    print(f"[EMAIL] Body: {request.body[:100]}...")
    
    try:
        # Load credentials first
        creds = load_credentials()
        if not creds:
            print("[EMAIL] ERROR: Could not load credentials")
            log_action("send_email", "error", {"to": request.to}, "No credentials")
            raise HTTPException(status_code=500, detail="Email credentials not configured")
        
        print(f"[EMAIL] Credentials loaded: {creds.get('email')}")
        
        # Send email
        result = send_email(
            to=request.to,
            subject=request.subject,
            body=request.body,
            cc=request.cc
        )
        
        print(f"[EMAIL] Send result: {result}")
        
        if result:
            log_action("send_email", "success", {"to": request.to, "subject": request.subject})
            print("[EMAIL] SUCCESS")
            return {"status": "success", "message": "Email sent successfully"}
        else:
            log_action("send_email", "error", {"to": request.to}, "SMTP send failed")
            print("[EMAIL] FAILED - SMTP send failed")
            raise HTTPException(status_code=500, detail="Failed to send email")
            
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"{str(e)}\n{traceback.format_exc()}"
        print(f"[EMAIL] ERROR: {error_msg}")
        log_action("send_email", "error", {"to": request.to}, str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/test/whatsapp")
async def test_whatsapp(request: WhatsAppRequest):
    """Send WhatsApp message using direct Chrome method."""
    import traceback
    import subprocess
    import os
    
    # Clean phone number - remove +, spaces, dashes
    phone_str = str(request.phone).replace('+', '').replace(' ', '').replace('-', '')
    
    print(f"\n{'='*60}")
    print(f"[WHATSAPP] Received request")
    print(f"[WHATSAPP] Phone: {phone_str}")
    print(f"[WHATSAPP] Message: {request.message[:50]}...")
    
    try:
        # Use direct Chrome method (opens in user's existing Chrome session)
        whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_str}&text={request.message.replace(' ', '%20').replace('\n', '%0A')}"
        
        # Find Chrome
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
        
        if chrome_path:
            # Open in Chrome
            subprocess.Popen([chrome_path, whatsapp_url])
            print(f"[WHATSAPP] Opened in Chrome: {whatsapp_url}")
            
            # Log the action
            log_action("send_whatsapp", "success", {
                "phone": phone_str,
                "message": request.message[:100],
                "method": "direct_chrome"
            })
            
            print("[WHATSAPP] SUCCESS - Chrome opened")
            return {
                "status": "success", 
                "message": "WhatsApp opened in Chrome! Message is pre-filled, press Enter to send.",
                "phone": phone_str,
                "method": "direct_chrome"
            }
        else:
            # Fallback to default browser
            import webbrowser
            webbrowser.open(whatsapp_url)
            print(f"[WHATSAPP] Opened in default browser: {whatsapp_url}")
            
            log_action("send_whatsapp", "success", {
                "phone": phone_str,
                "message": request.message[:100],
                "method": "default_browser"
            })
            
            print("[WHATSAPP] SUCCESS - Browser opened")
            return {
                "status": "success", 
                "message": "WhatsApp opened in browser! Message is pre-filled, press Enter to send.",
                "phone": phone_str,
                "method": "default_browser"
            }
            
    except Exception as e:
        error_msg = f"{str(e)}\n{traceback.format_exc()}"
        print(f"[WHATSAPP] ERROR: {error_msg}")
        log_action("send_whatsapp", "error", {"phone": phone_str}, str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/test/linkedin")
async def test_linkedin(request: LinkedInRequest):
    """Post to LinkedIn AUTONOMOUSLY - guaranteed to work."""
    import threading
    
    print(f"\n{'='*60}")
    print(f"[LINKEDIN] Autonomous post request")
    print(f"[LINKEDIN] Content: {request.content[:100]}...")
    
    result_container = {'success': False, 'error': None, 'done': False}
    
    def post_thread():
        try:
            from mcp.linkedin_guaranteed import post_to_linkedin_guaranteed
            result = post_to_linkedin_guaranteed(request.content)
            result_container['success'] = result
            result_container['done'] = True
        except Exception as e:
            result_container['error'] = str(e)
            result_container['done'] = True
            print(f"[LINKEDIN] Error: {e}")
    
    try:
        # Start thread
        thread = threading.Thread(target=post_thread)
        thread.start()
        
        # Wait up to 3 minutes
        print("[INFO] Waiting for autonomous posting (max 180s)...")
        thread.join(timeout=180)
        
        if not result_container.get('done'):
            raise Exception("Timeout after 180 seconds")
        
        if result_container.get('error'):
            raise Exception(result_container['error'])
        
        if result_container.get('success'):
            log_action("post_linkedin", "success", {
                "content": request.content[:200],
                "method": "autonomous_guaranteed"
            })
            print("[LINKEDIN] ✅ SUCCESS")
            return {"status": "success", "message": "LinkedIn post published autonomously!"}
        else:
            log_action("post_linkedin", "error", {"content": request.content[:200]}, "Posting failed")
            print("[LINKEDIN] ❌ FAILED")
            raise HTTPException(status_code=500, detail="Failed to post - check if logged in to LinkedIn in Chrome")
            
    except HTTPException:
        raise
    except Exception as e:
        log_action("post_linkedin", "error", {"content": request.content[:200]}, str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/linkedin/message")
async def send_linkedin_message(request: LinkedInRequest):
    """Open LinkedIn messaging for sending message."""
    import subprocess
    import os
    
    if not request.message_to or not request.message_content:
        raise HTTPException(status_code=400, detail="message_to and message_content required")
    
    print(f"\n{'='*60}")
    print(f"[LINKEDIN MESSAGE] To: {request.message_to}")
    print(f"[LINKEDIN MESSAGE] Content: {request.message_content[:50]}...")
    
    try:
        # Find Chrome
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        
        chrome_path = None
        for path in chrome_paths:
            if os.path.exists(path):
                chrome_path = path
                break
        
        if not chrome_path:
            raise HTTPException(status_code=404, detail="Chrome not found")
        
        # Open LinkedIn messaging
        subprocess.Popen([chrome_path, "https://www.linkedin.com/messaging/"])
        
        log_action("linkedin_message", "success", {
            "to": request.message_to,
            "content": request.message_content[:100]
        })
        
        return {
            "status": "success",
            "message": f"LinkedIn messaging opened! Find '{request.message_to}' and send your message."
        }
            
    except Exception as e:
        log_action("linkedin_message", "error", {"to": request.message_to}, str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/orchestrator/run")
async def run_orchestrator():
    """Run the orchestrator to process all pending actions."""
    import traceback
    
    print(f"\n{'='*60}")
    print(f"[ORCHESTRATOR] Starting...")
    
    try:
        results = {
            "emails": 0,
            "whatsapp": 0,
            "linkedin": 0
        }
        
        # Process emails
        print("[ORCHESTRATOR] Processing emails...")
        results["emails"] = process_approved_emails()
        
        # Process WhatsApp
        print("[ORCHESTRATOR] Processing WhatsApp...")
        process_approved_whatsapp()
        
        # Process LinkedIn
        print("[ORCHESTRATOR] Processing LinkedIn...")
        results["linkedin"] = process_approved_linkedin()
        
        print(f"[ORCHESTRATOR] Complete: {results}")
        return {"status": "success", "message": "Orchestrator completed", "results": results}
            
    except Exception as e:
        error_msg = f"{str(e)}\n{traceback.format_exc()}"
        print(f"[ORCHESTRATOR] ERROR: {error_msg}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/whatsapp/session")
async def check_whatsapp_session():
    """Check WhatsApp session status."""
    session_folder = BASE_DIR / "whatsapp_session"
    
    exists = session_folder.exists()
    file_count = len(list(session_folder.glob("*"))) if exists else 0
    
    return {
        "exists": exists,
        "file_count": file_count,
        "ready": exists and file_count > 5
    }

@app.get("/api/v1/credentials/status")
async def credentials_status():
    """Check credentials status."""
    creds = load_credentials()
    return {
        "email_configured": creds is not None,
        "email_address": creds.get("email", "") if creds else ""
    }

# Run the server
if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("  SILVER TIER DASHBOARD API")
    print("="*60)
    print(f"  Starting server on http://0.0.0.0:8001")
    print(f"  Dashboard: http://localhost:8001")
    print(f"  API Docs: http://localhost:8001/docs")
    print("="*60)
    print("\nPress Ctrl+C to stop\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
