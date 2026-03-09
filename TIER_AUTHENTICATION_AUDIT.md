# Tier Architecture & Authentication Audit Report

**Date:** 2026-03-06
**Status:** 🔴 Critical Issues Found
**Scope:** Bronze/Silver/Gold Tier Separation + MCP Social Media Authentication

---

## 🚨 Executive Summary

### Critical Issues Identified

1. **Tier Separation Issues** - Bronze, Silver, and Gold Tiers have overlapping/duplicate files instead of proper inheritance
2. **MCP Authentication Broken** - Social media MCPs not properly checking/using saved sessions
3. **Path Resolution Errors** - MCP files using relative paths instead of absolute paths based on tier location
4. **Session Management Inconsistent** - Different session handling across tiers

---

## 📊 Issue #1: Tier Separation Problems

### Current State ❌

```
Bronze Tire/
├── AI_Employee_Vault/
│   ├── scripts/
│   └── (basic features)

Silver Tire/
├── AI_Employee_Vault/
│   ├── scripts/
│   └── mcp/ (duplicate MCP files)
├── mcp/
│   ├── email_mcp.py
│   ├── linkedin_post.py
│   └── whatsapp_mcp.py

Gold Tire/
├── AI_Employee_Vault/
│   ├── MCP/ (ANOTHER duplicate)
│   │   ├── social/
│   │   ├── email_mcp.py
│   │   └── whatsapp_mcp.py
│   └── Ralph_Wiggum/

MCP/ (Root - Shared)
├── social/
│   └── social_mcp.py (DUPLICATE x4)
├── email_mcp.py (DUPLICATE x3)
└── whatsapp_mcp.py (DUPLICATE x3)
```

### Problem

**Files are duplicated across tiers instead of being properly separated and linked:**

| MCP File | Locations Found | Issue |
|----------|----------------|-------|
| `social_mcp.py` | 4 locations | Root MCP/, Root MCP/mcp/, Gold/MCP/social/, Gold/MCP/mcp/ |
| `email_mcp.py` | 3 locations | Root MCP/, Silver/mcp/, Gold/MCP/ |
| `whatsapp_mcp.py` | 3 locations | Root MCP/, Silver/mcp/, Gold/MCP/ |
| `linkedin_post.py` | 3 locations | Root MCP/, Silver/mcp/, Gold/MCP/ |

### Expected Architecture ✅

```
Root/ (Shared Resources)
├── MCP/
│   ├── social/social_mcp.py (Gold only - uses absolute paths)
│   ├── email_mcp.py (Silver+ - uses absolute paths)
│   ├── linkedin_post.py (Silver+ - uses absolute paths)
│   └── whatsapp_mcp.py (Silver+ - uses absolute paths)

Bronze Tire/
├── AI_Employee_Vault/
│   ├── Inbox/
│   ├── Plans/
│   └── Done/
└── orchestrator.py (basic)

Silver Tire/
├── AI_Employee_Vault/
│   ├── Inbox/
│   ├── Approved/
│   │   ├── Email/
│   │   ├── LinkedIn/
│   │   └── WhatsApp/
│   └── Done/
├── orchestrator.py (imports from ../MCP/)
└── scheduler.py

Gold Tire/
├── AI_Employee_Vault/
│   ├── Needs_Action/
│   │   ├── Personal/
│   │   └── Business/
│   ├── Approved/
│   ├── Done/
│   │   ├── Personal/
│   │   └── Business/
│   └── Sessions/
│       ├── facebook_session/
│       ├── instagram_session/
│       ├── twitter_session/
│       ├── linkedin_session/
│       └── whatsapp_session/
├── orchestrator.py (imports from ../MCP/)
└── Ralph_Wiggum/
```

---

## 🔐 Issue #2: MCP Authentication Not Working

### Social Media MCP Authentication Flow

**Current Implementation:**
```python
# In MCP/social/social_mcp.py (ALL 4 copies)
def check_logged_in(page, platform: str) -> bool:
    """Check if user is logged in to the platform."""
    try:
        if platform == "facebook":
            return page.query_selector('[data-testid="create-post"]') is not None
        elif platform == "instagram":
            return page.query_selector('svg[aria-label="New post"]') is not None
        elif platform == "twitter":
            return page.query_selector('div[contenteditable="true"][role="textbox"]') is not None
        return False
    except:
        return False
```

**Problem:** The function exists but is NOT being used to validate sessions before posting!

**Current Flow:**
```python
def post_facebook(page, message: str, media_path: Optional[str] = None):
    page.goto("https://www.facebook.com")
    
    # Check if logged in
    if not check_logged_in(page, "facebook"):
        log_action("post_facebook", "warning", {"status": "not_logged_in"})
        print("\n[WARNING] Manual login required for Facebook")
        input("Press Enter after you've logged in...")  # ❌ BLOCKING - waits for manual login
```

**Issues:**
1. ✅ Session folder is created but **session state is NOT loaded** before navigation
2. ✅ `check_logged_in()` is called but only triggers **manual login prompt**
3. ✅ **No automatic retry** after detecting invalid session
4. ✅ **Session persistence** uses `launch_persistent_context` but doesn't verify saved state

### Email MCP Authentication

**Current State:**
```python
# In MCP/email_mcp.py
CONFIG_PATH = Path("credential.json")  # ❌ Relative path - breaks in Gold/Silver tiers

def load_credentials():
    if not CONFIG_PATH.exists():  # ❌ Looks in wrong directory
        print("[ERROR] credential.json not found")
        return None
```

**Problem:** Credential path is relative, so:
- Works in Root MCP/
- Fails in Silver/mcp/ (looks in Silver/credential.json)
- Fails in Gold/MCP/ (looks in Gold/credential.json)

### WhatsApp MCP Authentication

**Current State:**
```python
# In MCP/whatsapp_mcp.py
SESSION_DIR = Path("whatsapp_session")  # ❌ Relative path

# In Silver Tire/mcp/whatsapp_mcp.py ✅
BASE_DIR = Path(__file__).parent.parent.parent
SESSION_DIR = BASE_DIR / "whatsapp_session"  # ✅ Absolute path
```

**Problem:** Root MCP/whatsapp_mcp.py uses relative paths, Silver version uses absolute paths.

---

## 🔍 Detailed File Analysis

### 1. `MCP/social/social_mcp.py` (Root)

**Lines 410-430: Session Handling**
```python
# Launch browser with persistent context for session persistence
session_folder = SESSION_DIR / f"{platform}_session"
session_folder.mkdir(exist_ok=True)

# Use persistent context to maintain login sessions
context = p.chromium.launch_persistent_context(
    user_data_dir=str(session_folder),
    headless=False,
    ...
)

page = context.new_page()

# Execute post
result = post_func(page, message, media_path)

# ❌ Session is NOT explicitly loaded from saved state
# ❌ No verification that session exists before using
```

**Issue:** `launch_persistent_context` will use the `user_data_dir`, but:
1. No check if `state.json` exists in session folder
2. No explicit loading of saved storage state
3. Falls back to manual login if not logged in

### 2. `MCP/mcp/social_mcp.py` (Root)

**Lines 140-160: Session Loading Attempt**
```python
# Load existing session if available
session_file = SESSION_DIR / f"{platform}_session" / "state.json"
if session_file.exists():
    try:
        await context.storage_state(path=session_file)  # ❌ WRONG METHOD
    except:
        pass
```

**Issue:** `storage_state()` is for **saving**, not loading! Should use:
```python
context = browser.new_context(
    storage_state=session_file  # ✅ Correct way to load
)
```

### 3. `Gold Tire/AI_Employee_Vault/MCP/social/social_mcp.py`

Same issues as root version - **duplicated code with same bugs**.

---

## 🛠️ Required Fixes

### Fix #1: Consolidate MCP Files

**Action:** Remove duplicate MCP files from tier directories

```bash
# Keep only in Root/MCP/
✅ Root/MCP/social/social_mcp.py
✅ Root/MCP/email_mcp.py
✅ Root/MCP/linkedin_post.py
✅ Root/MCP/whatsapp_mcp.py

# Delete duplicates
❌ Silver/mcp/email_mcp.py
❌ Silver/mcp/linkedin_post.py
❌ Silver/mcp/whatsapp_mcp.py
❌ Silver/mcp/whatsapp_simple.py
❌ Gold/MCP/email_mcp.py
❌ Gold/MCP/whatsapp_mcp.py
❌ Gold/MCP/mcp/social_mcp.py
❌ Gold/MCP/social/social_mcp.py (keep only one)
```

### Fix #2: Fix Path Resolution in All MCPs

**For Root/MCP/*.py files:**
```python
# ✅ Use absolute paths based on script location
from pathlib import Path

# Get the root directory (parent of MCP folder)
ROOT_DIR = Path(__file__).parent.parent

# Now paths work from any tier
CREDENTIAL_PATHS = [
    ROOT_DIR / "credential.json",
    ROOT_DIR / "Bronze Tire" / "AI_Employee_Vault" / "credential.json",
    ROOT_DIR / "Silver Tire" / "credential.json",
    ROOT_DIR / "Gold Tire" / "AI_Employee_Vault" / "credential.json",
]

SESSION_DIR = ROOT_DIR  # Sessions stored at root level
```

### Fix #3: Fix Session Loading in Social MCP

**Replace lines 410-430 in `MCP/social/social_mcp.py`:**

```python
def execute_social_action(input_data: Dict[str, Any]) -> Dict[str, Any]:
    # ... existing code ...

    try:
        with sync_playwright() as p:
            session_folder = SESSION_DIR / f"{platform}_session"
            session_folder.mkdir(exist_ok=True)
            
            # ✅ Check if session exists
            session_state_file = session_folder / "state.json"
            has_saved_session = session_state_file.exists()

            # Use persistent context
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(session_folder),
                headless=False,
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                locale="en-US",
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-dev-shm-usage'
                ],
                ignore_default_args=['--enable-automation']
            )

            page = context.new_page()

            # ✅ If we have saved session, verify it's still valid
            if has_saved_session:
                print(f"[INFO] Found saved session for {platform}")
                page.goto(f"https://www.{platform}.com", timeout=30000)
                page.wait_for_timeout(5000)
                
                if not check_logged_in(page, platform):
                    print(f"[WARNING] Saved session invalid, needs re-login")
                    log_action(f"{platform}_session", "expired", {})
                else:
                    print(f"[OK] Session verified for {platform}")

            # Execute post
            result = post_func(page, message, media_path)

            # ✅ Save session after successful action
            if result.get("status") == "success":
                try:
                    context.storage_state(path=str(session_state_file))
                    print(f"[INFO] Session saved for {platform}")
                except Exception as e:
                    print(f"[WARN] Could not save session: {e}")

            context.close()
            return result

    except Exception as e:
        log_action(action, "error", {"error": str(e)})
        return {"status": "error", "error": str(e)}
```

### Fix #4: Add Automatic Session Recovery

**In `post_facebook()`, `post_instagram()`, `post_twitter()`:**

```python
def post_facebook(page, message: str, media_path: Optional[str] = None):
    log_action("post_facebook", "info", {"status": "starting"})

    try:
        page.goto("https://www.facebook.com", timeout=60000)
        human_delay(*DELAY_PAGE_LOAD)

        # ✅ Check if logged in
        if not check_logged_in(page, "facebook"):
            log_action("post_facebook", "error", {"status": "not_logged_in"})
            
            # ✅ Return error instead of blocking for manual login
            return {
                "status": "error",
                "error": "Not logged in. Run: python MCP/social/login_helper.py"
            }

        # ... rest of posting logic ...
```

### Fix #5: Create Tier Linking Documentation

**Create `TIER_LINKING.md`:**

```markdown
# Tier Linking Guide

## How Tiers Are Connected

### Bronze → Silver → Gold Inheritance

Tiers share MCP tools from root `/MCP/` directory via relative imports.

**Silver Tier uses:**
```bash
python ../MCP/email_mcp.py < input.json
python ../MCP/linkedin_post.py < input.json
python ../MCP/whatsapp_mcp.py < input.json
```

**Gold Tier uses:**
```bash
python ../MCP/social/social_mcp.py < input.json
python ../MCP/email_mcp.py < input.json
```

### Session Storage

All tiers share session storage at root level:
- `/facebook_session/`
- `/instagram_session/`
- `/twitter_session/`
- `/linkedin_session/`
- `/whatsapp_session/`

### Credentials

Credentials stored in:
- Primary: `/credential.json`
- Fallback: `/Bronze Tire/AI_Employee_Vault/credential.json`
```

---

## 📋 Action Items

### Priority 1: Critical (Authentication Broken)

- [ ] **Fix session loading in `MCP/social/social_mcp.py`** - Add proper session state loading
- [ ] **Fix credential paths in `MCP/email_mcp.py`** - Use absolute paths with fallbacks
- [ ] **Fix session paths in `MCP/whatsapp_mcp.py`** - Use absolute paths
- [ ] **Fix session paths in `MCP/linkedin_post.py`** - Use absolute paths
- [ ] **Remove blocking manual login prompts** - Return errors instead

### Priority 2: High (Tier Separation)

- [ ] **Delete duplicate MCP files from Silver/mcp/**
- [ ] **Delete duplicate MCP files from Gold/MCP/**
- [ ] **Update Silver orchestrator** to import from `../MCP/`
- [ ] **Update Gold orchestrator** to import from `../MCP/`
- [ ] **Create TIER_LINKING.md** documentation

### Priority 3: Medium (Improvements)

- [ ] **Add session validation before posting**
- [ ] **Add automatic session refresh**
- [ ] **Add session expiry alerts**
- [ ] **Create unified session manager MCP**
- [ ] **Add credential encryption**

---

## 🧪 Testing Plan

### Test 1: Email MCP from Silver Tier

```bash
cd "Silver Tire"
echo '{"to": "test@example.com", "subject": "Test", "body": "Test body"}' | python ../MCP/email_mcp.py
# Expected: Works with credentials from root credential.json
```

### Test 2: Social MCP from Gold Tier

```bash
cd "Gold Tire"
echo '{"action": "post_facebook", "message": "Test post"}' | python ../MCP/social/social_mcp.py
# Expected: Uses saved session from facebook_session/state.json
```

### Test 3: WhatsApp MCP from Root

```bash
python MCP/whatsapp_mcp.py
# Expected: Uses session from whatsapp_session/
```

---

## 📞 Next Steps

1. **Immediate:** Fix authentication in all MCP files (Priority 1)
2. **Short-term:** Clean up duplicate files (Priority 2)
3. **Long-term:** Implement session manager (Priority 3)

---

**Audit Status:** 🔴 Requires Immediate Action
**Estimated Fix Time:** 2-3 hours
**Risk Level:** HIGH - Authentication currently broken for social media MCPs
