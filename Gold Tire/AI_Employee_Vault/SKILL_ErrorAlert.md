# SKILL: Error Alert

**Version:** 0.3 Gold Tier - Phase 5
**Owner:** Suleman AI Employee v0.3

---

## Objective

Notify humans on unrecoverable errors that require manual intervention.

---

## When to Use

Create an ERROR_ALERT file when:
- All retry attempts exhausted (max 3 retries)
- Critical system failure detected
- Data corruption possible
- Security concern identified
- Financial transaction failed

---

## Error Alert Format

**Location:** `/Pending_Approval/ERROR_ALERT_{action}_{timestamp}.md`

**Template:**
```markdown
---
type: error_alert
created: 2026-03-04T12:30:00+05:00
status: critical
---

## Error Details

- **Action:** post_instagram
- **Error:** Session expired, all retries exhausted
- **Domain:** Business
- **Iterations:** 3 (max_retries: 3)
- **Original Input:**
  ```json
  {
    "action": "post_instagram",
    "message": "Test post",
    "media_path": "/path/to/image.jpg"
  }
  ```

## Stack Trace

```
Traceback (most recent call last):
  File "MCP/social/social_mcp.py", line 123, in post_instagram
    raise SessionExpiredError("Instagram session expired")
SessionExpiredError: Instagram session expired
```

## Required Actions

- [ ] Review error cause
- [ ] Re-authenticate to Instagram if needed
- [ ] Re-run action manually or approve retry
- [ ] Update this file with resolution

---

**Assigned To:** System Administrator  
**Priority:** High  
**Created:** 2026-03-04T12:30:00+05:00

**Resolution:**
[Fill after review]

**Resolved At:** _______________
```

---

## Creation Logic

```python
def create_error_alert(action: str, error: str, params: Dict, attempt: int):
    """Create an error alert file for human review."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    alert_file = PENDING_APPROVAL_DIR / f"ERROR_ALERT_{action}_{timestamp}.md"
    
    content = f"""---
type: error_alert
created: {datetime.now().isoformat()}
status: critical
---

## Error Details

- **Action:** {action}
- **Error:** {error}
- **Domain:** {params.get('domain', 'Unknown')}
- **Iterations:** {attempt} (max_retries: {params.get('max_retries', 3)})

## Original Input

```json
{json.dumps(params, indent=2)}
```

## Required Actions

- [ ] Review error cause
- [ ] Fix underlying issue
- [ ] Re-run action manually or approve retry
- [ ] Update this file with resolution

---

**Assigned To:** System Administrator  
**Priority:** High
"""
    
    with open(alert_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    # Log alert creation
    log_action("error_alert_created", "warning", {
        "file": str(alert_file),
        "action": action
    })
    
    return str(alert_file)
```

---

## Alert Processing

### Human Review Flow

1. **Alert Created** → File appears in `/Pending_Approval/`
2. **Human Reviews** → Opens file, reads error details
3. **Human Acts:**
   - Fix issue (re-authenticate, etc.)
   - Re-run action manually
   - Approve retry with modified params
4. **Resolution** → Update file with resolution, move to `/Done/`

### Alert Status

| Status | Meaning |
|--------|---------|
| `critical` | Immediate attention required |
| `high` | Review within 24 hours |
| `medium` | Review within 1 week |

---

## Integration with Error Recovery

**Called automatically when all retries fail:**

```python
# In error_recovery_mcp.py
if attempt >= max_retries:
    # All retries exhausted - create human alert
    alert_file = create_error_alert(
        action=action_name,
        error=str(last_error),
        params=params,
        attempt=max_retries
    )
    
    return {
        "status": "failed",
        "error": str(last_error),
        "alert_file": alert_file
    }
```

---

## Examples

### Example 1: Social Post Failure

**File:** `/Pending_Approval/ERROR_ALERT_post_instagram_20260304_123000.md`

```markdown
---
type: error_alert
created: 2026-03-04T12:30:00+05:00
status: critical
---

## Error Details

- **Action:** post_instagram
- **Error:** Session expired, all retries exhausted
- **Domain:** Business
- **Iterations:** 3

## Required Actions

- [ ] Re-authenticate to Instagram
- [ ] Re-run post manually

---

**Priority:** High
```

### Example 2: Briefing Generation Failure

**File:** `/Pending_Approval/ERROR_ALERT_briefing_generation_20260304_230000.md`

```markdown
---
type: error_alert
created: 2026-03-04T23:00:00+05:00
status: critical
---

## Error Details

- **Action:** briefing_generation
- **Error:** transactions.csv not found
- **Domain:** Business
- **Iterations:** 3

## Required Actions

- [ ] Check if transactions.csv exists
- [ ] Restore from backup if corrupted
- [ ] Re-run briefing generation

---

**Priority:** High (Sunday 11 PM - briefing deadline)
```

---

## Monitoring

### View Pending Alerts

```bash
# List all pending error alerts
dir Pending_Approval\ERROR_ALERT_*.md
```

### Alert Statistics

```python
def get_alert_stats():
    """Get statistics on error alerts."""
    alerts = list(PENDING_APPROVAL_DIR.glob("ERROR_ALERT_*.md"))
    
    by_action = {}
    by_priority = {"critical": 0, "high": 0, "medium": 0}
    
    for alert in alerts:
        content = alert.read_text()
        # Parse action and priority from content
        # ...
    
    return {
        "total_pending": len(alerts),
        "by_action": by_action,
        "by_priority": by_priority
    }
```

---

## Related Skills

- `SKILL_ErrorRecovery.md` – Retry logic before alerting
- `SKILL_RalphWiggumLoop.md` – Loop error handling
- `SKILL_WeeklyCEOBriefing.md` – Briefing failure alerts

---

**Status:** ✅ Active  
**Last Updated:** 2026-03-04
