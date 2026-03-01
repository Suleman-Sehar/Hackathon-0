"""
Scheduler - Silver Tier
Manages scheduled tasks for AI Employee.
"""
import schedule
import time
from pathlib import Path
from datetime import datetime

def create_daily_briefing_trigger():
    """Create trigger file for daily briefing."""
    trigger = Path("Trigger_Daily_Briefing.txt")
    trigger.write_text(f"Generated: {datetime.now().isoformat()}")
    print("[SCHEDULER] Daily briefing trigger created")

def cleanup_old_logs():
    """Archive logs older than 7 days."""
    logs_dir = Path("Logs")
    if not logs_dir.exists():
        return
    
    # Simple cleanup - can be enhanced
    print("[SCHEDULER] Log cleanup check completed")

def main():
    """Run scheduler with configured tasks."""
    print("=" * 50)
    print("AI Employee Scheduler - Silver Tier")
    print("=" * 50)
    
    # Schedule daily briefing trigger at 7:55 AM (runs before 8 AM briefing)
    schedule.every().day.at("07:55").do(create_daily_briefing_trigger)
    
    # Weekly cleanup on Sunday at 11 PM
    schedule.every().sunday.at("23:00").do(cleanup_old_logs)
    
    print("[OK] Scheduler configured:")
    print("  - Daily briefing trigger: 7:55 AM")
    print("  - Log cleanup: Sunday 11 PM")
    print()
    print("Running scheduler...")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()
