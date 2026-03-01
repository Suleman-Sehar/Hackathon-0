#!/usr/bin/env python3
"""
Metadata Manager v1.0 - Utility Script
Manages file metadata tracking across the AI Employee vault.
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime

# Vault directories
VAULT_ROOT = Path(__file__).parent
INDEX_FILE = VAULT_ROOT / "metadata_index.json"

FOLDERS_TO_SCAN = [
    "Inbox",
    "Needs_Action", 
    "Plans",
    "Done",
    "Logs"
]

class MetadataManager:
    def __init__(self):
        self.index = self._load_index()
    
    def _load_index(self):
        """Load existing index or create new one."""
        if INDEX_FILE.exists():
            with open(INDEX_FILE, 'r') as f:
                return json.load(f)
        return {
            "version": "1.0",
            "last_updated": None,
            "files": [],
            "stats": {
                "total_files": 0,
                "active_plans": 0,
                "p1_count": 0,
                "p2_count": 0,
                "p3_count": 0
            }
        }
    
    def _save_index(self):
        """Save index to file."""
        self.index["last_updated"] = datetime.now().isoformat()
        with open(INDEX_FILE, 'w') as f:
            json.dump(self.index, f, indent=2)
    
    def _extract_metadata(self, file_path: Path) -> dict:
        """Extract metadata from a file."""
        try:
            content = file_path.read_text(encoding='utf-8')
        except:
            return None
        
        # Determine file type based on folder
        file_type = "unknown"
        for folder in FOLDERS_TO_SCAN:
            if folder in str(file_path):
                file_type = folder.lower().replace('_', '')
                break
        
        # Extract priority from content
        priority = "P3"  # Default
        if re.search(r'priority:\s*P1|Priority:\s*P1|🔴|urgent', content, re.IGNORECASE):
            priority = "P1"
        elif re.search(r'priority:\s*P2|Priority:\s*P2|🟡|high', content, re.IGNORECASE):
            priority = "P2"
        
        # Extract tags from frontmatter or filename
        tags = []
        filename_tags = re.findall(r'[A-Z][a-z]+|[A-Z]{2,}', file_path.stem)
        tags.extend([t.lower() for t in filename_tags if len(t) > 2])
        
        # Look for tags in content
        tag_match = re.search(r'tags:\s*\[([^\]]+)\]', content)
        if tag_match:
            tags.extend([t.strip() for t in tag_match.group(1).split(',')])
        
        # Extract status for plans
        status = "unknown"
        if "Plans" in str(file_path):
            status = "active"
            if re.search(r'status:\s*(completed|done)', content, re.IGNORECASE):
                status = "completed"
        elif "Done" in str(file_path):
            status = "completed"
        
        # Count tasks in plans
        tasks_total = 0
        tasks_completed = 0
        if "Plans" in str(file_path):
            tasks_total = len(re.findall(r'^- \[ \]', content, re.MULTILINE)) + len(re.findall(r'^- \[x\]', content, re.MULTILINE))
            tasks_completed = len(re.findall(r'^- \[x\]', content, re.MULTILINE))
        
        return {
            "path": str(file_path.relative_to(VAULT_ROOT)),
            "type": file_type,
            "priority": priority,
            "tags": list(set(tags)),
            "created": datetime.fromtimestamp(file_path.stat().st_ctime).strftime('%Y-%m-%d'),
            "status": status,
            "tasks_total": tasks_total,
            "tasks_completed": tasks_completed
        }
    
    def scan_vault(self):
        """Scan vault and update index."""
        print("[METADATA] Scanning vault...")
        
        self.index["files"] = []
        
        for folder in FOLDERS_TO_SCAN:
            folder_path = VAULT_ROOT / folder
            if not folder_path.exists():
                continue
            
            for file_path in folder_path.rglob("*.md"):
                metadata = self._extract_metadata(file_path)
                if metadata:
                    self.index["files"].append(metadata)
                    print(f"  Indexed: {metadata['path']}")
        
        # Update stats
        self._update_stats()
        self._save_index()
        
        print(f"[METADATA] Indexed {len(self.index['files'])} files")
    
    def _update_stats(self):
        """Update statistics from indexed files."""
        files = self.index["files"]
        
        self.index["stats"] = {
            "total_files": len(files),
            "active_plans": len([f for f in files if f.get('type') == 'plans' and f.get('status') == 'active']),
            "p1_count": len([f for f in files if f.get('priority') == 'P1']),
            "p2_count": len([f for f in files if f.get('priority') == 'P2']),
            "p3_count": len([f for f in files if f.get('priority') == 'P3'])
        }
    
    def get_stats(self) -> dict:
        """Return current statistics."""
        return self.index.get("stats", {})
    
    def search_by_tag(self, tag: str) -> list:
        """Search files by tag."""
        return [f for f in self.index["files"] if tag.lower() in [t.lower() for t in f.get('tags', [])]]
    
    def search_by_priority(self, priority: str) -> list:
        """Search files by priority."""
        return [f for f in self.index["files"] if f.get('priority') == priority.upper()]


def main():
    """Main entry point."""
    import sys
    
    manager = MetadataManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--scan":
            manager.scan_vault()
        
        elif command == "--stats":
            stats = manager.get_stats()
            print("\n=== Metadata Stats ===")
            for key, value in stats.items():
                print(f"{key}: {value}")
        
        elif command == "--search-tag":
            if len(sys.argv) > 2:
                results = manager.search_by_tag(sys.argv[2])
                print(f"\nFiles with tag '{sys.argv[2]}':")
                for f in results:
                    print(f"  - {f['path']}")
        
        elif command == "--search-priority":
            if len(sys.argv) > 2:
                results = manager.search_by_priority(sys.argv[2])
                print(f"\nFiles with priority {sys.argv[2]}:")
                for f in results:
                    print(f"  - {f['path']}")
        
        else:
            print("Usage: python util_metadata-manager_v1.0.py [--scan|--stats|--search-tag <tag>|--search-priority <P1|P2|P3>]")
    else:
        # Default: scan and show stats
        manager.scan_vault()
        stats = manager.get_stats()
        print("\n=== Quick Stats ===")
        print(f"Total files: {stats['total_files']}")
        print(f"Active plans: {stats['active_plans']}")
        print(f"P1 (Urgent): {stats['p1_count']}")
        print(f"P2 (High): {stats['p2_count']}")
        print(f"P3 (Normal): {stats['p3_count']}")


if __name__ == "__main__":
    main()
