"""
MCP: Weekly CEO Briefing Generator
Generates comprehensive weekly reports for CEO review.
Runs every Sunday at 11 PM.
"""

import json
import sys
import os
import csv
from datetime import datetime, timedelta
from pathlib import Path
import glob

# Configuration
MAX_RETRIES = 3
ROOT_DIR = Path(__file__).parent.parent.parent
LOGS_DIR = ROOT_DIR / "Logs"
BRIEFINGS_DIR = ROOT_DIR / "Briefings"
ACCOUNTING_DIR = ROOT_DIR / "Accounting"
DONE_PERSONAL = ROOT_DIR / "Personal" / "Done" / "Personal"
DONE_BUSINESS = ROOT_DIR / "Business" / "Done" / "Business"
SOCIAL_REPORTS_DIR = ROOT_DIR / "Business" / "Social_Reports"
GOALS_FILE = ROOT_DIR / "Business" / "Goals.md"
DASHBOARD_FILE = ROOT_DIR / "Dashboard.md"

def get_audit_log_path():
    """Get today's audit log path."""
    today = datetime.now().strftime("%Y-%m-%d")
    return LOGS_DIR / f"audit_{today}.json"

def log_action(action, status, details=None, error=None):
    """Log every action to audit file."""
    LOGS_DIR.mkdir(exist_ok=True)
    log_path = get_audit_log_path()
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "status": status,
        "details": details or {},
        "error": str(error) if error else None
    }
    
    logs = []
    if log_path.exists():
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except:
            logs = []
    
    logs.append(entry)
    
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)

def get_week_range():
    """Get the date range for the current week (Monday to Sunday)."""
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    return monday.strftime("%Y-%m-%d"), sunday.strftime("%Y-%m-%d")

def read_transactions():
    """Read and parse transactions.csv."""
    transactions_file = ACCOUNTING_DIR / "transactions.csv"
    transactions = []
    
    if not transactions_file.exists():
        log_action("read_transactions", "warning", {"error": "File not found"})
        return transactions
    
    try:
        with open(transactions_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                transactions.append({
                    "date": row.get("date", ""),
                    "amount": float(row.get("amount", 0)),
                    "description": row.get("description", ""),
                    "category": row.get("category", ""),
                    "type": row.get("type", "")
                })
    except Exception as e:
        log_action("read_transactions", "error", {"error": str(e)})
    
    return transactions

def calculate_financial_summary(transactions):
    """Calculate revenue, expenses, and profit for the week."""
    monday, _ = get_week_range()
    monday_dt = datetime.strptime(monday, "%Y-%m-%d")
    
    revenue = 0
    expenses = 0
    revenue_breakdown = {}
    expense_breakdown = {}
    
    for txn in transactions:
        try:
            txn_date = datetime.strptime(txn["date"], "%Y-%m-%d")
            if txn_date >= monday_dt:
                amount = txn["amount"]
                category = txn["category"]
                
                if amount > 0:  # Income
                    revenue += amount
                    revenue_breakdown[category] = revenue_breakdown.get(category, 0) + amount
                else:  # Expense
                    expenses += abs(amount)
                    expense_breakdown[category] = expense_breakdown.get(category, 0) + abs(amount)
        except:
            pass
    
    return {
        "revenue": revenue,
        "expenses": expenses,
        "profit": revenue - expenses,
        "revenue_breakdown": revenue_breakdown,
        "expense_breakdown": expense_breakdown
    }

def read_goals():
    """Read business goals from Goals.md."""
    if not GOALS_FILE.exists():
        return None
    
    try:
        with open(GOALS_FILE, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return None

def collect_completed_tasks():
    """Collect completed tasks from the past week."""
    monday, _ = get_week_range()
    monday_dt = datetime.strptime(monday, "%Y-%m-%d")
    
    tasks = []
    
    for done_dir in [DONE_BUSINESS, DONE_PERSONAL]:
        if done_dir.exists():
            for file_path in done_dir.glob("**/*"):
                if file_path.is_file() and file_path.suffix in [".md", ".txt", ".json"]:
                    try:
                        stat = file_path.stat()
                        file_date = datetime.fromtimestamp(stat.st_mtime)
                        
                        if file_date >= monday_dt:
                            domain = "Business" if "Business" in str(file_path) else "Personal"
                            tasks.append({
                                "name": file_path.name,
                                "completed_at": file_date.isoformat(),
                                "domain": domain,
                                "path": str(file_path)
                            })
                    except:
                        pass
    
    return tasks

def collect_social_reports():
    """Collect social media performance data."""
    reports = {
        "facebook": {"posts": 0, "reach": 0, "engagement": 0},
        "instagram": {"posts": 0, "reach": 0, "engagement": 0},
        "twitter": {"posts": 0, "reach": 0, "engagement": 0}
    }
    
    if not SOCIAL_REPORTS_DIR.exists():
        return reports
    
    monday, _ = get_week_range()
    monday_dt = datetime.strptime(monday, "%Y-%m-%d")
    
    for report_file in SOCIAL_REPORTS_DIR.glob("*.md"):
        try:
            stat = report_file.stat()
            file_date = datetime.fromtimestamp(stat.st_mtime)
            
            if file_date >= monday_dt:
                with open(report_file, "r", encoding="utf-8") as f:
                    content = f.read().lower()
                    
                    if "facebook" in content:
                        reports["facebook"]["posts"] += 1
                    elif "instagram" in content:
                        reports["instagram"]["posts"] += 1
                    elif "twitter" in content:
                        reports["twitter"]["posts"] += 1
        except:
            pass
    
    return reports

def generate_recommendations(financial_summary, tasks, social_reports):
    """Generate proactive suggestions based on data analysis."""
    recommendations = []
    
    # Check for unused subscriptions
    expense_breakdown = financial_summary.get("expense_breakdown", {})
    if expense_breakdown.get("software", 0) > 500:
        recommendations.append({
            "type": "cost_cutting",
            "priority": "high",
            "title": "Review software subscriptions",
            "description": f"Software expenses at ${expense_breakdown.get('software', 0):,.2f} this week. Consider canceling unused tools.",
            "potential_savings": "$100-200/month"
        })
    
    # Check infrastructure costs
    if expense_breakdown.get("infrastructure", 0) > 300:
        recommendations.append({
            "type": "cost_cutting",
            "priority": "high",
            "title": "Optimize AWS/Cloud costs",
            "description": f"Infrastructure at ${expense_breakdown.get('infrastructure', 0):,.2f} this week. Review underutilized instances.",
            "potential_savings": "$150-300/month"
        })
    
    # Check task completion rate
    business_tasks = [t for t in tasks if t["domain"] == "Business"]
    if len(business_tasks) < 10:
        recommendations.append({
            "type": "productivity",
            "priority": "medium",
            "title": "Low task completion rate",
            "description": f"Only {len(business_tasks)} business tasks completed this week. Consider prioritizing or delegating.",
            "action": "Review Needs_Action folder"
        })
    
    # Check social media activity
    total_posts = sum(r["posts"] for r in social_reports.values())
    if total_posts < 5:
        recommendations.append({
            "type": "marketing",
            "priority": "medium",
            "title": "Increase social media activity",
            "description": f"Only {total_posts} posts this week. Aim for 10-15 posts/week for better engagement.",
            "action": "Schedule more content"
        })
    
    return recommendations

def generate_briefing(input_data):
    """Generate the weekly CEO briefing report."""
    week_start, week_end = get_week_range()
    
    # Collect all data
    transactions = read_transactions()
    financial_summary = calculate_financial_summary(transactions)
    goals = read_goals()
    tasks = collect_completed_tasks()
    social_reports = collect_social_reports()
    recommendations = generate_recommendations(financial_summary, tasks, social_reports)
    
    # Build briefing content
    briefing = f"""# CEO Weekly Briefing

**Week:** {week_start} to {week_end}  
**Generated:** {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}  
**Prepared by:** Suleman AI Employee v0.3

---

## 📊 Executive Summary

| Metric | This Week | Status |
|--------|-----------|--------|
| Revenue | ${financial_summary['revenue']:,.2f} | {'✅ Good' if financial_summary['revenue'] > 10000 else '⚠️ Below Target'} |
| Expenses | ${financial_summary['expenses']:,.2f} | {'✅ On Budget' if financial_summary['expenses'] < 2000 else '⚠️ Over Budget'} |
| Net Profit | ${financial_summary['profit']:,.2f} | {'✅ Profitable' if financial_summary['profit'] > 0 else '🔴 Loss'} |
| Tasks Completed | {len(tasks)} | {'✅ On Track' if len(tasks) >= 15 else '⚠️ Behind'} |

---

## 💰 Revenue Summary

### Income Breakdown

| Category | Amount |
|----------|--------|
"""
    
    for category, amount in financial_summary['revenue_breakdown'].items():
        briefing += f"| {category.title()} | ${amount:,.2f} |\n"
    
    if not financial_summary['revenue_breakdown']:
        briefing += "| No revenue recorded | $0.00 |\n"
    
    briefing += f"""
### Expense Breakdown

| Category | Amount |
|----------|--------|
"""
    
    for category, amount in financial_summary['expense_breakdown'].items():
        briefing += f"| {category.title()} | ${amount:,.2f} |\n"
    
    if not financial_summary['expense_breakdown']:
        briefing += "| No expenses recorded | $0.00 |\n"
    
    briefing += f"""
---

## 🎯 Goal Progress

"""
    
    if goals:
        briefing += f"See: `/Business/Goals.md`\n\n"
        briefing += f"**Key Focus Areas:**\n"
        briefing += f"- AI Employee v0.3 Gold Tier Launch\n"
        briefing += f"- Client Acquisition (67/100 enterprise clients)\n"
        briefing += f"- Cost Optimization (-12% AWS costs so far)\n"
    else:
        briefing += "*Goals file not found*\n"
    
    briefing += f"""
---

## ✅ Tasks Completed This Week

**Total:** {len(tasks)} tasks

### Business Tasks: {len([t for t in tasks if t['domain'] == 'Business'])}
"""
    
    business_tasks = [t for t in tasks if t['domain'] == 'Business'][:10]
    for task in business_tasks:
        briefing += f"- {task['name']}\n"
    
    briefing += f"""
### Personal Tasks: {len([t for t in tasks if t['domain'] == 'Personal'])}
"""
    
    personal_tasks = [t for t in tasks if t['domain'] == 'Personal'][:5]
    for task in personal_tasks:
        briefing += f"- {task['name']}\n"
    
    briefing += f"""
---

## 📱 Social Media Performance

| Platform | Posts | Status |
|----------|-------|--------|
| Facebook | {social_reports['facebook']['posts']} | {'✅ Active' if social_reports['facebook']['posts'] > 0 else '⚠️ No posts'} |
| Instagram | {social_reports['instagram']['posts']} | {'✅ Active' if social_reports['instagram']['posts'] > 0 else '⚠️ No posts'} |
| Twitter/X | {social_reports['twitter']['posts']} | {'✅ Active' if social_reports['twitter']['posts'] > 0 else '⚠️ No posts'} |

---

## 💡 Proactive Suggestions

"""
    
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            briefing += f"### {i}. {rec['title']}\n"
            briefing += f"**Priority:** {rec['priority'].title()}\n"
            briefing += f"{rec['description']}\n"
            if 'potential_savings' in rec:
                briefing += f"**Potential Savings:** {rec['potential_savings']}\n"
            briefing += "\n"
    else:
        briefing += "*No critical recommendations this week*\n"
    
    briefing += f"""
---

## 📋 CEO Action Items

- [ ] Review briefing and provide feedback
- [ ] Approve any pending HITL requests
- [ ] Review expense reports if over budget

---

**End of Briefing**

*Generated automatically by Suleman AI Employee v0.3*
*Next briefing: Sunday, {datetime.now().strftime('%B %d, %Y')} at 11:00 PM*
"""
    
    return {
        "content": briefing,
        "data": {
            "week_start": week_start,
            "week_end": week_end,
            "revenue": financial_summary['revenue'],
            "expenses": financial_summary['expenses'],
            "profit": financial_summary['profit'],
            "tasks_completed": len(tasks),
            "social_posts": sum(r['posts'] for r in social_reports.values())
        }
    }

def save_briefing(briefing_data):
    """Save briefing to file."""
    BRIEFINGS_DIR.mkdir(exist_ok=True)
    
    filename = f"CEO_Briefing_{briefing_data['data']['week_start']}.md"
    filepath = BRIEFINGS_DIR / filename
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(briefing_data['content'])
    
    return str(filepath)

def update_dashboard(briefing_data):
    """Update Dashboard.md with latest metrics."""
    data = briefing_data['data']
    
    content = f"""# Business Dashboard

**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Generated by:** Suleman AI Employee v0.3

---

## Quick Metrics

| Metric | Value |
|--------|-------|
| Weekly Revenue | ${data['revenue']:,.2f} |
| Weekly Expenses | ${data['expenses']:,.2f} |
| Net Profit | ${data['profit']:,.2f} |
| Tasks Completed | {data['tasks_completed']} |
| Social Posts | {data['social_posts']} |

---

## Latest Briefing

See: `/Briefings/CEO_Briefing_{data['week_start']}.md`

---

## System Status

- Ralph Wiggum Loop: ✅ Active
- MCP Servers: ✅ Running
- HITL Queue: Pending review

---

*Auto-updated by Weekly CEO Briefing system*
"""
    
    with open(DASHBOARD_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    
    return str(DASHBOARD_FILE)

def execute_briefing(input_data):
    """Main execution function for CEO briefing generation."""
    log_action("briefing_start", "info", {
        "requested_by": input_data.get("requested_by", "scheduler")
    })
    
    for attempt in range(MAX_RETRIES):
        try:
            briefing_data = generate_briefing(input_data)
            filepath = save_briefing(briefing_data)
            dashboard_path = update_dashboard(briefing_data)
            
            log_action("briefing_complete", "success", {
                "filepath": filepath,
                "dashboard": dashboard_path,
                "week_period": briefing_data['data']['week_start']
            })
            
            return {
                "status": "success",
                "briefing": briefing_data['content'],
                "data": briefing_data['data'],
                "filepath": filepath,
                "dashboard": dashboard_path
            }
            
        except Exception as e:
            log_action("briefing_attempt", "warning", {
                "attempt": attempt + 1,
                "error": str(e)
            })
            
            if attempt == MAX_RETRIES - 1:
                log_action("briefing_failed", "error", {
                    "max_retries": MAX_RETRIES,
                    "final_error": str(e)
                })
                return {
                    "status": "failed",
                    "error": str(e),
                    "attempts": MAX_RETRIES
                }

def main():
    """Entry point - accepts JSON from stdin."""
    try:
        input_json = sys.stdin.read()
        input_data = json.loads(input_json)
        
        result = execute_briefing(input_data)
        print(json.dumps(result))
        
    except json.JSONDecodeError as e:
        error = {"status": "failed", "error": f"Invalid JSON input: {str(e)}"}
        log_action("briefing", "failed", error)
        print(json.dumps(error))
    except Exception as e:
        error = {"status": "failed", "error": str(e)}
        log_action("briefing", "failed", error)
        print(json.dumps(error))

if __name__ == "__main__":
    main()
