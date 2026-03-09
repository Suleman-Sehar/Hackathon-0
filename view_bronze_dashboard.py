#!/usr/bin/env python3
"""
Bronze Tire Dashboard Viewer
=============================
Displays the Bronze Tier Dashboard in a formatted view.

Usage:
    python view_bronze_dashboard.py
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')  # Set UTF-8 code page
    sys.stdout.reconfigure(encoding='utf-8')

# Configuration
BRONZE_ROOT = Path(__file__).parent / "Bronze Tire"
VAULT_DIR = BRONZE_ROOT / "AI_Employee_Vault"
DASHBOARD_FILE = VAULT_DIR / "Dashboard.md"

# Use ASCII-safe emojis
EMOJI_BRONZE = "[BRONZE]"
EMOJI_FOLDER = "[DIR]"
EMOJI_CLOCK = "[TIME]"
EMOJI_CHECK = "[OK]"
EMOJI_CROSS = "[FAIL]"
EMOJI_SCRIPT = "[PY]"
EMOJI_CHART = "[STATS]"
EMOJI_WATCH = "[WATCH]"
EMOJI_GREEN = "[ACTIVE]"

def read_dashboard():
    """Read and display the Bronze Tire Dashboard."""
    if not DASHBOARD_FILE.exists():
        print(f"{EMOJI_CROSS} Dashboard not found at: {DASHBOARD_FILE}")
        print(f"\nCreating new dashboard...")
        
        # Create basic dashboard
        DASHBOARD_FILE.parent.mkdir(parents=True, exist_ok=True)
        DASHBOARD_FILE.write_text("""# AI Employee Dashboard

**Last Updated:** {}
**AI Employee:** Suleman AI Employee v0.1 Bronze
**Project:** Hackathon 0 - Bronze Tier

## Quick Stats
- Pending Tasks: 0
- Files Tracked: 0
- Active Plans: 0

## Today's Priorities
- [ ] Review inbox items
- [ ] Process any pending tasks

## System Status
- Inbox Monitor: Ready
- Metadata Manager: Ready
- File Mover: Ready

**AI Employee Status:** [ACTIVE] Running

---

*Bronze Tier - Basic Task Tracking*
""".format(datetime.now().strftime("%Y-%m-%d %H:%M")))
        
        print(f"{EMOJI_CHECK} Created new dashboard")
    
    # Read and display dashboard
    content = DASHBOARD_FILE.read_text(encoding="utf-8")
    
    print("\n" + "="*70)
    print(f"{EMOJI_BRONZE} BRONZE TIRE DASHBOARD")
    print("="*70)
    print(f"{EMOJI_FOLDER} Location: {DASHBOARD_FILE}")
    print(f"{EMOJI_CLOCK} Last Modified: {datetime.fromtimestamp(DASHBOARD_FILE.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    print()
    print(content)
    print()
    print("="*70)


def show_bronze_status():
    """Show Bronze Tier status summary."""
    print("\n" + "="*70)
    print(f"{EMOJI_BRONZE} BRONZE TIER STATUS")
    print("="*70)
    
    # Check directories
    dirs = {
        "Inbox": VAULT_DIR / "Inbox",
        "Needs_Action": VAULT_DIR / "Needs_Action",
        "Plans": VAULT_DIR / "Plans",
        "Done": VAULT_DIR / "Done",
        "Logs": VAULT_DIR / "Logs"
    }
    
    print(f"\n{EMOJI_FOLDER} Directory Status:")
    for name, path in dirs.items():
        if path.exists():
            count = len(list(path.iterdir()))
            print(f"  {EMOJI_CHECK} {name:20} - {count} items")
        else:
            print(f"  {EMOJI_CROSS} {name:20} - Not found")
    
    # Check scripts
    print(f"\n{EMOJI_SCRIPT} Available Scripts:")
    scripts_dir = VAULT_DIR / "scripts"
    if scripts_dir.exists():
        scripts = list(scripts_dir.glob("*.py"))
        for script in scripts:
            print(f"  {EMOJI_CHECK} {script.name}")
    else:
        print(f"  {EMOJI_CROSS} Scripts folder not found")
    
    # Check metadata
    print(f"\n{EMOJI_CHART} Metadata:")
    metadata_file = VAULT_DIR / "metadata_index.json"
    if metadata_file.exists():
        print(f"  {EMOJI_CHECK} metadata_index.json exists")
    else:
        print(f"  {EMOJI_CROSS} metadata_index.json not found")
    
    print("\n" + "="*70)


def watch_dashboard():
    """Watch dashboard for changes."""
    import time
    
    print("\n👁️  Watching dashboard for changes... (Ctrl+C to stop)")
    print(f"📁 Monitoring: {DASHBOARD_FILE}")
    
    last_modified = DASHBOARD_FILE.stat().st_mtime if DASHBOARD_FILE.exists() else 0
    
    try:
        while True:
            time.sleep(2)
            
            if DASHBOARD_FILE.exists():
                current_modified = DASHBOARD_FILE.stat().st_mtime
                if current_modified != last_modified:
                    print(f"\n📝 Dashboard updated at {datetime.now().strftime('%H:%M:%S')}")
                    last_modified = current_modified
    except KeyboardInterrupt:
        print("\n\n👋 Stopping watcher...")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Bronze Tire Dashboard Viewer")
    parser.add_argument("--status", action="store_true", help="Show Bronze Tier status")
    parser.add_argument("--watch", action="store_true", help="Watch dashboard for changes")
    parser.add_argument("--refresh", action="store_true", help="Refresh and display dashboard")
    
    args = parser.parse_args()
    
    if args.status:
        show_bronze_status()
    elif args.watch:
        if DASHBOARD_FILE.exists():
            watch_dashboard()
        else:
            print("❌ Dashboard not found. Run without --watch first.")
    elif args.refresh:
        read_dashboard()
    else:
        # Default: show both dashboard and status
        read_dashboard()
        show_bronze_status()


if __name__ == "__main__":
    main()
