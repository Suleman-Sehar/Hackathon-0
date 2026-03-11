# SKILL: Twitter (X) Auto-Post

**Version:** 0.3 Gold Tier - Phase 5
**Tier:** Gold
**Owner:** Suleman AI Employee v0.3
**Platform:** Twitter / X
**HITL Required:** ✅ Yes (always for public posts)

---

## Error Handling & Logging

**Wrap all actions with error_recovery_mcp.py:**

```bash
# On error, retry with exponential backoff (2s, 8s, 32s)
echo '{"action_type": "retry_with_backoff", "params": {...}, "max_retries": 3}' | python MCP/error_recovery/error_recovery_mcp.py
```

**Log every step to audit JSON:**
- Every tweet attempt logged to `/Logs/audit_YYYY-MM-DD.json`
- Format: `{"timestamp": "...", "action": "post_twitter", "status": "success/failed", "domain": "Business"}`

**On critical fail:** Create `ERROR_ALERT` file in `Pending_Approval/`

---

## MCP Integration

**After HITL approval, call social_mcp.py:**

```bash
echo '{"action": "post_twitter", "message": "Your tweet content here (max 280 chars)", "media_path": "/path/to/image.jpg"}' | python MCP/social/social_mcp.py
```

**Response:**
```json
{
    "status": "success",
    "platform": "twitter",
    "url": "https://twitter.com/status/..."
}
```

---

## Objective

Generate professional tweets and post to Twitter (X) with HITL approval.

---

## Steps

### 1. Generate Tweet Content

**Requirements:**
- Max 280 characters (strict for free accounts)
- 1-3 relevant hashtags
- 2-3 emojis max
- Engaging hook in first line

**Template:**
```
🎯 [Hook/headline]

[Main message - concise]

#Hashtag1 #Hashtag2
```

### 2. Create HITL Approval Request

**Create Pending_Approval file:**

```markdown
---
type: approval_request
action: post_twitter
platforms: ["twitter"]
created: 2026-03-04T12:00:00
status: pending
---

## Tweet Details

**Content:**
[Tweet text - max 280 chars]

**Media:**
/path/to/image.jpg (or "none")

**Reason:**
[Why this tweet is being created]

**Character Count:**
[XX]/280

---
**Move to Approved/ to post, Rejected/ to cancel**
```

### 3. Wait for Approval

- File stays in `Pending_Approval/`
- Move to `Approved/` = post immediately
- Move to `Rejected/` = cancel

### 4. Execute Post via MCP

```bash
echo '{"action": "post_twitter", "message": "...", "media_path": "..."}' | python MCP/social/social_mcp.py
```

### 5. Generate Summary Report

Save to `/Business/Social_Reports/`:

```markdown
# Twitter Post Report

**Posted:** 2026-03-04 15:30:00
**Domain:** Business
**Tweet URL:** https://twitter.com/status/...

## Content
[Full tweet]

## Performance
- Status: ✅ Posted successfully
- Session: Saved
- Audit Log: `/Logs/audit_2026-03-04.json`

## Expected Engagement
- Retweets: Low-Medium (5-20)
- Likes: Medium (20-100)
- Replies: Low (2-10)
```

---

## Thread Support

For longer content (>280 chars), auto-generate threads:

```python
def create_thread(long_content, max_chars=260):
    """Split into threaded tweets."""
    words = long_content.split()
    parts = []
    current = ""
    
    for word in words:
        if len(current) + len(word) + 1 < max_chars:
            current += " " + word if current else word
        else:
            parts.append(current.strip())
            current = word
    
    if current:
        parts.append(current.strip())
    
    # Add thread markers
    total = len(parts)
    for i in range(total):
        parts[i] = f"({i+1}/{total}) {parts[i]}"
    
    return parts
```

---

## Session Management

**Persistent Session Folder:**
- `/twitter_session/` - Twitter auth cookies

**First Time:**
1. Run MCP script
2. Browser opens
3. Login when prompted
4. Session saved

---

## Human-Like Behavior

| Action | Delay |
|--------|-------|
| Page load | 2-5 seconds |
| Typing | 50-150ms per char |
| Before click | 1-3 seconds |
| After tweet | 3-8 seconds |

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Session expired | Manual login prompt |
| Tweet failed | Retry with error_recovery_mcp.py |
| Rate limited | Wait 1 hour, retry |
| Duplicate content | Modify text, retry |
| Too long | Auto-truncate to 277 + "..." |

---

## Best Practices

### Content
- Use 1-3 hashtags (not more)
- Include 2-3 emojis max
- Tag relevant accounts when appropriate
- Add images for 2x engagement

### Timing
- Business: 9 AM - 5 PM weekdays
- Personal: Evenings, weekends
- Avoid major news events

---

## Related Skills

- `SKILL_FacebookInstagramPost.md` – FB/IG posting
- `SKILL_ErrorRecovery.md` – Retry logic
- `SKILL_SocialSummaryGenerator.md` – Post summaries

---

**Status:** ✅ Active  
**Last Updated:** 2026-03-04
