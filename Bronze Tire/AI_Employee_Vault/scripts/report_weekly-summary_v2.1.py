#!/usr/bin/env python3
"""
Weekly Report Generator - Creates summary reports from vault activity.

Usage:
    python report_weekly-summary_v2.1.py
    python report_weekly-summary_v2.1.py --week 2026-W08
    python report_weekly-summary_v2.1.py --output report.md

Version: 2.1
"""

import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict


# Configuration
VAULT_ROOT = Path(__file__).parent.parent
DONE_DIR = VAULT_ROOT / "Done"
LOGS_ACTIVITY_DIR = VAULT_ROOT / "Logs" / "activity"
LOGS_ERRORS_DIR = VAULT_ROOT / "Logs" / "errors"
NEEDS_ACTION_DIR = VAULT_ROOT / "Needs_Action"
INBOX_DIR = VAULT_ROOT / "Inbox"


def get_current_week() -> str:
    """Get current ISO week string (YYYY-Www)."""
    return datetime.now().strftime("%Y-W%W")


def parse_week(week_str: str) -> Tuple[datetime, datetime]:
    """Parse week string and return (start_date, end_date)."""
    try:
        year, week = week_str.split("-W")
        year = int(year)
        week = int(week)
        
        # Get first day of week (Monday)
        start = datetime.strptime(f"{year}-W{week:02d}-1", "%Y-W%W-%w")
        end = start + timedelta(days=6)
        
        return start, end
    except ValueError:
        print(f"❌ Invalid week format: {week_str}. Use YYYY-Www (e.g., 2026-W08)")
        sys.exit(1)


def count_files_by_date(folder: Path, start: datetime, end: datetime) -> int:
    """Count files created/modified within date range."""
    if not folder.exists():
        return 0
    
    count = 0
    for f in folder.iterdir():
        if f.is_file():
            try:
                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                if start <= mtime <= end + timedelta(days=1):
                    count += 1
            except Exception:
                pass
    
    return count


def parse_activity_logs(start: datetime, end: datetime) -> Dict[str, int]:
    """Parse activity logs and extract statistics."""
    stats = {
        "moves": 0,
        "errors": 0,
        "total_actions": 0,
        "by_category": defaultdict(int),
        "by_priority": defaultdict(int),
    }
    
    if not LOGS_ACTIVITY_DIR.exists():
        return stats
    
    for log_file in LOGS_ACTIVITY_DIR.iterdir():
        if not log_file.is_file():
            continue
        
        try:
            log_date = datetime.strptime(log_file.stem.split("_")[-1], "%Y-%m-%d")
            if not (start <= log_date <= end + timedelta(days=1)):
                continue
            
            with open(log_file, "r", encoding="utf-8") as f:
                for line in f:
                    stats["total_actions"] += 1
                    
                    if "| MOVE |" in line:
                        stats["moves"] += 1
                        
                        # Extract category
                        if "category=" in line:
                            for cat in ["contract", "bug", "meeting", "report", "invoice", "feature", "general"]:
                                if f"category={cat}" in line:
                                    stats["by_category"][cat] += 1
                                    break
                        
                        # Extract priority
                        if "priority=" in line:
                            for pri in ["P1", "P2", "P3", "P4"]:
                                if f"priority={pri}" in line:
                                    stats["by_priority"][pri] += 1
                                    break
                    
                    if "| ERROR |" in line:
                        stats["errors"] += 1
                        
        except Exception:
            continue
    
    return stats


def count_pending_by_priority() -> Dict[str, int]:
    """Count items in Needs_Action by priority."""
    counts = {"P1": 0, "P2": 0, "P3": 0, "P4": 0}
    
    if not NEEDS_ACTION_DIR.exists():
        return counts
    
    for f in NEEDS_ACTION_DIR.iterdir():
        if f.is_file():
            name_lower = f.name.lower()
            for priority in ["P1", "P2", "P3", "P4"]:
                if f"_{priority}_" in name_lower or f"[{priority.lower()}]" in name_lower:
                    counts[priority] += 1
                    break
    
    return counts


def generate_report(week: str, output_file: Path = None) -> str:
    """Generate weekly summary report."""
    start, end = parse_week(week)
    
    # Gather statistics
    activity_stats = parse_activity_logs(start, end)
    pending = count_pending_by_priority()
    
    inbox_count = len([f for f in INBOX_DIR.iterdir() if f.is_file()]) if INBOX_DIR.exists() else 0
    needs_action_count = sum(pending.values())
    
    # Build report
    report = []
    report.append("# 📈 Weekly Summary Report")
    report.append("")
    report.append(f"**Week:** {week}")
    report.append(f"**Period:** {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}")
    report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Key Metrics
    report.append("## 🎯 Key Metrics")
    report.append("")
    report.append("| Metric | Value |")
    report.append("|--------|-------|")
    report.append(f"| Files Processed | {activity_stats['moves']} |")
    report.append(f"| Errors | {activity_stats['errors']} |")
    report.append(f"| Total Actions | {activity_stats['total_actions']} |")
    report.append(f"| Current Inbox | {inbox_count} |")
    report.append(f"| Pending Actions | {needs_action_count} |")
    report.append("")
    
    # Priority Breakdown
    report.append("## ⚠️ Pending by Priority")
    report.append("")
    report.append("| Priority | Count |")
    report.append("|----------|-------|")
    for pri in ["P1", "P2", "P3", "P4"]:
        emoji = {"P1": "🔴", "P2": "🟠", "P3": "🟡", "P4": "🟢"}.get(pri, "")
        report.append(f"| {emoji} {pri} | {pending[pri]} |")
    report.append("")
    
    # Category Breakdown
    if activity_stats["by_category"]:
        report.append("## 📁 Files by Category")
        report.append("")
        report.append("| Category | Count |")
        report.append("|----------|-------|")
        for cat, count in sorted(activity_stats["by_category"].items(), key=lambda x: -x[1]):
            report.append(f"| {cat.capitalize()} | {count} |")
        report.append("")
    
    # Daily Activity (if data available)
    if activity_stats["total_actions"] > 0:
        report.append("## 📅 Activity Timeline")
        report.append("")
        report.append("```")
        for day_offset in range(7):
            day = start + timedelta(days=day_offset)
            day_str = day.strftime("%Y-%m-%d")
            log_file = LOGS_ACTIVITY_DIR / f"activity_{day_str}.log"
            
            if log_file.exists():
                with open(log_file, "r", encoding="utf-8") as f:
                    day_count = sum(1 for _ in f)
                bar = "█" * min(day_count, 20)
                report.append(f"{day.strftime('%a')} {day_str[5:]} | {bar} {day_count}")
            else:
                report.append(f"{day.strftime('%a')} {day_str[5:]} | — 0")
        report.append("```")
        report.append("")
    
    # Recommendations
    report.append("## 💡 Recommendations")
    report.append("")
    
    if activity_stats["errors"] > 0:
        report.append(f"- ⚠️ Review {activity_stats['errors']} error(s) in Logs/errors/")
    
    if pending["P1"] > 0:
        report.append(f"- 🔴 {pending['P1']} urgent item(s) need immediate attention")
    
    if inbox_count > 0:
        report.append(f"- 📥 Process {inbox_count} inbox item(s) to achieve inbox zero")
    
    if activity_stats["moves"] == 0:
        report.append("- 📭 No activity this week. Consider reviewing automation settings.")
    
    if not any([activity_stats["errors"], pending["P1"], inbox_count, activity_stats["moves"] == 0]):
        report.append("- ✅ All systems operational. Great work!")
    
    report.append("")
    
    # Footer
    report.append("---")
    report.append("")
    report.append("*Report generated by `report_weekly-summary_v2.1.py`*")
    
    report_text = "\n".join(report)
    
    # Save to file if specified
    if output_file:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report_text)
        print(f"✅ Report saved to: {output_file}")
    
    return report_text


def main():
    parser = argparse.ArgumentParser(
        description="Generate weekly summary report for AI Employee Vault"
    )
    
    parser.add_argument(
        "--week", "-w",
        default=get_current_week(),
        help=f"Week to report on (default: {get_current_week()})"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output file path (default: print to console)"
    )
    parser.add_argument(
        "--save-default",
        action="store_true",
        help="Save to Logs/weekly-report-YYYY-Www.md"
    )
    
    args = parser.parse_args()
    
    # Determine output path
    output_file = None
    if args.save_default:
        output_file = VAULT_ROOT / "Logs" / f"weekly-report-{args.week}.md"
    elif args.output:
        output_file = args.output
    
    # Generate report
    report = generate_report(args.week, output_file)
    
    if not output_file:
        print(report)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
