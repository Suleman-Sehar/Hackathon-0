# SKILL_SendEmailMCP

## Objective
Send emails using SMTP with app password after receiving proper approval from the approval workflow.

## Step-by-Step Instructions

1. **Receive Approved Email Request**
   - Monitor `Approved/Email/` folder for authorized send requests
   - Verify approval token/signature is present
   - Extract email parameters:
     - Recipient(s) (To, CC, BCC)
     - Subject line
     - Email body (plain text or HTML)
     - Attachments (if any)

2. **Validate Request**
   - Confirm approval status in `Approved/` folder
   - Check for any restrictions or conditions
   - Verify recipient list against allowed contacts (if configured)

3. **Load Credentials**
   - Read `credential.json` from vault root
   - Extract: email, app_password, smtp_server, smtp_port
   - Never log or display credentials

4. **Send Email via SMTP**
   - Connect to SMTP server (default: smtp.gmail.com:587)
   - Start TLS encryption
   - Authenticate with app password
   - Send email to all recipients (To, CC, BCC)
   - Handle transmission errors with retry (max 3 attempts)

5. **Log and Archive**
   - Record sent email in `Dashboard.md` under "Emails Sent Today"
   - Move request file to `Done/` with SENT_ prefix
   - Update activity log

## How to Trigger

- **Automatic:** File appears in `Approved/Email/` with valid approval marker
- **Manual:** Run `python mcp/email_mcp.py` from project root
- **Scheduled:** Daily briefing at 8 AM via scheduler

## Email Request Format

```markdown
To: recipient@example.com
Subject: Meeting Confirmation
CC: manager@example.com

---

Dear Team,

This is the email body content.

Best regards,
Sender
```

## Prerequisites

- `credential.json` with email configuration:
  ```json
  {
    "email": "your-email@gmail.com",
    "email_app_password": "your-app-password",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587
  }
  ```
- Gmail app password generated (not regular password)
- Approval workflow completed before triggering

## Safety Rules

- All emails > $100 value or to new contacts require approval
- Never send to unverified recipients
- Always log sent emails to Dashboard
- BCC recipients kept hidden from headers

## Integration Points

- Called by `SKILL_HumanApproval` after approval granted
- Orchestrator checks `Approved/Email/` folder every 5 minutes
- Daily briefing scheduler triggers at 8 AM
