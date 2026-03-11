"""
Simple LinkedIn API - Just opens Chrome for posting
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import subprocess
import os
from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).parent

app = FastAPI(title="Simple LinkedIn API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LinkedInRequest(BaseModel):
    content: str
    message_to: Optional[str] = None
    message_content: Optional[str] = None

def log_action(action, status, details=None):
    """Log to audit file."""
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = BASE_DIR / "Logs" / f"audit_{today}.json"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "status": status,
        "details": details or {}
    }
    
    logs = []
    if log_file.exists():
        try:
            logs = json.load(open(log_file, "r", encoding="utf-8"))
        except:
            logs = []
    
    logs.append(entry)
    json.dump(logs, open(log_file, "w", encoding="utf-8"), indent=2)

@app.post("/api/v1/test/linkedin")
async def test_linkedin(request: LinkedInRequest):
    """Open LinkedIn in Chrome for posting."""
    print(f"\n[LINKEDIN] Request: {request.content[:50]}...")
    
    try:
        # Find Chrome
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        if not os.path.exists(chrome_path):
            chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        
        if not os.path.exists(chrome_path):
            raise HTTPException(status_code=404, detail="Chrome not found")
        
        # Open LinkedIn
        subprocess.Popen([chrome_path, "https://www.linkedin.com/feed/"])
        
        log_action("post_linkedin", "success", {
            "content": request.content[:200],
            "method": "manual_chrome"
        })
        
        print("[LINKEDIN] OK - Chrome opened")
        return {
            "status": "success",
            "message": "LinkedIn opened in Chrome! Paste your content and post.",
            "content": request.content[:100]
        }
        
    except Exception as e:
        log_action("post_linkedin", "error", {"content": request.content[:200]}, str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/linkedin/message")
async def send_message(request: LinkedInRequest):
    """Open LinkedIn messaging."""
    if not request.message_to or not request.message_content:
        raise HTTPException(status_code=400, detail="message_to and message_content required")
    
    try:
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        if not os.path.exists(chrome_path):
            chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        
        if not os.path.exists(chrome_path):
            raise HTTPException(status_code=404, detail="Chrome not found")
        
        subprocess.Popen([chrome_path, "https://www.linkedin.com/messaging/"])
        
        log_action("linkedin_message", "success", {
            "to": request.message_to,
            "content": request.message_content[:100]
        })
        
        return {
            "status": "success",
            "message": f"LinkedIn messaging opened! Find '{request.message_to}' and send message."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("  SIMPLE LINKEDIN API")
    print("="*60)
    print("\nStarting on http://localhost:8001\n")
    uvicorn.run(app, host="0.0.0.0", port=8001)
