# Social Media Test Trigger Prompts

**Phase 2 - FB/IG/X Integration Testing**

Use these prompts to test the social media posting system.

---

## Quick Test Prompts

### 1. Instagram + Twitter Test
```
Generate and post on Instagram and Twitter: 'Excited to launch autonomous AI Employee – 24/7 productivity boost! #AI #Automation'
```

**Expected Flow:**
1. Generate captions for both platforms
2. Create HITL approval request in Pending_Approval/
3. Wait for approval (move to Approved/)
4. Post to Instagram via MCP
5. Post to Twitter via MCP
6. Generate summary reports
7. Log to audit JSON

---

### 2. Facebook Only Test
```
Post only on Facebook: 'New feature: Ralph Wiggum loop for true autonomy'
```

**Expected Flow:**
1. Generate Facebook caption
2. Create HITL approval request
3. After approval, call social_mcp.py
4. Generate summary report

---

### 3. Multi-Platform Announcement
```
Generate posts for all platforms (FB, IG, Twitter): 'Gold Tier Phase 2 complete - Full social media automation with HITL approval! #Hackathon2026 #AI'
```

**Expected Flow:**
1. Generate platform-specific captions
2. Create single HITL request for all platforms
3. Post to each platform sequentially
4. Generate individual summaries

---

### 4. Low-Risk System Update (No HITL)
```
Post system status on Twitter: 'System status: All services operational ✅ #TechUpdate' (low_risk: true)
```

**Expected Flow:**
1. Generate tweet
2. Skip HITL (low-risk flag)
3. Post directly via MCP
4. Log action

---

## Manual Testing Steps

### Step 1: Create Test Post
```bash
# Create pending approval file
echo "---
type: approval_request
action: post_social
platforms: [\"twitter\"]
created: $(date -Iseconds)
status: pending
---

## Post Details

**Message:**
Test post from Gold Tier Phase 2 #Testing

**Media:** none

**Reason:** Phase 2 integration test

---
Move to Approved/ to post, Rejected/ to cancel" > Pending_Approval/SOCIAL_TEST_$(date +%Y%m%d_%H%M%S).md
```

### Step 2: Approve Post
```bash
# Move to Approved folder
mv Pending_Approval/SOCIAL_TEST_*.md Approved/
```

### Step 3: Execute Post
```bash
# Call MCP (example for Twitter)
echo '{"action": "post_twitter", "message": "Test post from Gold Tier Phase 2 #Testing", "media_path": null}' | python MCP/social/social_mcp.py
```

### Step 4: Verify
```bash
# Check audit log
type Logs\audit_2026-03-04.json

# Check summary report
type Business\Social_Reports\*.md
```

---

## Expected Results

| Check | Expected |
|-------|----------|
| Browser opens | ✅ Chromium launches |
| Session loads | ✅ Persistent session used |
| Post appears | ✅ Content posted to platform |
| Summary created | ✅ Report in Social_Reports/ |
| Audit logged | ✅ Entry in audit_YYYY-MM-DD.json |

---

## Troubleshooting

### "Playwright not installed"
```bash
pip install playwright
playwright install chromium
```

### "Session expired"
- Browser will open
- Login manually when prompted
- Session saved for next time

### "Post failed"
- Check error in console
- Retry with error_recovery_mcp.py
- Check audit log for details

---

**Ready for Phase 2 Testing!** 🚀
