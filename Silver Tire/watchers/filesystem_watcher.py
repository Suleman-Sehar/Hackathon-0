#!/usr/bin/env python3
"""
Filesystem Watcher - Monitors a directory for new files and processes them.

This is a general-purpose filesystem watcher that monitors a directory for new files
and can perform custom actions on them.
"""

import os
import sys
import time
import logging
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# Configuration
WATCH_DIR = os.environ.get('WATCH_DIR', 'Bronze Tire/AI_Employee_Vault/Inbox')
OUTPUT_DIR = os.environ.get('OUTPUT_DIR', 'Bronze Tire/AI_Employee_Vault/Needs_Action')
LOG_DIR = os.environ.get('LOG_DIR', 'Bronze Tire/AI_Employee_Vault/Logs')
WATCH_INTERVAL = int(os.environ.get('WATCH_INTERVAL', '5'))
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')


class FileHandler(FileSystemEventHandler):
    """Handler for filesystem events."""
    
    def __init__(self, logger, output_dir):
        super().__init__()
        self.logger = logger
        self.output_dir = Path(output_dir)
        self.processed_files = set()
    
    def on_created(self, event):
        """Called when a file or directory is created."""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # Skip if already processed
        if file_path in self.processed_files:
            return
        
        # Wait a bit for file to be fully written
        time.sleep(0.5)
        
        self.logger.info(f"New file detected: {file_path.name}")
        self.process_file(file_path)
    
    def process_file(self, file_path):
        """Process a new file."""
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Generate new filename with timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d')
            new_filename = f"{timestamp}_{file_path.name}"
            dest_path = self.output_dir / new_filename
            
            # Ensure output directory exists
            self.output_dir.mkdir(parents=True, exist_ok=True)
            
            # Move file to output directory
            file_path.rename(dest_path)
            
            self.logger.info(f"Processed: {file_path.name} -> {new_filename}")
            self.processed_files.add(file_path)
            
        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {e}")


def setup_logging(log_dir):
    """Setup logging configuration."""
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / f"watcher_{datetime.now().strftime('%Y-%m-%d')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)


def scan_existing_files(watch_dir, output_dir, logger):
    """Scan for existing files in watch directory and process them."""
    watch_path = Path(watch_dir)
    output_path = Path(output_dir)
    
    if not watch_path.exists():
        logger.warning(f"Watch directory does not exist: {watch_dir}")
        return 0

    existing_files = list(watch_path.glob('*'))
    logger.info(f"Found {len(existing_files)} existing files in {watch_dir}")

    # Process each existing file
    processed_count = 0
    for file_path in existing_files:
        if file_path.is_file():
            try:
                # Generate new filename with timestamp
                timestamp = datetime.now().strftime('%Y-%m-%d')
                new_filename = f"{timestamp}_{file_path.name}"
                dest_path = output_path / new_filename

                # Ensure output directory exists
                output_path.mkdir(parents=True, exist_ok=True)

                # Move file to output directory
                file_path.rename(dest_path)
                logger.info(f"Processed existing file: {file_path.name} -> {new_filename}")
                processed_count += 1

            except Exception as e:
                logger.error(f"Error processing existing file {file_path}: {e}")

    return processed_count


def main():
    """Main entry point."""
    logger = setup_logging(LOG_DIR)
    
    logger.info("=" * 60)
    logger.info("Filesystem Watcher Started")
    logger.info(f"Watch Directory: {WATCH_DIR}")
    logger.info(f"Output Directory: {OUTPUT_DIR}")
    logger.info(f"Log Directory: {LOG_DIR}")
    logger.info(f"Check Interval: {WATCH_INTERVAL}s")
    logger.info("=" * 60)
    
    # Ensure directories exist
    Path(WATCH_DIR).mkdir(parents=True, exist_ok=True)
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    # Scan and process existing files
    existing_count = scan_existing_files(WATCH_DIR, OUTPUT_DIR, logger)
    if existing_count > 0:
        logger.info(f"Processed {existing_count} existing file(s) on startup")
    
    # Setup watchdog observer
    event_handler = FileHandler(logger, OUTPUT_DIR)
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=False)
    observer.start()
    
    logger.info(f"Watching for changes in: {WATCH_DIR}")
    
    try:
        while True:
            time.sleep(WATCH_INTERVAL)
    except KeyboardInterrupt:
        logger.info("Stopping watcher...")
        observer.stop()
    
    observer.join()
    logger.info("Watcher stopped.")


if __name__ == '__main__':
    main()
