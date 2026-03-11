# SKILL: Facebook & Instagram Auto-Post

**Version:** 0.3 Gold Tier - Phase 5
**Tier:** Gold
**Owner:** Suleman AI Employee v0.3
**Platforms:** Facebook, Instagram
**HITL Required:** ✅ Yes (always for public posts)

---

## Objective

Generate professional captions and post to Facebook and/or Instagram with HITL approval.

---

## Error Handling & Logging

**Wrap all actions with error_recovery_mcp.py:**

```bash
# On error, retry with exponential backoff
echo '{"action_type": "retry_with_backoff", "params": {...}, "max_retries": 3}' | python MCP/error_recovery/error_recovery_mcp.py
```

**Log every step to audit JSON:**
- Every post attempt logged to `/Logs/audit_YYYY-MM-DD.json`
- Format: `{"timestamp": "...", "action": "post_facebook", "status": "success/failed", "domain": "Business"}`

**On critical fail:** Create `ERROR_ALERT` file in `Pending_Approval/`

---

## MCP Integration

**After HITL approval, call social_mcp.py:**

```bash
# Facebook only
echo '{"action": "post_facebook", "message": "Your post content here", "media_path": "/path/to/image.jpg"}' | python MCP/social/social_mcp.py

# Instagram only
echo '{"action": "post_instagram", "message": "Your post content here", "media_path": "/path/to/image.jpg"}' | python MCP/social/social_mcp.py

# Both platforms (separate calls)
echo '{"action": "post_facebook", "message": "...", "media_path": "..."}' | python MCP/social/social_mcp.py
echo '{"action": "post_instagram", "message": "...", "media_path": "..."}' | python MCP/social/social_mcp.py
```

**Response:**
```json
{
    "status": "success",
    "platform": "facebook",
    "url": "https://facebook.com/posts/..."
}
```

---

## Steps

### 1. Generate Professional Caption

**Requirements:**
- Facebook: <300 characters optimal, hashtags at end
- Instagram: 150-200 characters, 5-10 hashtags

**Template:**
```
🎯 [Engaging headline with emoji]

[Main content - 2-3 sentences]

✅ [Call-to-action or key benefit]

#Hashtag1 #Hashtag2 #Hashtag3
```

### 2. Create HITL Approval Request

**Always create Pending_Approval file first:**

```markdown
---
type: approval_request
action: post_social
platforms: ["facebook", "instagram"]
created: 2026-03-04T12:00:00
status: pending
---

## Post Details

**Message:**
[Full post content here]

**Media:**
/path/to/image.jpg (or "none")

**Reason:**
[Why this post is being created]

**Expected Reach:**
High/Medium/Low

---
**Move to Approved/ to post, Rejected/ to cancel**
```

### 3. Wait for Approval

- File stays in `Pending_Approval/` until human reviews
- Move to `Approved/` = post immediately
- Move to `Rejected/` = cancel and log reason

### 4. Execute Post via MCP

After approval:
```bash
echo '{"action": "post_facebook", "message": "...", "media_path": "..."}' | python MCP/social/social_mcp.py
```

### 5. Generate Summary Report

Save to `/Business/Social_Reports/`:

```markdown
# Social Post Report

**Platform:** Facebook
**Posted:** 2026-03-04 15:30:00
**Domain:** Business

## Content
[Full post content]

## Performance
- Status: ✅ Posted successfully
- Session: Saved
- Audit Log: `/Logs/audit_2026-03-04.json`

## Expected Engagement
- Likes: Medium (10-50 estimated)
- Comments: Low (2-5 estimated)
- Shares: Low-Medium
```

---

## Session Management

**Persistent Session Folders:**
- `/facebook_session/` - Facebook auth cookies
- `/instagram_session/` - Instagram auth cookies

**First Time Setup:**
1. Run the MCP script
2. Browser opens automatically
3. Login manually when prompted
4. Session saved for future use

---

## Human-Like Behavior

| Action | Delay |
|--------|-------|
| Page load | 2-5 seconds |
| Typing | 50-150ms per char |
| Before click | 1-3 seconds |
| After post | 3-8 seconds |
| Mouse movement | Random throughout |

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Session expired | Browser opens, wait for manual login |
| Post failed | Retry with error_recovery_mcp.py |
| Rate limited | Wait 15 minutes, retry |
| Media upload failed | Post text-only, log warning |

---

## Related Skills

- `SKILL_TwitterPost.md` – Twitter/X posting
- `SKILL_ErrorRecovery.md` – Retry logic
- `SKILL_SocialSummaryGenerator.md` – Post summaries
- `SKILL_CrossDomainRouter.md` – Domain routing

---

**Status:** ✅ Active  
**Last Updated:** 2026-03-04
