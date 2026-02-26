#!/usr/bin/env python3
"""
File Mover Utility - Manual file routing between vault folders.

Usage:
    python util_file-mover_v0.5.py --source Inbox --dest Needs_Action
    python util_file-mover_v0.5.py --health
    python util_file-mover_v0.5.py --list Inbox

Version: 0.5
"""

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import List


# Configuration
VAULT_ROOT = Path(__file__).parent.parent

FOLDERS = {
    "Inbox": VAULT_ROOT / "Inbox",
    "Needs_Action": VAULT_ROOT / "Needs_Action",
    "Plans": VAULT_ROOT / "Plans",
    "Done": VAULT_ROOT / "Done",
    "Logs": VAULT_ROOT / "Logs",
}


def get_folder(folder_name: str) -> Path:
    """Get folder path by name."""
    if folder_name not in FOLDERS:
        raise ValueError(f"Unknown folder: {folder_name}. Valid: {list(FOLDERS.keys())}")
    return FOLDERS[folder_name]


def list_files(folder_name: str) -> List[Path]:
    """List all files in a folder."""
    folder = get_folder(folder_name)
    if not folder.exists():
        return []
    return [f for f in folder.iterdir() if f.is_file()]


def move_file(source_folder: str, filename: str, dest_folder: str) -> bool:
    """Move a file between folders."""
    source_path = get_folder(source_folder) / filename
    dest_path = get_folder(dest_folder) / filename
    
    if not source_path.exists():
        print(f"❌ Source file not found: {source_path}")
        return False
    
    # Handle duplicates
    if dest_path.exists():
        counter = 1
        name_parts = filename.rsplit(".", 1)
        while True:
            if len(name_parts) > 1:
                new_name = f"{name_parts[0]}_{counter}.{name_parts[1]}"
            else:
                new_name = f"{name_parts[0]}_{counter}"
            dest_path = get_folder(dest_folder) / new_name
            if not dest_path.exists():
                break
            counter += 1
    
    try:
        shutil.move(str(source_path), str(dest_path))
        print(f"✅ Moved: {filename}")
        print(f"   From: {source_folder}/")
        print(f"   To: {dest_folder}/")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def move_all(source_folder: str, dest_folder: str) -> tuple:
    """Move all files from source to destination folder."""
    files = list_files(source_folder)
    success = 0
    failed = 0
    
    for file_path in files:
        if move_file(source_folder, file_path.name, dest_folder):
            success += 1
        else:
            failed += 1
    
    return success, failed


def health_check() -> bool:
    """Check vault health and folder status."""
    print("Vault Health Check")
    print("=" * 50)

    all_ok = True

    for name, path in FOLDERS.items():
        exists = path.exists()
        status = "[OK]" if exists else "[--]"
        print(f"{status} {name}/")

        if not exists:
            all_ok = False
            print(f"   Creating: {path}")
            path.mkdir(parents=True, exist_ok=True)
        else:
            file_count = len([f for f in path.iterdir() if f.is_file()])
            print(f"   Files: {file_count}")

    print("=" * 50)

    # Quick stats
    inbox_count = len(list_files("Inbox"))
    action_count = len(list_files("Needs_Action"))

    print("Quick Stats:")
    print(f"   Inbox: {inbox_count} items")
    print(f"   Needs Action: {action_count} items")

    if inbox_count > 0:
        print(f"\nWarning: Inbox has {inbox_count} unprocessed items")

    return all_ok


def show_tree():
    """Display folder tree structure."""
    print("AI Employee Vault Structure")
    print("=" * 50)
    
    for name, path in sorted(FOLDERS.items()):
        if path.exists():
            print(f"{name}/")
            for item in sorted(path.iterdir()):
                if item.is_dir():
                    print(f"  [DIR]  {item.name}/")
                else:
                    print(f"  [FILE] {item.name}")
        else:
            print(f"{name}/ (not created)")
    
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(
        description="File Mover Utility for AI Employee Vault",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s --list Inbox
    %(prog)s --source Inbox --dest Needs_Action
    %(prog)s --source Inbox --dest Needs_Action --file report.pdf
    %(prog)s --health
    %(prog)s --tree
        """
    )
    
    parser.add_argument("--source", "-s", help="Source folder name")
    parser.add_argument("--dest", "-d", help="Destination folder name")
    parser.add_argument("--file", "-f", help="Specific file to move")
    parser.add_argument("--list", "-l", metavar="FOLDER", help="List files in folder")
    parser.add_argument("--health", action="store_true", help="Run health check")
    parser.add_argument("--tree", action="store_true", help="Show folder tree")
    
    args = parser.parse_args()
    
    # Handle health check
    if args.health:
        health_check()
        return 0
    
    # Handle tree view
    if args.tree:
        show_tree()
        return 0
    
    # Handle list
    if args.list:
        try:
            files = list_files(args.list)
            print(f"📁 {args.list}/ ({len(files)} files)")
            print("-" * 50)
            for f in sorted(files, key=lambda x: x.name.lower()):
                size = f.stat().st_size
                size_str = f"{size:,} bytes" if size < 1024 else f"{size/1024:.1f} KB"
                modified = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                print(f"  {f.name} ({size_str}, {modified})")
        except ValueError as e:
            print(f"❌ {e}")
            return 1
        return 0
    
    # Handle move operations
    if args.source and args.dest:
        try:
            if args.file:
                # Move specific file
                success = move_file(args.source, args.file, args.dest)
                return 0 if success else 1
            else:
                # Move all files
                print(f"🔄 Moving all files from {args.source}/ → {args.dest}/")
                success, failed = move_all(args.source, args.dest)
                print(f"✅ Done: {success} moved, {failed} failed")
                return 0 if failed == 0 else 1
        except ValueError as e:
            print(f"❌ {e}")
            return 1
    
    # No valid arguments
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
