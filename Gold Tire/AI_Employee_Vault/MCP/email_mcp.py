"""
Email MCP - Send emails via SMTP with app password.
Reads approved email requests from Approved/Email/ folder.
"""
import smtplib
import json
import time
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Configuration - load from vault
CONFIG_PATH = Path("credential.json")

def load_credentials():
    """Load email credentials from secure vault."""
    if not CONFIG_PATH.exists():
        print("[ERROR] credential.json not found")
        return None
    
    with open(CONFIG_PATH, 'r') as f:
        creds = json.load(f)
    
    return {
        "email": creds.get("email", ""),
        "app_password": creds.get("email_app_password", ""),
        "smtp_server": creds.get("smtp_server", "smtp.gmail.com"),
        "smtp_port": creds.get("smtp_port", 587)
    }

def send_email(to: str, subject: str, body: str, cc: str = None, bcc: str = None):
    """
    Send email using SMTP with app password.
    
    Args:
        to: Recipient email address
        subject: Email subject
        body: Email body (plain text or HTML)
        cc: CC recipients (comma-separated)
        bcc: BCC recipients (comma-separated)
    
    Returns:
        bool: True if sent successfully
    """
    creds = load_credentials()
    if not creds:
        return False
    
    msg = MIMEMultipart()
    msg['From'] = creds['email']
    msg['To'] = to
    msg['Subject'] = subject
    
    if cc:
        msg['Cc'] = cc
    # BCC recipients are added to recipients list but not to email headers (handled separately)
    
    # Attach body
    msg.attach(MIMEText(body, 'plain'))
    
    # Build recipient list
    recipients = [to]
    if cc:
        recipients.extend([x.strip() for x in cc.split(',')])
    if bcc:
        recipients.extend([x.strip() for x in bcc.split(',')])
    
    try:
        server = smtplib.SMTP(creds['smtp_server'], creds['smtp_port'])
        server.starttls()
        server.login(creds['email'], creds['app_password'])
        server.send_message(msg, to_addrs=recipients)
        server.quit()
        print(f"[OK] Email sent to {to}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")
        return False

def process_approved_emails():
    """Process all approved email requests."""
    approved_dir = Path("Approved/Email")
    
    if not approved_dir.exists():
        print("[INFO] No Approved/Email folder")
        return 0
    
    files = list(approved_dir.glob("*.md"))
    if not files:
        print("[INFO] No approved emails to send")
        return 0
    
    sent_count = 0
    done_dir = Path("Done")
    done_dir.mkdir(exist_ok=True)
    
    for file in files:
        content = file.read_text()
        
        # Parse email parameters from markdown
        to_email = None
        subject = None
        body = None
        cc = None
        bcc = None
        
        for line in content.split('\n'):
            if line.startswith('To:'):
                to_email = line.replace('To:', '').strip()
            elif line.startswith('Subject:'):
                subject = line.replace('Subject:', '').strip()
            elif line.startswith('CC:'):
                cc = line.replace('CC:', '').strip()
            elif line.startswith('BCC:'):
                bcc = line.replace('BCC:', '').strip()
            elif line.startswith('---'):
                break
        
        # Extract body (everything after ---)
        parts = content.split('---', 1)
        if len(parts) > 1:
            body = parts[1].strip()
        
        if not to_email or not subject:
            print(f"[SKIP] Invalid email in {file.name}")
            continue
        
        print(f"Sending: {subject} -> {to_email}")
        
        if send_email(to_email, subject, body, cc, bcc):
            # Move to Done
            target = done_dir / f"SENT_{file.name}"
            if target.exists():
                target.unlink()
            file.replace(target)
            sent_count += 1
            
            # Log to Dashboard
            log_email_sent(to_email, subject)
    
    return sent_count

def log_email_sent(to: str, subject: str):
    """Log sent email to Dashboard.md"""
    dashboard_path = Path("Bronze Tire/AI_Employee_Vault/Dashboard.md")
    if not dashboard_path.exists():
        return
    
    content = dashboard_path.read_text()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Find Emails Sent Today section and add entry
    lines = content.split('\n')
    new_lines = []
    in_section = False
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        if '## Emails Sent Today' in line:
            in_section = True
        elif in_section and line.startswith('| Recipient'):
            # Add new entry after header row
            new_lines.append(f"| {to} | {subject[:40]} | Sent | {timestamp} |")
            in_section = False
    
    dashboard_path.write_text('\n'.join(new_lines))
    print(f"[LOG] Email logged to Dashboard")

def send_daily_briefing():
    """Generate and send daily briefing email."""
    # Gather briefing data
    pending_dir = Path("Pending_Approval")
    pending_count = len(list(pending_dir.glob("*.md"))) if pending_dir.exists() else 0
    
    needs_action_dir = Path("Needs_Action")
    unread_count = len(list(needs_action_dir.glob("*.md"))) if needs_action_dir.exists() else 0
    
    briefing = f"""Good morning!

Daily Briefing - {datetime.now().strftime('%Y-%m-%d')}

Summary:
- Pending Approvals: {pending_count}
- Unread Items: {unread_count}

Priority Actions:
"""
    
    # List pending approvals
    if pending_dir.exists():
        for f in pending_dir.glob("*.md"):
            briefing += f"- [PENDING] {f.stem}\n"
    
    briefing += """
Have a productive day!
- Suleman AI Employee v0.2 Silver
"""
    
    # Send to self or configured recipient
    creds = load_credentials()
    if creds and creds['email']:
        send_email(
            to=creds['email'],
            subject=f"Daily Briefing - {datetime.now().strftime('%Y-%m-%d')}",
            body=briefing
        )

def main():
    """Main entry point."""
    print("=" * 50)
    print("Email MCP - Silver Tier")
    print("=" * 50)
    
    # Process approved emails
    sent = process_approved_emails()
    print(f"[DONE] Sent {sent} email(s)")
    
    # Check for daily briefing trigger
    briefing_flag = Path("Trigger_Daily_Briefing.txt")
    if briefing_flag.exists():
        print("[INFO] Daily briefing triggered")
        send_daily_briefing()
        briefing_flag.unlink()

if __name__ == "__main__":
    main()
