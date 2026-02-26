#!/usr/bin/env python3
"""
Metadata Manager - Manages file metadata using sidecar files and central index.

Creates .meta.json sidecar files for each document and maintains a central
metadata_index.json for searchability and statistics.

Version: 1.0
"""

import json
import os
import hashlib
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, asdict, field


# Configuration
VAULT_ROOT = Path(__file__).parent.parent
METADATA_INDEX = VAULT_ROOT / "metadata_index.json"

# Folder paths
FOLDERS = {
    "Inbox": VAULT_ROOT / "Inbox",
    "Needs_Action": VAULT_ROOT / "Needs_Action",
    "Plans": VAULT_ROOT / "Plans",
    "Done": VAULT_ROOT / "Done",
    "Logs": VAULT_ROOT / "Logs",
}

# Default metadata values
DEFAULTS = {
    "priority": "P3",
    "status": "pending",
    "assignee": "unassigned",
    "category": "general",
}


@dataclass
class FileMetadata:
    """Represents metadata for a single file."""
    file_id: str
    filename: str
    path: str
    created: str
    modified: str
    size_bytes: int
    type: str = "document"
    priority: str = DEFAULTS["priority"]
    status: str = DEFAULTS["status"]
    assignee: str = DEFAULTS["assignee"]
    category: str = DEFAULTS["category"]
    tags: List[str] = field(default_factory=list)
    due_date: Optional[str] = None
    source: Optional[str] = None
    related_files: List[str] = field(default_factory=list)
    custom: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> "FileMetadata":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


class MetadataManager:
    """Manages metadata for all files in the vault."""
    
    def __init__(self):
        self.index = self._load_index()
    
    def _load_index(self) -> Dict:
        """Load the central metadata index."""
        if METADATA_INDEX.exists():
            with open(METADATA_INDEX, "r", encoding="utf-8") as f:
                return json.load(f)
        return self._create_empty_index()
    
    def _create_empty_index(self) -> Dict:
        """Create a new empty index."""
        return {
            "version": "1.0",
            "created": datetime.now().strftime("%Y-%m-%d"),
            "last_updated": datetime.now().isoformat(),
            "vault_name": "AI_Employee_Vault",
            "ai_employee": "Suleman AI Employee v0.1 Bronze",
            "statistics": {
                "total_files": 0,
                "total_plans": 0,
                "total_tasks": 0,
                "pending_tasks": 0,
                "completed_tasks": 0,
                "files_by_folder": {k: 0 for k in FOLDERS.keys()},
                "files_by_priority": {"P1": 0, "P2": 0, "P3": 0, "P4": 0},
                "files_by_category": {}
            },
            "files": [],
            "tags": [],
            "assignees": [],
            "plans": [],
            "tasks": []
        }
    
    def _save_index(self):
        """Save the central metadata index."""
        self.index["last_updated"] = datetime.now().isoformat()
        with open(METADATA_INDEX, "w", encoding="utf-8") as f:
            json.dump(self.index, f, indent=2)
    
    def _generate_file_id(self, filepath: Path) -> str:
        """Generate a unique ID for a file based on its path and content."""
        content = f"{str(filepath)}-{datetime.now().isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def _get_sidecar_path(self, filepath: Path) -> Path:
        """Get the sidecar file path for a given file."""
        return Path(str(filepath) + ".meta.json")
    
    def _detect_type(self, filepath: Path) -> str:
        """Detect file type based on path and content."""
        path_str = str(filepath).lower()
        
        if "/Plans/" in path_str or "plan" in filepath.name.lower():
            return "plan"
        elif "/Logs/" in path_str:
            return "log"
        elif "/Inbox/" in path_str:
            return "inbox"
        elif "/Needs_Action/" in path_str:
            return "task"
        elif "/Done/" in path_str:
            return "archived"
        return "document"
    
    def _detect_priority(self, filename: str) -> str:
        """Detect priority from filename."""
        filename_lower = filename.lower()
        
        if "_p1_" in filename_lower or "[p1]" in filename_lower:
            return "P1"
        elif "_p2_" in filename_lower or "[p2]" in filename_lower:
            return "P2"
        elif "_p3_" in filename_lower or "[p3]" in filename_lower:
            return "P3"
        elif "_p4_" in filename_lower or "[p4]" in filename_lower:
            return "P4"
        
        # Keyword detection
        urgent_keywords = ["urgent", "emergency", "critical", "asap"]
        high_keywords = ["high", "important", "deadline"]
        low_keywords = ["low", "nice-to-have", "future"]
        
        for kw in urgent_keywords:
            if kw in filename_lower:
                return "P1"
        for kw in high_keywords:
            if kw in filename_lower:
                return "P2"
        for kw in low_keywords:
            if kw in filename_lower:
                return "P4"
        
        return "P3"
    
    def _detect_category(self, filename: str) -> str:
        """Detect category from filename."""
        categories = {
            "contract": ["contract", "agreement", "nda", "sow", "proposal"],
            "bug": ["bug", "error", "issue", "defect", "fix"],
            "meeting": ["meeting", "standup", "sync", "call", "notes"],
            "report": ["report", "summary", "metrics", "dashboard"],
            "invoice": ["invoice", "receipt", "payment", "bill"],
            "feature": ["feature", "enhancement", "request"],
            "client": ["client", "customer", "onboarding"],
        }
        
        filename_lower = filename.lower()
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in filename_lower:
                    return category
        return "general"
    
    def _extract_tags(self, filepath: Path) -> List[str]:
        """Extract tags from file content (frontmatter or inline)."""
        tags = []
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read(2048)  # Read first 2KB
            
            # Look for YAML frontmatter tags
            frontmatter_match = re.search(r'^---\s*\n.*?tags:\s*\[(.*?)\]', content, re.DOTALL)
            if frontmatter_match:
                tags = [t.strip() for t in frontmatter_match.group(1).split(",")]
            
            # Look for inline tags (#tag format)
            inline_tags = re.findall(r'#(\w+)', content)
            tags.extend(inline_tags)
            
        except Exception:
            pass
        
        return list(set(tags))
    
    def create_sidecar(self, filepath: Path, custom_data: Optional[Dict] = None) -> FileMetadata:
        """Create a sidecar metadata file for a given file."""
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        stat = filepath.stat()
        file_type = self._detect_type(filepath)
        
        metadata = FileMetadata(
            file_id=self._generate_file_id(filepath),
            filename=filepath.name,
            path=str(filepath.relative_to(VAULT_ROOT)),
            created=datetime.fromtimestamp(stat.st_ctime).isoformat(),
            modified=datetime.fromtimestamp(stat.st_mtime).isoformat(),
            size_bytes=stat.st_size,
            type=file_type,
            priority=self._detect_priority(filepath.name),
            category=self._detect_category(filepath.name),
            tags=self._extract_tags(filepath),
            custom=custom_data or {}
        )
        
        # Save sidecar
        sidecar_path = self._get_sidecar_path(filepath)
        with open(sidecar_path, "w", encoding="utf-8") as f:
            json.dump(metadata.to_dict(), f, indent=2)
        
        # Update index
        self._add_to_index(metadata)
        
        return metadata
    
    def load_sidecar(self, filepath: Path) -> Optional[FileMetadata]:
        """Load metadata from a sidecar file."""
        sidecar_path = self._get_sidecar_path(filepath)
        
        if not sidecar_path.exists():
            return None
        
        with open(sidecar_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        return FileMetadata.from_dict(data)
    
    def update_sidecar(self, filepath: Path, updates: Dict) -> FileMetadata:
        """Update metadata in a sidecar file."""
        metadata = self.load_sidecar(filepath)
        
        if not metadata:
            metadata = self.create_sidecar(filepath)
        
        # Apply updates
        for key, value in updates.items():
            if hasattr(metadata, key):
                setattr(metadata, key, value)
        
        metadata.modified = datetime.now().isoformat()
        
        # Save updated sidecar
        sidecar_path = self._get_sidecar_path(filepath)
        with open(sidecar_path, "w", encoding="utf-8") as f:
            json.dump(metadata.to_dict(), f, indent=2)
        
        # Update index
        self._update_in_index(metadata)
        
        return metadata
    
    def _add_to_index(self, metadata: FileMetadata):
        """Add metadata to the central index."""
        # Add to files list
        file_entry = {
            "file_id": metadata.file_id,
            "filename": metadata.filename,
            "path": metadata.path,
            "type": metadata.type,
            "priority": metadata.priority,
            "status": metadata.status,
            "tags": metadata.tags
        }
        self.index["files"].append(file_entry)
        
        # Update statistics
        self._update_statistics(metadata)
        
        # Update tags index
        for tag in metadata.tags:
            if tag not in self.index["tags"]:
                self.index["tags"].append(tag)
        
        # Update assignees index
        if metadata.assignee not in self.index["assignees"]:
            self.index["assignees"].append(metadata.assignee)
        
        # Update plans/tasks index
        if metadata.type == "plan":
            self.index["plans"].append(file_entry)
            self.index["statistics"]["total_plans"] += 1
        elif metadata.type == "task":
            self.index["tasks"].append(file_entry)
            self.index["statistics"]["total_tasks"] += 1
            if metadata.status == "pending":
                self.index["statistics"]["pending_tasks"] += 1
        
        self._save_index()
    
    def _update_in_index(self, metadata: FileMetadata):
        """Update metadata in the central index."""
        # Find and update in files list
        for i, entry in enumerate(self.index["files"]):
            if entry["file_id"] == metadata.file_id:
                self.index["files"][i] = {
                    "file_id": metadata.file_id,
                    "filename": metadata.filename,
                    "path": metadata.path,
                    "type": metadata.type,
                    "priority": metadata.priority,
                    "status": metadata.status,
                    "tags": metadata.tags
                }
                break
        
        self._save_index()
    
    def _update_statistics(self, metadata: FileMetadata):
        """Update statistics based on new metadata."""
        stats = self.index["statistics"]
        
        # Total files
        stats["total_files"] += 1
        
        # By folder
        for folder_name, folder_path in FOLDERS.items():
            if str(metadata.path).startswith(folder_name):
                stats["files_by_folder"][folder_name] += 1
                break
        
        # By priority
        stats["files_by_priority"][metadata.priority] += 1
        
        # By category
        if metadata.category not in stats["files_by_category"]:
            stats["files_by_category"][metadata.category] = 0
        stats["files_by_category"][metadata.category] += 1
    
    def search(self, query: str) -> List[Dict]:
        """
        Search files by query.
        
        Query format:
        - priority:P1
        - status:pending
        - assignee:alice
        - category:contract
        - tag:urgent
        - type:plan
        """
        results = []
        
        for file_entry in self.index["files"]:
            match = True
            
            # Parse query parts (support multiple conditions)
            conditions = query.split()
            for condition in conditions:
                if ":" not in condition:
                    continue
                
                key, value = condition.split(":", 1)
                
                if key == "priority" and file_entry.get("priority") != value:
                    match = False
                elif key == "status" and file_entry.get("status") != value:
                    match = False
                elif key == "assignee" and file_entry.get("assignee") != value:
                    match = False
                elif key == "category" and file_entry.get("category") != value:
                    match = False
                elif key == "type" and file_entry.get("type") != value:
                    match = False
                elif key == "tag" and value not in file_entry.get("tags", []):
                    match = False
            
            if match:
                results.append(file_entry)
        
        return results
    
    def get_by_tag(self, tag: str) -> List[Dict]:
        """Get all files with a specific tag."""
        return self.search(f"tag:{tag}")
    
    def get_by_assignee(self, assignee: str) -> List[Dict]:
        """Get all files assigned to a person."""
        return self.search(f"assignee:{assignee}")
    
    def get_by_priority(self, priority: str) -> List[Dict]:
        """Get all files with a specific priority."""
        return self.search(f"priority:{priority}")
    
    def get_statistics(self) -> Dict:
        """Get current statistics from the index."""
        return self.index.get("statistics", {})
    
    def rebuild_index(self):
        """Rebuild the entire index from existing sidecar files."""
        self.index = self._create_empty_index()
        
        for folder in FOLDERS.values():
            if not folder.exists():
                continue
            
            for filepath in folder.rglob("*"):
                if filepath.is_file() and not filepath.name.endswith(".meta.json"):
                    try:
                        sidecar = self._get_sidecar_path(filepath)
                        if sidecar.exists():
                            with open(sidecar, "r", encoding="utf-8") as f:
                                data = json.load(f)
                            metadata = FileMetadata.from_dict(data)
                            self._add_to_index(metadata)
                    except Exception as e:
                        print(f"Error processing {filepath}: {e}")
        
        self._save_index()


# Convenience functions
def create_metadata(filepath: str, custom: Optional[Dict] = None) -> FileMetadata:
    """Create metadata for a file."""
    manager = MetadataManager()
    return manager.create_sidecar(Path(filepath), custom)


def update_metadata(filepath: str, updates: Dict) -> FileMetadata:
    """Update metadata for a file."""
    manager = MetadataManager()
    return manager.update_sidecar(Path(filepath), updates)


def search_files(query: str) -> List[Dict]:
    """Search files by query."""
    manager = MetadataManager()
    return manager.search(query)


def get_statistics() -> Dict:
    """Get vault statistics."""
    manager = MetadataManager()
    return manager.get_statistics()


if __name__ == "__main__":
    # Demo usage
    print("Metadata Manager v1.0")
    print("=" * 40)
    
    stats = get_statistics()
    print(f"Total files: {stats.get('total_files', 0)}")
    print(f"Total plans: {stats.get('total_plans', 0)}")
    print(f"Pending tasks: {stats.get('pending_tasks', 0)}")
