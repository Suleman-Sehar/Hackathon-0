# SKILL: Error Recovery

**Version:** 0.3 Gold Tier - Phase 5
**Owner:** Suleman AI Employee v0.3

---

## Objective

Handle failures gracefully with retry logic, exponential backoff, graceful degradation, and comprehensive logging to ensure system reliability.

---

## Core Principles

1. **Never crash silently** – Every error is logged
2. **Always try to recover** – Retry with exponential backoff
3. **Degrade gracefully** – If one service fails, try alternatives
4. **Document everything** – All actions logged to audit files

---

## Error Handling & Logging

**Wrap all actions with error_recovery_mcp.py:**

```bash
# Retry a failed function
echo '{"action_type": "retry_with_backoff", "params": {...}, "max_retries": 3}' | python MCP/error_recovery/error_recovery_mcp.py
```

**Log every step to audit JSON:**
- Every error logged to `/Logs/audit_YYYY-MM-DD.json`
- Format: `{"timestamp": "...", "action": "error_recovery", "status": "retry/failed", "domain": "Business"}`

**On critical fail:** Create `ERROR_ALERT` file in `Pending_Approval/`

---

## MCP Error Recovery Servers

### 1. `mcp/error_recovery_mcp.py`

**Purpose:** Central retry logic and graceful degradation handler.

**Usage:**
```python
import subprocess
import json

# Retry a failed function
input_data = {
    "action_type": "retry_with_backoff",
    "params": {"arg1": "value1"},
    "max_retries": 3
}

result = subprocess.run(
    ["python", "MCP/error_recovery/error_recovery_mcp.py"],
    input=json.dumps(input_data),
    capture_output=True,
    text=True
)
response = json.loads(result.stdout)
```

**Input Schema:**
```json
{
    "action_type": "retry_with_backoff|graceful_degradation|log_and_alert",
    "params": {},
    "fallback_services": [],
    "available_services": {}
}
```

**Output Schema:**
```json
{
    "success": true,
    "result": {},
    "attempts": 2,
    "error": null
}
```

---

### 2. `mcp/social_mcp.py`

**Purpose:** Social media posting with built-in retry for Facebook, Instagram, Twitter (X).

**Usage:**
```python
input_data = {
    "action": "post_twitter",
    "content": "Hello world!",
    "image_path": "/path/to/image.jpg",
    "domain": "Business"
}

result = subprocess.run(
    ["python", "MCP/social/social_mcp.py"],
    input=json.dumps(input_data),
    capture_output=True,
    text=True
)
```

**Retry Behavior:**
- Max 3 retries per platform
- Exponential backoff: 2s, 8s, 32s
- Session persistence (saves login state)
- Logs every attempt to `/Logs/audit_YYYY-MM-DD.json`

---

### 3. `mcp/briefing_mcp.py`

**Purpose:** Weekly CEO Briefing generation with retry on failure.

**Usage:**
```python
input_data = {
    "requested_by": "scheduler",
    "week_offset": 0
}

result = subprocess.run(
    ["python", "MCP/briefing/briefing_mcp.py"],
    input=json.dumps(input_data),
    capture_output=True,
    text=True
)
```

**Output:**
- Markdown briefing saved to `/Briefings/CEO_Briefing_YYYY-MM-DD.md`
- JSON response with summary stats

---

## Retry Logic

### Exponential Backoff Formula

```
delay = BASE_DELAY * (4 ^ attempt)

Attempt 0: Immediate
Attempt 1: +2 seconds
Attempt 2: +8 seconds
Attempt 3: +32 seconds
```

### Configuration

```python
MAX_RETRIES = 3
BASE_DELAY = 2  # seconds
```

### When to Retry

| Error Type | Retry? | Max Attempts | Backoff |
|------------|--------|--------------|---------|
| Network timeout | ✅ Yes | 3 | Exponential |
| Session expired | ✅ Yes | 3 | Exponential |
| Rate limit (429) | ✅ Yes | 3 | Extended (15min) |
| API unavailable (5xx) | ✅ Yes | 3 | Exponential |
| Invalid input (4xx) | ❌ No | 0 | N/A |
| File not found | ❌ No | 0 | N/A |
| Permission denied | ❌ No | 0 | N/A |

---

## Graceful Degradation

### Multi-Platform Social Posting

If posting to multiple platforms and one fails:

```python
# Input
platforms = ["facebook", "instagram", "twitter"]

# Scenario: Facebook fails, Instagram succeeds, Twitter fails
# Result: Partial success
{
    "status": "partial_success",
    "successful_platforms": ["instagram"],
    "failed_platforms": ["facebook", "twitter"],
    "results": {
        "facebook": {"status": "failed", "error": "..."},
        "instagram": {"status": "success", "result": {...}},
        "twitter": {"status": "failed", "error": "..."}
    }
}
```

### Fallback Service Chain

```python
input_data = {
    "action_type": "graceful_degradation",
    "primary_service": "twitter",
    "fallback_services": ["linkedin", "email"],
    "available_services": {
        "twitter": post_twitter,
        "linkedin": post_linkedin,
        "email": send_email
    }
}
```

**Flow:**
1. Try primary service (Twitter)
2. If fails, try fallback #1 (LinkedIn)
3. If fails, try fallback #2 (Email)
4. Return aggregated results if all fail

---

## Comprehensive Logging

### Audit Log Format

**Location:** `/Logs/audit_YYYY-MM-DD.json`

**Entry Structure:**
```json
{
    "timestamp": "2026-03-04T15:30:00.123456",
    "action": "social_post",
    "status": "success",
    "details": {
        "platform": "twitter",
        "domain": "Business",
        "content_length": 140
    },
    "error": null
}
```

### Log Levels

| Status | Severity | Description |
|--------|----------|-------------|
| `info` | Low | Normal operation |
| `success` | Low | Action completed successfully |
| `warning` | Medium | Recoverable issue, retry attempted |
| `error` | High | Failure, may retry |
| `failed` | Critical | All retries exhausted |

---

## Error Codes

| Code | Error | Recovery Action |
|------|-------|-----------------|
| E001 | JSON parse error | Fix input format |
| E002 | Session expired | Re-authenticate via browser |
| E003 | Rate limited | Wait 15 minutes, retry |
| E004 | Network timeout | Retry with exponential backoff |
| E005 | File not found | Check path, create if needed |
| E006 | Permission denied | Check file permissions |
| E007 | All retries exhausted | Manual review required |
| E008 | API unavailable | Wait and retry, check service status |
| E009 | Invalid credentials | Update credentials, re-authenticate |
| E010 | Resource not found | Verify resource exists |

---

## Integration Patterns

### Ralph Wiggum Loop Integration

```python
loop_state = {
    "task": "post_to_all_platforms",
    "error_handler": "mcp/error_recovery_mcp.py",
    "retry_on_failure": True,
    "max_retries": 3,
    "graceful_degradation": True
}
```

### Try/Except Pattern

```python
for attempt in range(MAX_RETRIES):
    try:
        result = execute_action()
        if result.success:
            log_action("success", result)
            break
    except Exception as e:
        log_action("retry", {"attempt": attempt, "error": str(e)})
        if attempt == MAX_RETRIES - 1:
            log_action("failed", {"error": str(e)})
            raise
        time.sleep(BASE_DELAY * (4 ** attempt))
```

### Graceful Degradation Pattern

```python
results = {}
for service in service_chain:
    try:
        result = call_service(service)
        results[service] = {"status": "success", "result": result}
        break  # Stop on first success
    except Exception as e:
        results[service] = {"status": "failed", "error": str(e)}
        continue  # Try next service

# Return partial success if any succeeded
if any(r["status"] == "success" for r in results.values()):
    return {"status": "partial_success", "results": results}
else:
    return {"status": "failed", "results": results}
```

---

## Manual Recovery Commands

### Trigger Retry
```bash
echo '{"action_type": "retry_with_backoff", "function": "my_task", "params": {}}' | python MCP/error_recovery/error_recovery_mcp.py
```

### Generate Briefing On-Demand
```bash
echo '{"requested_by": "manual"}' | python MCP/briefing/briefing_mcp.py
```

### Post to Social Media
```bash
echo '{"action": "post_twitter", "content": "Test"}' | python MCP/social/social_mcp.py
```

### View Today's Logs
```bash
type Logs\audit_2026-03-04.json
```

### View Errors Only
```bash
python -c "import json; logs=json.load(open('Logs/audit_2026-03-04.json')); print([l for l in logs if l['status'] in ['error','failed']])"
```

---

## Monitoring & Alerts

### Health Check Script

```python
def system_health_check():
    """Check system health based on recent logs."""
    logs = get_today_logs()
    
    errors = [l for l in logs if l['status'] in ['error', 'failed']]
    error_rate = len(errors) / max(len(logs), 1)
    
    if error_rate > 0.1:  # More than 10% errors
        return {"status": "unhealthy", "error_rate": error_rate}
    elif error_rate > 0.05:  # More than 5% errors
        return {"status": "degraded", "error_rate": error_rate}
    else:
        return {"status": "healthy", "error_rate": error_rate}
```

### Alert Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| Error rate | > 5% | > 10% |
| Failed tasks | > 3/day | > 10/day |
| API timeouts | > 5/hour | > 20/hour |
| Retry exhaustion | > 2/day | > 5/day |

---

## Related Skills

- `SKILL_CrossDomainRouter.md` – Domain-aware error handling
- `SKILL_RalphWiggumLoop.md` – Multi-step autonomy with recovery
- `SKILL_WeeklyCEOBriefing.md` – CEO briefing generation
- `SKILL_ErrorAlert.md` – Human notification on critical errors

---

**Status:** ✅ Active  
**Last Updated:** 2026-03-04
