"""
Briefing MCP - Weekly CEO Briefing Generator
Version: 0.3 Gold Tier - Phase 4
Owner: Suleman AI Employee v0.3

Generates comprehensive CEO briefings from accounting data and completed tasks.
Runs every Sunday at 11 PM PKT or on-demand.

Usage:
    echo '{}' | python MCP/briefing/briefing_mcp.py
"""

import json
import sys
import os
import csv
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional

# Configuration
ROOT_DIR = Path(__file__).parent.parent.parent
LOGS_DIR = ROOT_DIR / "Logs"
BRIEFINGS_DIR = ROOT_DIR / "Briefings"
ACCOUNTING_DIR = ROOT_DIR / "Accounting"
DASHBOARD_FILE = ROOT_DIR / "Dashboard.md"
DONE_BUSINESS = ROOT_DIR / "Business" / "Done" / "Business"
DONE_PERSONAL = ROOT_DIR / "Personal" / "Done" / "Personal"
SOCIAL_REPORTS_DIR = ROOT_DIR / "Business" / "Social_Reports"

# Ensure directories exist
for dir_path in [LOGS_DIR, BRIEFINGS_DIR]:
    dir_path.mkdir(exist_ok=True)


def get_audit_log_path() -> Path:
    """Get today's audit log file path."""
    today = datetime.now().strftime("%Y-%m-%d")
    return LOGS_DIR / f"audit_{today}.json"


def log_action(action: str, status: str, details: Optional[Dict] = None, error: Optional[str] = None):
    """Log every action to audit JSON file."""
    log_path = get_audit_log_path()
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "status": status,
        "details": details or {},
        "error": error
    }
    
    # Load existing logs
    logs = []
    if log_path.exists():
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except (json.JSONDecodeError, IOError):
            logs = []
    
    logs.append(entry)
    
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)


def read_transactions(days: int = 7) -> List[Dict[str, Any]]:
    """
    Read transactions from CSV file for the last N days.
    
    Args:
        days: Number of days to look back
    
    Returns:
        List of transaction dictionaries
    """
    transactions_file = ACCOUNTING_DIR / "transactions.csv"
    transactions = []
    
    if not transactions_file.exists():
        log_action("read_transactions", "warning", {"error": "File not found"})
        return transactions
    
    cutoff_date = datetime.now() - timedelta(days=days)
    
    try:
        with open(transactions_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    txn_date = datetime.strptime(row.get("date", ""), "%Y-%m-%d")
                    if txn_date >= cutoff_date:
                        transactions.append({
                            "date": row.get("date", ""),
                            "amount": float(row.get("amount", 0)),
                            "description": row.get("description", ""),
                            "category": row.get("category", "Uncategorized"),
                            "domain": row.get("domain", "Business"),
                            "status": row.get("status", "pending")
                        })
                except (ValueError, KeyError):
                    pass
        
        log_action("read_transactions", "success", {"count": len(transactions)})
        
    except Exception as e:
        log_action("read_transactions", "error", {"error": str(e)})
    
    return transactions


def calculate_financial_summary(transactions: List[Dict]) -> Dict[str, Any]:
    """
    Calculate financial summary from transactions.
    
    Returns:
        Dict with revenue, expenses, profit, and breakdowns
    """
    revenue = 0
    expenses = 0
    revenue_by_category = {}
    expenses_by_category = {}
    flagged_transactions = []
    
    for txn in transactions:
        amount = txn.get("amount", 0)
        category = txn.get("category", "Uncategorized")
        status = txn.get("status", "pending")
        
        # Flag high-value or pending transactions
        if abs(amount) > 10000 or status == "pending":
            flagged_transactions.append(txn)
        
        if amount > 0:
            revenue += amount
            revenue_by_category[category] = revenue_by_category.get(category, 0) + amount
        else:
            expenses += abs(amount)
            expenses_by_category[category] = expenses_by_category.get(category, 0) + abs(amount)
    
    return {
        "total_revenue": revenue,
        "total_expenses": expenses,
        "net_profit": revenue - expenses,
        "revenue_by_category": revenue_by_category,
        "expenses_by_category": expenses_by_category,
        "flagged_transactions": flagged_transactions
    }


def count_completed_tasks(days: int = 7) -> Dict[str, Any]:
    """
    Count completed tasks in Done folders for the last N days.
    
    Returns:
        Dict with task counts and lists
    """
    business_tasks = []
    personal_tasks = []
    
    cutoff_date = datetime.now() - timedelta(days=days)
    
    # Count Business tasks
    if DONE_BUSINESS.exists():
        for file_path in DONE_BUSINESS.glob("*.md"):
            try:
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                if mtime >= cutoff_date:
                    business_tasks.append({
                        "name": file_path.stem,
                        "completed_at": mtime.isoformat()
                    })
            except:
                pass
    
    # Count Personal tasks
    if DONE_PERSONAL.exists():
        for file_path in DONE_PERSONAL.glob("*.md"):
            try:
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                if mtime >= cutoff_date:
                    personal_tasks.append({
                        "name": file_path.stem,
                        "completed_at": mtime.isoformat()
                    })
            except:
                pass
    
    return {
        "business_tasks": business_tasks,
        "personal_tasks": personal_tasks,
        "total_tasks": len(business_tasks) + len(personal_tasks)
    }


def get_social_summary(days: int = 7) -> Dict[str, Any]:
    """
    Get summary of social media reports for the last N days.
    
    Returns:
        Dict with social media stats
    """
    summary = {
        "total_posts": 0,
        "platforms": {},
        "posts_list": []
    }
    
    if not SOCIAL_REPORTS_DIR.exists():
        return summary
    
    cutoff_date = datetime.now() - timedelta(days=days)
    
    for report_file in SOCIAL_REPORTS_DIR.glob("*.md"):
        try:
            mtime = datetime.fromtimestamp(report_file.stat().st_mtime)
            if mtime >= cutoff_date:
                with open(report_file, "r", encoding="utf-8") as f:
                    content = f.read().lower()
                    
                    # Detect platform
                    platform = None
                    if "facebook" in content:
                        platform = "facebook"
                    elif "instagram" in content:
                        platform = "instagram"
                    elif "twitter" in content:
                        platform = "twitter"
                    
                    if platform:
                        summary["platforms"][platform] = summary["platforms"].get(platform, 0) + 1
                        summary["posts_list"].append({
                            "platform": platform,
                            "file": report_file.name,
                            "date": mtime.isoformat()
                        })
                    
                    summary["total_posts"] += 1
                    
        except Exception:
            pass
    
    return summary


def generate_suggestions(financial_summary: Dict, task_counts: Dict, social_summary: Dict) -> List[str]:
    """
    Generate proactive suggestions based on data analysis.
    
    Returns:
        List of suggestion strings
    """
    suggestions = []
    
    # Check for high expenses
    expenses_by_category = financial_summary.get("expenses_by_category", {})
    
    if expenses_by_category.get("Subscriptions", 0) > 5000:
        suggestions.append("Review subscriptions – consider canceling unused tools (Save PKR 2,000+/month)")
    
    if expenses_by_category.get("Marketing", 0) > 10000:
        suggestions.append("Marketing spend high this week – review ROI")
    
    # Check for flagged transactions
    flagged = financial_summary.get("flagged_transactions", [])
    if flagged:
        suggestions.append(f"{len(flagged)} transaction(s) flagged for review (high value or pending)")
    
    # Check task completion
    if task_counts.get("total_tasks", 0) < 5:
        suggestions.append("Low task completion rate – review bottlenecks")
    
    # Check social activity
    if social_summary.get("total_posts", 0) < 3:
        suggestions.append("Increase social media activity – aim for 5+ posts/week")
    
    # Default suggestion if nothing else
    if not suggestions:
        suggestions.append("All metrics within target range – maintain current trajectory")
    
    return suggestions


def generate_briefing_content(
    financial_summary: Dict,
    task_counts: Dict,
    social_summary: Dict,
    suggestions: List[str]
) -> str:
    """
    Generate full briefing markdown content.
    
    Returns:
        Markdown string for briefing
    """
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    
    content = f"""# CEO Weekly Briefing

**Week:** {week_start.strftime('%Y-%m-%d')} to {today.strftime('%Y-%m-%d')}  
**Generated:** {today.strftime('%Y-%m-%d %I:%M %p PKT')}  
**Prepared by:** Suleman AI Employee v0.3 Gold Tier

---

## Executive Summary

| Metric | This Week | Status |
|--------|-----------|--------|
| Revenue | PKR {financial_summary.get('total_revenue', 0):,.0f} | {'✅ Good' if financial_summary.get('total_revenue', 0) > 100000 else '⚠️ Below Target'} |
| Expenses | PKR {financial_summary.get('total_expenses', 0):,.0f} | {'✅ On Budget' if financial_summary.get('total_expenses', 0) < 20000 else '⚠️ Over Budget'} |
| Net Profit | PKR {financial_summary.get('net_profit', 0):,.0f} | {'✅ Profitable' if financial_summary.get('net_profit', 0) > 0 else '🔴 Loss'} |
| Tasks Completed | {task_counts.get('total_tasks', 0)} | {'✅ On Track' if task_counts.get('total_tasks', 0) >= 5 else '⚠️ Behind'} |
| Social Posts | {social_summary.get('total_posts', 0)} | {'✅ Active' if social_summary.get('total_posts', 0) >= 3 else '⚠️ Low'} |

---

## Revenue Breakdown

"""
    
    # Revenue by category
    revenue_by_category = financial_summary.get("revenue_by_category", {})
    if revenue_by_category:
        content += "| Category | Amount |\n|----------|--------|\n"
        for category, amount in revenue_by_category.items():
            content += f"| {category} | PKR {amount:,.0f} |\n"
    else:
        content += "*No revenue recorded this week*\n"
    
    content += "\n---\n\n## Expense Breakdown\n\n"
    
    # Expenses by category
    expenses_by_category = financial_summary.get("expenses_by_category", {})
    if expenses_by_category:
        content += "| Category | Amount |\n|----------|--------|\n"
        for category, amount in expenses_by_category.items():
            content += f"| {category} | PKR {amount:,.0f} |\n"
    else:
        content += "*No expenses recorded this week*\n"
    
    # Flagged transactions
    flagged = financial_summary.get("flagged_transactions", [])
    if flagged:
        content += "\n### Flagged for Review\n\n"
        for txn in flagged:
            content += f"- {txn['description']} (PKR {txn['amount']:,.0f}) - {txn['status']}\n"
    
    content += f"""
---

## Completed Tasks

**Total:** {task_counts.get('total_tasks', 0)} tasks

### Business Tasks: {len(task_counts.get('business_tasks', []))}
"""
    
    for task in task_counts.get('business_tasks', [])[:10]:
        content += f"- {task['name']}\n"
    
    if not task_counts.get('business_tasks', []):
        content += "*No business tasks completed*\n"
    
    content += f"""
---

## Social Performance

"""
    
    platforms = social_summary.get("platforms", {})
    if platforms:
        content += "| Platform | Posts | Status |\n|----------|-------|--------|\n"
        for platform, count in platforms.items():
            status = "✅ Active" if count >= 2 else "⚠️ Low"
            content += f"| {platform.title()} | {count} | {status} |\n"
    else:
        content += "*No social media activity recorded*\n"
    
    content += "\n---\n\n## Proactive Suggestions\n\n"
    
    for i, suggestion in enumerate(suggestions, 1):
        content += f"{i}. {suggestion}\n"
    
    content += f"""
---

## Next Week Priorities

1. Review and approve flagged transactions
2. Continue Gold Tier development
3. Increase social media activity

---

## CEO Action Items

- [ ] Review briefing and provide feedback
- [ ] Approve flagged expenses
- [ ] Set priorities for next week

---

**End of Briefing**

*Generated automatically by Briefing MCP v0.3*
*Next briefing: Sunday 11 PM PKT*
"""
    
    return content


def update_dashboard(briefing_data: Dict):
    """
    Update Dashboard.md with latest briefing info.
    
    Args:
        briefing_data: Briefing data dictionary
    """
    if not DASHBOARD_FILE.exists():
        log_action("update_dashboard", "warning", {"error": "Dashboard not found"})
        return
    
    try:
        with open(DASHBOARD_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        
        today = datetime.now().strftime("%Y-%m-%d")
        revenue = briefing_data.get('total_revenue', 0)
        
        # Update "Last Briefing" line
        briefing_line = f"**Last Briefing:** {today} – Revenue: PKR {revenue:,.0f}"
        
        if "**Last Briefing:**" in content:
            # Update existing line
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if "**Last Briefing:**" in line:
                    lines[i] = briefing_line
                    break
            content = "\n".join(lines)
        else:
            # Add new section
            content += f"\n{briefing_line}\n"
        
        with open(DASHBOARD_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        
        log_action("update_dashboard", "success", {"briefing_date": today})
        
    except Exception as e:
        log_action("update_dashboard", "error", {"error": str(e)})


def generate_briefing(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main briefing generation function.
    
    Args:
        input_data: JSON input (can include override parameters)
    
    Returns:
        Dict with briefing result
    """
    log_action("briefing_generation", "info", {"status": "starting"})
    
    try:
        # Read transactions (last 7 days)
        transactions = read_transactions(days=7)
        
        # Calculate financial summary
        financial_summary = calculate_financial_summary(transactions)
        
        # Count completed tasks
        task_counts = count_completed_tasks(days=7)
        
        # Get social summary
        social_summary = get_social_summary(days=7)
        
        # Generate suggestions
        suggestions = generate_suggestions(financial_summary, task_counts, social_summary)
        
        # Generate briefing content
        briefing_content = generate_briefing_content(
            financial_summary,
            task_counts,
            social_summary,
            suggestions
        )
        
        # Save briefing
        today = datetime.now().strftime("%Y-%m-%d")
        briefing_file = BRIEFINGS_DIR / f"CEO_Briefing_{today}.md"
        
        with open(briefing_file, "w", encoding="utf-8") as f:
            f.write(briefing_content)
        
        # Update dashboard
        update_dashboard(financial_summary)
        
        log_action("briefing_generation", "success", {
            "file": str(briefing_file),
            "revenue": financial_summary.get("total_revenue", 0),
            "expenses": financial_summary.get("total_expenses", 0)
        })
        
        return {
            "status": "success",
            "briefing_file": str(briefing_file),
            "summary": {
                "revenue": financial_summary.get("total_revenue", 0),
                "expenses": financial_summary.get("total_expenses", 0),
                "profit": financial_summary.get("net_profit", 0),
                "tasks": task_counts.get("total_tasks", 0),
                "social_posts": social_summary.get("total_posts", 0)
            }
        }
        
    except Exception as e:
        log_action("briefing_generation", "error", {"error": str(e)})
        return {
            "status": "error",
            "error": str(e)
        }


def main():
    """Entry point - reads JSON from stdin and generates briefing."""
    try:
        # Read input from stdin
        input_text = sys.stdin.read()
        
        # Parse input (can be empty for default briefing)
        if input_text.strip():
            input_data = json.loads(input_text)
        else:
            input_data = {}
        
        # Generate briefing
        result = generate_briefing(input_data)
        
        # Output result as JSON
        print(json.dumps(result, indent=2))
        
    except json.JSONDecodeError as e:
        error_result = {"status": "error", "error": f"Invalid JSON input: {str(e)}"}
        log_action("briefing_mcp", "error", error_result)
        print(json.dumps(error_result))
    except Exception as e:
        error_result = {"status": "error", "error": str(e)}
        log_action("briefing_mcp", "error", error_result)
        print(json.dumps(error_result))


if __name__ == "__main__":
    main()
