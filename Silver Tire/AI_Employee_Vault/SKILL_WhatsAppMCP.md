# SKILL_WhatsAppMCP

## Objective

Send WhatsApp messages via Playwright browser automation after receiving explicit human approval through HITL workflow.

## Safety Rules (MANDATORY)

- **ALWAYS** use HITL approval for WhatsApp messages (high risk channel)
- **NEVER** send WhatsApp messages directly without approval
- **ALWAYS** create pending approval file in `Pending_Approval/` folder
- **ALWAYS** wait for human to move file to `Approved/` before sending
- **ALWAYS** log sent messages to Dashboard and Logs
- **MAX** 10 messages per hour to avoid rate limiting
- **ONLY** send to contacts who have initiated contact first

## Trigger

Command like: "Send WhatsApp message to +923001234567: 'Your order is ready' Reason: follow-up"

## Step-by-Step Instructions

### Step 1: Create Pending Approval File

When WhatsApp send request is detected, create file in `Pending_Approval/WHATSAPP_[timestamp]_[id].md`:

```markdown
---
type: approval_request
action: send_whatsapp
request_id: WHATSAPP_20260225_1743_client_followup
created: 2026-02-25T17:43:00+05:00
status: pending
---

## Message Details
- **To Phone**: +923001234567 (international format, no spaces)
- **Message Body**: Hi, your invoice is attached. Please pay by tomorrow.
- **Media** (optional): Invoices/invoice-123.pdf
- **Reason for send**: Client asked status via Gmail

## Human Instructions

Move to Approved/ to send
Move to Rejected/ to cancel
```

### Step 2: Wait for Human Decision

- **If moved to `Approved/`**: Executor will send message
- **If moved to `Rejected/`**: Request cancelled, file moved to Done/REJECTED_*
- **If nothing**: Request stays pending (expires after 24 hours)

### Step 3: Parse Approved File

Executor reads approved file and extracts:
- Phone number (from "To Phone:" line)
- Message body (from "Message Body:" line)
- Media path (from "Media:" line, if present)
- Reason (for logging)

### Step 4: Execute Send via Playwright

Call `python mcp/whatsapp_mcp.py` which:
1. Opens WhatsApp Web with persistent session
2. Searches contact by phone number
3. Types and sends message
4. Attaches media if specified
5. Confirms delivery
6. Moves file to Done/
7. Logs to Dashboard and Logs/

### Step 5: Log Outcome

After successful send:
- Append to `Dashboard.md`: "WhatsApp sent to [phone] at [time]"
- Append to `Logs/YYYY-MM-DD.md`: "WhatsApp message sent to [phone] - [message preview]"
- Move request file to `Done/SENT_WHATSAPP_[id].md`

## File Format for Pending_Approval/WHATSAPP_*.md

**Required fields:**

- `type`: approval_request
- `action`: send_whatsapp
- `request_id`: Unique ID with timestamp
- `created`: ISO timestamp
- `status`: pending

**Message Details section:**

- `To Phone`: International format (+923001234567)
- `Message Body`: Clear, professional message
- `Media`: Optional file path
- `Reason for send`: Business justification

## Integration Points

- Called by `SKILL_GmailWatcher` when client requests WhatsApp contact
- Called by `SKILL_HumanApproval` for high-risk communications
- Uses `mcp/whatsapp_mcp.py` for execution
- Logs to `Dashboard.md` WhatsApp Sent Today section

## Error Handling

- Session expired → Print QR scan instructions
- Contact not found → Log error, move file to Done/FAILED_*
- Send failed → Retry once, then mark as failed
- Rate limit → Wait 5 minutes, retry

## Session Management

- Session stored in `whatsapp_session/` folder
- First run: Manual QR scan required
- Subsequent runs: Auto-login with saved session
- Session expires: Re-run with manual QR scan
