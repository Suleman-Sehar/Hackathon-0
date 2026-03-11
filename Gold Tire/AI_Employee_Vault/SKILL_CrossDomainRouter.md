# SKILL: Cross-Domain Router

**Version:** 0.3 Gold Tier - Phase 5
**Owner:** Suleman AI Employee v0.3

---

## Objective

Route tasks to Personal or Business domain based on content keywords.
**If task is multi-step (>3 steps), route to Ralph Wiggum orchestrator.**

**Keywords → Business:**
- client, invoice, revenue, payment, contract, proposal
- meeting, presentation, report, deadline
- marketing, sales, lead, customer

**Keywords → Personal:**
- personal email, family, friend
- personal finance, personal shopping
- hobby, vacation, personal social media

**Multi-Step Indicators → Ralph Wiggum:**
- "generate... then post... create summary"
- Multiple action verbs in sequence
- Tasks requiring >3 distinct steps

---

## Error Handling & Logging

**Wrap all actions with error_recovery_mcp.py:**

```bash
# On routing error
echo '{"action_type": "retry_with_backoff", "params": {...}, "max_retries": 3}' | python MCP/error_recovery/error_recovery_mcp.py
```

**Log every step to audit JSON:**
- Every routing decision logged to `/Logs/audit_YYYY-MM-DD.json`
- Format: `{"timestamp": "...", "action": "cross_domain_routing", "status": "success/failed", "domain": "Business"}`

**On critical fail:** Create `ERROR_ALERT` file in `Pending_Approval/`

---

## Steps

1. **Read file** – Load task file from Needs_Action root
2. **Decide domain** – Analyze content for keywords
3. **Check if multi-step** – Count distinct actions/steps
4. **Route accordingly:**
   - Single-step → Move to correct Needs_Action subfolder
   - Multi-step → Send to Ralph Wiggum orchestrator
5. **Create Plan in matching Plans subfolder:**
   - Business → `/Business/Plans/Business/{task}_Plan.md`
   - Personal → `/Personal/Plans/Personal/{task}_Plan.md`

---

## Ralph Wiggum Integration

**If task is multi-step, route to Ralph Wiggum orchestrator:**

```bash
python Ralph_Wiggum/orchestrator.py /Needs_Action/{domain}/{task}.md
```

**Multi-step indicators:**
- Multiple platform posting (FB + IG + Twitter)
- Generate + Post + Summarize sequence
- Data gathering + Report + Send sequence

---

## Domain Detection Logic

```python
def detect_domain(content):
    business_keywords = ['client', 'invoice', 'business', 'revenue']
    personal_keywords = ['personal', 'family', 'friend']
    
    content_lower = content.lower()
    
    business_count = sum(1 for kw in business_keywords if kw in content_lower)
    personal_count = sum(1 for kw in personal_keywords if kw in content_lower)
    
    if business_count > personal_count:
        return "Business"
    elif personal_count > business_count:
        return "Personal"
    else:
        return "Business"  # Default to Business for ambiguous
```

---

## File Routing

| Input | Output |
|-------|--------|
| `/Needs_Action/task.md` | `/Business/Needs_Action/Business/task.md` or `/Personal/Needs_Action/Personal/task.md` |

---

## Logging

Every routing decision logged to `/Logs/audit_YYYY-MM-DD.json`:

```json
{
    "timestamp": "2026-03-04T12:00:00",
    "action": "cross_domain_routing",
    "status": "success",
    "domain": "Business",
    "details": {
        "task": "task_name",
        "keywords_found": ["client", "invoice"]
    },
    "error": null
}
```

---

## Related Skills

- `SKILL_RalphWiggumLoop.md` – Multi-step autonomy
- `SKILL_WeeklyCEOBriefing.md` – CEO reporting
- `SKILL_ErrorRecovery.md` – Error handling

---

**Status:** ✅ Active  
**Last Updated:** 2026-03-04
