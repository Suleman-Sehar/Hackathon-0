"""
AI Employee Orchestrator - Silver Tier
Coordinates watchers, MCP tools, and scheduled tasks.
"""
import sys
import time
import schedule
from pathlib import Path
from datetime import datetime

# Add Silver Tire to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import MCP tools
from mcp.email_mcp import process_approved_emails, send_daily_briefing
from mcp.linkedin_post import process_approved_linkedin
from mcp.whatsapp_mcp import process_approved_whatsapp

class Orchestrator:
    def __init__(self):
        self.running = True
        self.check_interval = 30  # seconds

        # Ensure required directories exist
        self._ensure_directories()

    def _ensure_directories(self):
        """Create required directories if they don't exist."""
        # Use parent directory for Approved/Pending_Approval folders (root level)
        parent = Path("..")
        dirs = [
            "../Approved/Email",
            "../Approved/LinkedIn", 
            "../Approved/WhatsApp",
            "../Pending_Approval",
            "Done"
        ]
        for d in dirs:
            Path(d).mkdir(parents=True, exist_ok=True)
        
        # Also create local dirs for sessions
        Path("whatsapp_session").mkdir(exist_ok=True)
        Path("linkedin_session").mkdir(exist_ok=True)

    def check_approved_emails(self):
        """Check and process approved email requests."""
        # Look in parent directory (root level)
        approved_dir = Path("../Approved/Email")
        if approved_dir.exists():
            files = list(approved_dir.glob("*.md"))
            if files:
                print(f"[ORCHESTRATOR] Found {len(files)} approved email(s)")
                process_approved_emails()

    def check_approved_linkedin(self):
        """Check and process approved LinkedIn posts."""
        # Look in parent directory (root level)
        approved_dir = Path("../Approved/LinkedIn")
        if approved_dir.exists():
            files = list(approved_dir.glob("*.md"))
            if files:
                print(f"[ORCHESTRATOR] Found {len(files)} approved LinkedIn post(s)")
                process_approved_linkedin()

    def check_approved_whatsapp(self):
        """Check and process approved WhatsApp messages."""
        # Look in parent directory (root level)
        approved_dir = Path("../Approved/WhatsApp")
        if not approved_dir.exists():
            approved_dir = Path("../Approved")

        if approved_dir.exists():
            files = list(approved_dir.glob("*whatsapp*.md")) + list(approved_dir.glob("*WHATSAPP*.md"))
            if files:
                print(f"[ORCHESTRATOR] Found {len(files)} approved WhatsApp message(s)")
                process_approved_whatsapp()

    def check_pending_approvals(self):
        """Monitor pending approvals and notify if urgent."""
        # Look in parent directory (root level)
        pending_dir = Path("../Pending_Approval")
        if pending_dir.exists():
            files = list(pending_dir.glob("*.md"))
            if files:
                print(f"[ORCHESTRATOR] {len(files)} approval(s) awaiting review")

    def run_daily_briefing(self):
        """Send daily briefing at scheduled time."""
        print("[ORCHESTRATOR] Running daily briefing...")
        send_daily_briefing()

    def setup_schedule(self):
        """Configure scheduled tasks."""
        # Daily briefing at 8 AM
        schedule.every().day.at("08:00").do(self.run_daily_briefing)
        print("[ORCHESTRATOR] Schedule configured: Daily briefing at 8 AM")

    def run(self):
        """Main orchestrator loop."""
        print("=" * 50)
        print("AI Employee Orchestrator v0.2 Silver")
        print("=" * 50)
        print("[OK] Starting orchestrator...")
        print("[OK] Email MCP: Available")
        print("[OK] LinkedIn MCP: Available (auto-posting enabled)")
        print("[OK] WhatsApp MCP: Available (auto-send enabled)")

        self.setup_schedule()

        while self.running:
            try:
                # Run scheduled tasks
                schedule.run_pending()

                # Check for approved actions
                self.check_approved_emails()
                self.check_approved_linkedin()
                self.check_approved_whatsapp()
                self.check_pending_approvals()

                # Wait before next check
                time.sleep(self.check_interval)

            except KeyboardInterrupt:
                print("\n[ORCHESTRATOR] Stopping...")
                self.running = False
            except Exception as e:
                print(f"[ERROR] Orchestrator error: {e}")
                time.sleep(self.check_interval)

def main():
    orchestrator = Orchestrator()
    orchestrator.run()

if __name__ == "__main__":
    main()
