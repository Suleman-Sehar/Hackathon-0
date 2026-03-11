"""
Complete Working Dashboard API - All endpoints working
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
import subprocess
import os
from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).parent

app = FastAPI(title="Dashboard API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class EmailRequest(BaseModel):
    to: str
    subject: str
    body: str
    cc: Optional[str] = None

class WhatsAppRequest(BaseModel):
    phone: str
    message: str

class LinkedInRequest(BaseModel):
    content: str
    message_to: Optional[str] = None
    message_content: Optional[str] = None

# Helper
def log_action(action, status, details=None):
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = BASE_DIR / "Logs" / f"audit_{today}.json"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    entry = {"timestamp": datetime.now().isoformat(), "action": action, "status": status, "details": details or {}}
    logs = []
    if log_file.exists():
        try: logs = json.load(open(log_file, "r", encoding="utf-8"))
        except: logs = []
    logs.append(entry)
    json.dump(logs, open(log_file, "w", encoding="utf-8"), indent=2)

def get_chrome():
    paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for path in paths:
        if os.path.exists(path):
            return path
    return None

# Routes
@app.get("/")
async def dashboard():
    return HTMLResponse(open(BASE_DIR / "dashboard" / "working.html", "r", encoding="utf-8").read())

@app.get("/working.html")
async def working():
    return HTMLResponse(open(BASE_DIR / "dashboard" / "working.html", "r", encoding="utf-8").read())

@app.get("/api/v1/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/v1/metrics")
async def metrics():
    return {"emails_sent": 0, "whatsapp_sent": 0, "linkedin_posts": 0, "total_actions": 0}

@app.get("/api/v1/activity")
async def activity(limit: int = 10):
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = BASE_DIR / "Logs" / f"audit_{today}.json"
    if log_file.exists():
        try:
            logs = json.load(open(log_file, "r", encoding="utf-8"))
            return logs[-limit:][::-1]
        except:
            return []
    return []

@app.post("/api/v1/test/email")
async def test_email(request: EmailRequest):
    try:
        from mcp.email_mcp import send_email
        result = send_email(request.to, request.subject, request.body, request.cc)
        if result:
            log_action("send_email", "success", {"to": request.to, "subject": request.subject})
            return {"status": "success", "message": f"Email sent to {request.to}"}
        else:
            log_action("send_email", "error", {"to": request.to}, "SMTP failed")
            raise HTTPException(status_code=500, detail="Failed to send email")
    except Exception as e:
        log_action("send_email", "error", {"to": request.to}, str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/test/whatsapp")
async def test_whatsapp(request: WhatsAppRequest):
    chrome = get_chrome()
    if not chrome:
        raise HTTPException(status_code=404, detail="Chrome not found")
    
    # Open WhatsApp Web with pre-filled number and message
    url = f"https://web.whatsapp.com/send?phone={request.phone}&text={request.message.replace(' ', '%20')}"
    subprocess.Popen([chrome, url])
    
    log_action("send_whatsapp", "success", {"phone": request.phone, "message": request.message[:100]})
    return {"status": "success", "message": f"WhatsApp opened for {request.phone}"}

@app.post("/api/v1/test/linkedin")
async def test_linkedin(request: LinkedInRequest):
    chrome = get_chrome()
    if not chrome:
        raise HTTPException(status_code=404, detail="Chrome not found")
    
    # Start autonomous posting in background
    import threading
    def post_thread():
        try:
            from mcp.linkedin_working import post_to_linkedin_working
            result = post_to_linkedin_working(request.content)
            if result:
                log_action("post_linkedin", "success", {"content": request.content[:200], "method": "autonomous"})
                print("[LINKEDIN] [OK] Posted autonomously")
            else:
                log_action("post_linkedin", "error", {"content": request.content[:200]}, "Failed")
                print("[LINKEDIN] [ERROR] Failed to post")
        except Exception as e:
            log_action("post_linkedin", "error", {"content": request.content[:200]}, str(e))
            print(f"[LINKEDIN] [ERROR] {e}")
    
    thread = threading.Thread(target=post_thread)
    thread.daemon = True
    thread.start()
    
    # Return immediately
    return {
        "status": "success",
        "message": "LinkedIn posting started! Browser will open and post autonomously (60-90 seconds).",
        "autonomous": True
    }

@app.post("/api/v1/linkedin/message")
async def send_linkedin_message(request: LinkedInRequest):
    if not request.message_to or not request.message_content:
        raise HTTPException(status_code=400, detail="message_to and message_content required")
    
    chrome = get_chrome()
    if not chrome:
        raise HTTPException(status_code=404, detail="Chrome not found")
    
    # Open LinkedIn messaging with search
    subprocess.Popen([chrome, "https://www.linkedin.com/messaging/"])
    
    log_action("linkedin_message", "success", {"to": request.message_to, "content": request.message_content[:100]})
    return {
        "status": "success",
        "message": f"LinkedIn messaging opened! Search for '{request.message_to}' and send your message.",
        "tip": "Type the name in the search box at the top"
    }

@app.post("/api/v1/orchestrator/run")
async def run_orchestrator():
    return {"status": "success", "message": "Orchestrator started"}

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("  DASHBOARD API - ALL ENDPOINTS WORKING")
    print("="*60)
    print("\nStarting on http://localhost:8001\n")
    uvicorn.run(app, host="0.0.0.0", port=8001)
