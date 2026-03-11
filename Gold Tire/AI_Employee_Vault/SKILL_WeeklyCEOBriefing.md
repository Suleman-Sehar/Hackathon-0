# SKILL: Weekly CEO Briefing

**Version:** 0.3 Gold Tier - Phase 5
**Owner:** Suleman AI Employee v0.3
**Schedule:** Every Sunday 11 PM PKT

---

## Objective

Generate comprehensive Monday Morning CEO Briefing every Sunday at 11 PM with revenue/expenses analysis, bottlenecks, social performance, and proactive suggestions.

---

## Error Handling & Logging

**Wrap all actions with error_recovery_mcp.py:**

```bash
# On briefing generation error
echo '{"action_type": "retry_with_backoff", "params": {...}, "max_retries": 3}' | python MCP/error_recovery/error_recovery_mcp.py
```

**Log every step to audit JSON:**
- Briefing generation logged to `/Logs/audit_YYYY-MM-DD.json`
- Format: `{"timestamp": "...", "action": "ceo_briefing_generated", "status": "success/failed", "domain": "Business"}`

**On critical fail:** Create `ERROR_ALERT` file in `Pending_Approval/`

---

## Trigger

- **Scheduled:** Every Sunday 11 PM PKT (via Windows Task Scheduler or cron)
- **Manual:** `echo '{}' | python MCP/briefing/briefing_mcp.py`
- **Autonomous:** Via Ralph Wiggum orchestrator as recurring task

---

## Data Sources

| Source | Location | Data Extracted |
|--------|----------|----------------|
| Transactions | `/Accounting/transactions.csv` | Last 7 days revenue/expenses |
| Completed Tasks | `/Business/Done/Business/` | Tasks completed this week |
| Social Reports | `/Business/Social_Reports/` | Post performance metrics |
| Goals | `/Business/Goals.md` | Goal progress tracking |

---

## Output File

**Location:** `/Briefings/CEO_Briefing_YYYY-MM-DD.md`

**Example:** `/Briefings/CEO_Briefing_2026-03-04.md`

---

## Briefing Sections

### 1. Executive Summary
- Total Revenue (PKR)
- Total Expenses (PKR)
- Net Profit (PKR)
- Tasks Completed (count)
- Social Posts (count)

### 2. Revenue & Expenses
- Revenue breakdown by category
- Expense breakdown by category
- Comparison with previous week
- Flagged transactions (>10,000 PKR or pending)

### 3. Completed Tasks & Bottlenecks
- List of tasks completed this week
- Tasks that took >3 iterations (potential bottlenecks)
- Tasks requiring CEO attention

### 4. Social Performance
- Posts on Facebook, Instagram, Twitter/X
- Expected reach per platform
- Best performing content
- Engagement estimates

### 5. Proactive Suggestions
- Cost-cutting opportunities (e.g., "Cancel Adobe – no usage in 30 days")
- Process improvements
- Revenue optimization ideas
- Risk mitigation suggestions

### 6. Next Week Priorities
- Top 3 priorities for next week
- Deadlines approaching
- Resource requirements

---

## Generation Logic

```python
def generate_briefing():
    # 1. Read transactions from last 7 days
    transactions = read_transactions(days=7)
    
    # 2. Calculate totals
    revenue = sum(t.amount for t in transactions if t.amount > 0)
    expenses = sum(abs(t.amount) for t in transactions if t.amount < 0)
    net = revenue - expenses
    
    # 3. Count completed tasks
    tasks = count_completed_tasks(days=7)
    
    # 4. Aggregate social reports
    social = aggregate_social_posts(days=7)
    
    # 5. Generate suggestions
    suggestions = generate_suggestions(transactions, tasks, social)
    
    # 6. Format and save briefing
    briefing = format_briefing(revenue, expenses, net, tasks, social, suggestions)
    save_briefing(briefing)
    
    # 7. Update dashboard
    update_dashboard(briefing)
    
    # 8. Log action
    log_action("ceo_briefing_generated", "success")
```

---

## Sample Output

```markdown
# CEO Weekly Briefing

**Week:** 2026-02-26 to 2026-03-04
**Generated:** 2026-03-04 11:00 PM PKT
**Prepared by:** Suleman AI Employee v0.3 Gold Tier

---

## Executive Summary

| Metric | This Week | Last Week | Change |
|--------|-----------|-----------|--------|
| Revenue | PKR 157,000 | PKR 120,000 | +31% |
| Expenses | PKR 13,799 | PKR 15,000 | -8% |
| Net Profit | PKR 143,201 | PKR 105,000 | +36% |
| Tasks Completed | 12 | 8 | +50% |

---

## Revenue Breakdown

| Category | Amount |
|----------|--------|
| Client Invoices | PKR 120,000 |
| Freelance | PKR 12,000 |
| Product Sales | PKR 25,000 |

---

## Expense Breakdown

| Category | Amount |
|----------|--------|
| Subscriptions | PKR 2,999 |
| Marketing | PKR 5,000 |
| Cloud Services | PKR 1,500 |
| Office | PKR 3,500 |
| Fees | PKR 800 |

### Flagged for Review
- Adobe Subscription (PKR 2,999) - Pending status
- Bank Fee (PKR 0) - Pending status

---

## Social Performance

| Platform | Posts | Expected Reach |
|----------|-------|----------------|
| Instagram | 2 | 300+ |
| Twitter | 2 | 200+ |

---

## Proactive Suggestions

1. **Cancel Adobe Subscription** – No usage detected in 30 days (Save PKR 2,999/month)
2. **Review Bank Fees** – Multiple pending fee transactions
3. **Increase Twitter Activity** – Only 2 posts this week, aim for 5+

---

## Next Week Priorities

1. Complete Gold Tier Phase 5
2. Follow up on pending invoices
3. Review and approve flagged expenses

---

**End of Briefing**
```

---

## Integration

### With Ralph Wiggum Loop

Weekly briefing is a **recurring autonomous task**:

```bash
# Trigger via orchestrator every Sunday
python Ralph_Wiggum/orchestrator.py Needs_Action/Business/WEEKLY_BRIEFING.md
```

### With MCP

```bash
# Direct MCP call
echo '{}' | python MCP/briefing/briefing_mcp.py
```

---

## Error Handling

| Error | Recovery |
|-------|----------|
| transactions.csv missing | Generate briefing without financial data, flag warning |
| No tasks completed | Note "No tasks completed this week" |
| Social reports missing | Skip social section, continue |
| Briefing generation fails | Retry 3 times, alert CEO via email |

---

## Related Skills

- `SKILL_ErrorRecovery.md` – Retry logic
- `SKILL_RalphWiggumLoop.md` – Autonomous scheduling
- `SKILL_SocialSummaryGenerator.md` – Social data

---

**Status:** ✅ Active  
**Last Updated:** 2026-03-04  
**Next Scheduled Run:** Sunday 11 PM PKT
