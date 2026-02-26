#!/usr/bin/env python3
"""
Inbox Monitor - Watches Inbox folder and auto-processes incoming files.

Moves files from Inbox/ → Needs_Action/ based on classification rules.
Logs all actions to Logs/activity/ and Logs/runs/.

Version: 1.0
"""

import os
import shutil
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

# Configuration
VAULT_ROOT = Path(__file__).parent.parent
INBOX_DIR = VAULT_ROOT / "Inbox"
NEEDS_ACTION_DIR = VAULT_ROOT / "Needs_Action"
LOGS_ACTIVITY_DIR = VAULT_ROOT / "Logs" / "activity"
LOGS_RUNS_DIR = VAULT_ROOT / "Logs" / "runs"

# Watch interval in seconds
WATCH_INTERVAL = 5

# Priority keywords (P1 = urgent, P2 = high, P3 = normal, P4 = low)
PRIORITY_KEYWORDS = {
    "P1": ["urgent", "emergency", "critical", "asap", "production", "down", "blocked"],
    "P2": ["high", "important", "deadline", "priority", "soon"],
    "P3": ["normal", "standard", "regular"],
    "P4": ["low", "nice-to-have", "future", "someday"],
}

# Auto-categorization patterns
CATEGORY_PATTERNS = {
    "contract": ["contract", "agreement", "nda", "sow", "proposal"],
    "bug": ["bug", "error", "issue", "defect", "fix"],
    "meeting": ["meeting", "standup", "sync", "call", "notes"],
    "report": ["report", "summary", "metrics", "dashboard", "analytics"],
    "invoice": ["invoice", "receipt", "payment", "bill"],
    "feature": ["feature", "enhancement", "request", "improvement"],
}

# Setup logging
def setup_logging() -> Tuple[logging.Logger, logging.FileHandler]:
    """Configure logging to both file and console."""
    LOGS_RUNS_DIR.mkdir(parents=True, exist_ok=True)
    
    log_file = LOGS_RUNS_DIR / f"run_inbox-monitor_{datetime.now().strftime('%Y-%m-%d')}.log"
    
    logger = logging.getLogger("inbox_monitor")
    logger.setLevel(logging.INFO)
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger, file_handler


def ensure_directories():
    """Create required directories if they don't exist."""
    for directory in [INBOX_DIR, NEEDS_ACTION_DIR, LOGS_ACTIVITY_DIR, LOGS_RUNS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)


def detect_priority(filename: str) -> str:
    """Detect priority level from filename content."""
    filename_lower = filename.lower()
    
    # Check for explicit priority tags
    if "_p1_" in filename_lower or "[p1]" in filename_lower:
        return "P1"
    elif "_p2_" in filename_lower or "[p2]" in filename_lower:
        return "P2"
    elif "_p3_" in filename_lower or "[p3]" in filename_lower:
        return "P3"
    elif "_p4_" in filename_lower or "[p4]" in filename_lower:
        return "P4"
    
    # Keyword-based detection
    for priority, keywords in PRIORITY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in filename_lower:
                return priority
    
    return "P3"  # Default priority


def detect_category(filename: str) -> str:
    """Detect category from filename content."""
    filename_lower = filename.lower()
    
    for category, keywords in CATEGORY_PATTERNS.items():
        for keyword in keywords:
            if keyword in filename_lower:
                return category
    
    return "general"


def extract_assignee(filename: str) -> str:
    """Extract assignee name from filename if present."""
    # Look for pattern like _name_ or [name]
    parts = filename.lower().replace("[", "_").replace("]", "_").split("_")
    
    # Common assignee patterns
    for part in parts:
        if part and part not in ["p1", "p2", "p3", "p4", "auto", "manual", "urgent"]:
            # Check if it looks like a name (alphabetic, 2-20 chars)
            if part.isalpha() and 2 <= len(part) <= 20:
                return part
    
    return "unassigned"


def generate_new_filename(original: str) -> str:
    """Generate standardized filename for Needs_Action folder."""
    timestamp = datetime.now().strftime("%Y-%m-%d")
    priority = detect_priority(original)
    assignee = extract_assignee(original)
    
    # Remove extension
    name_parts = original.rsplit(".", 1)
    base_name = name_parts[0] if len(name_parts) > 1 else original
    extension = f".{name_parts[1]}" if len(name_parts) > 1 else ""
    
    # Clean base name
    clean_base = base_name.replace("[", "").replace("]", "").replace(" ", "-")
    
    return f"{timestamp}_{priority}_{assignee}_{clean_base}{extension}"


def log_activity(action: str, source: str, destination: str, details: str = ""):
    """Log activity to the activity log file."""
    activity_file = LOGS_ACTIVITY_DIR / f"activity_{datetime.now().strftime('%Y-%m-%d')}.log"
    
    with open(activity_file, "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp} | {action} | {source} → {destination} | {details}\n")


def process_file(file_path: Path, logger: logging.Logger) -> bool:
    """Process a single file from Inbox."""
    if file_path.suffix.lower() in [".tmp", ".part", ".download"]:
        logger.info(f"⏳ Skipping incomplete file: {file_path.name}")
        return False
    
    try:
        # Generate new filename
        new_filename = generate_new_filename(file_path.name)
        destination = NEEDS_ACTION_DIR / new_filename
        
        # Handle duplicate filenames
        counter = 1
        while destination.exists():
            name_parts = new_filename.rsplit(".", 1)
            if len(name_parts) > 1:
                new_filename = f"{name_parts[0]}_{counter}.{name_parts[1]}"
            else:
                new_filename = f"{name_parts[0]}_{counter}"
            destination = NEEDS_ACTION_DIR / new_filename
            counter += 1
        
        # Move file
        shutil.move(str(file_path), str(destination))
        
        # Log success
        priority = detect_priority(file_path.name)
        category = detect_category(file_path.name)
        
        logger.info(f"✅ Moved: {file_path.name} → {new_filename}")
        log_activity(
            "MOVE",
            str(file_path.name),
            str(new_filename),
            f"priority={priority}, category={category}"
        )
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error processing {file_path.name}: {e}")
        log_activity("ERROR", str(file_path.name), "FAILED", str(e))
        return False


def scan_and_process(logger: logging.Logger) -> int:
    """Scan Inbox and process all files. Returns count of processed files."""
    processed = 0
    
    if not INBOX_DIR.exists():
        return 0
    
    for file_path in INBOX_DIR.iterdir():
        if file_path.is_file():
            if process_file(file_path, logger):
                processed += 1
    
    return processed


def main():
    """Main entry point for the inbox monitor."""
    logger, file_handler = setup_logging()
    ensure_directories()
    
    logger.info("=" * 60)
    logger.info("🚀 Inbox Monitor Started")
    logger.info(f"📁 Watching: {INBOX_DIR}")
    logger.info(f"📤 Moving to: {NEEDS_ACTION_DIR}")
    logger.info(f"⏱️  Check interval: {WATCH_INTERVAL}s")
    logger.info("=" * 60)
    
    try:
        while True:
            processed = scan_and_process(logger)
            
            if processed > 0:
                logger.info(f"📊 Processed {processed} file(s)")
            
            time.sleep(WATCH_INTERVAL)
            
    except KeyboardInterrupt:
        logger.info("\n👋 Shutting down...")
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
        raise
    finally:
        # Cleanup
        logger.removeHandler(file_handler)
        file_handler.close()


if __name__ == "__main__":
    main()
