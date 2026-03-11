# ✅ CUSTOM EMAIL RECIPIENT - COMPLETE GUIDE

**Status:** ✅ WORKING - Send emails to ANY address!  
**Feature:** Custom recipient, subject, and message

---

## 🚀 HOW TO USE

### **Step 1: Open Dashboard**
```
http://localhost:8001/working.html
```

### **Step 2: Find Email Section**
- Look for **📧 Gmail** card
- You'll see THREE input fields:
  1. **Recipient Email** - Who to send to
  2. **Subject** - Email subject line
  3. **Message** - Email body content

### **Step 3: Enter Details**

**Recipient Email:**
```
Examples:
- client@company.com
- friend@gmail.com
- support@business.com
- team@organization.org
```

**Subject:**
```
Examples:
- Meeting Reminder
- Project Update
- Quick Question
- Follow-up
```

**Message:**
```
Type your full email message here
Can be multiple paragraphs
Professional or casual tone
```

### **Step 4: Click "Send Email"**

**What happens:**
1. Email sends via Gmail SMTP
2. Uses your configured Gmail account
3. Takes 5-10 seconds
4. Success notification appears
5. Email logged to activity feed

---

## 📋 EXAMPLE USE CASES

### Send to Client:
```
Recipient: client@company.com
Subject: Project Update - Week 12
Message: 
Dear Client,

Here's the weekly update on your project...

Best regards,
Your Name
```

### Send to Team:
```
Recipient: team@company.com
Subject: Meeting Tomorrow at 2 PM
Message:
Hi Team,

Reminder: We have a meeting tomorrow at 2 PM in Conference Room A.

Please prepare your status updates.

Thanks!
```

### Send to Friend:
```
Recipient: friend@gmail.com
Subject: Lunch This Weekend?
Message:
Hey!

Want to grab lunch this weekend? Let me know what day works for you.

Cheers!
```

### Send to Professor:
```
Recipient: professor@university.edu
Subject: Question About Assignment 3
Message:
Dear Professor Smith,

I have a question about assignment 3...

Thank you,
John Student
```

---

## ✅ EMAIL FORMAT VALIDATION

### ✅ Valid Email Formats:
```
user@example.com
john.doe@company.co.uk
support@business.org
team+project@startup.io
```

### ❌ Invalid Email Formats:
```
userexample.com         ← Missing @
user@example            ← Missing domain extension
user @example.com       ← Has space
user@example,com        ← Comma instead of period
```

**Auto-Validation:**
- Dashboard checks for @ and .
- Shows error if invalid format
- Prevents sending to invalid emails

---

## 🎯 FEATURES

### ✅ What Works:
- [x] Send to ANY email address
- [x] Custom subject lines
- [x] Custom messages (any length)
- [x] Multi-paragraph emails
- [x] Professional or casual tone
- [x] Uses your Gmail account
- [x] SMTP authentication
- [x] Activity logging
- [x] View sent emails history
- [x] Email validation

### ⚠️ Notes:
- Emails send from your configured Gmail
- Recipient sees your email address
- Takes 5-10 seconds to send
- Requires internet connection
- Gmail daily limits apply (~500 emails)

---

## 🔍 TROUBLESHOOTING

### "Please fill in all fields"?

**Cause:** One or more fields empty

**Solution:**
```
1. Fill Recipient Email
2. Fill Subject
3. Fill Message
4. Click Send Email
```

---

### "Please enter a valid email address"?

**Cause:** Email format invalid

**Solution:**
```
Check email has:
- @ symbol
- Domain name
- Extension (.com, .org, etc.)

Example: user@example.com
```

---

### "Failed to send email"?

**Possible Causes:**
1. Gmail credentials not configured
2. SMTP connection failed
3. Invalid app password
4. Gmail account issue

**Solutions:**

**Check Credentials:**
```
File: D:\Hackathon 0\credentials.json
Should have:
{
    "email": "your-email@gmail.com",
    "email_app_password": "16-char-app-password"
}
```

**Check Internet:**
```
Make sure you're connected to internet
Try loading gmail.com
```

**Check App Password:**
```
Gmail → Settings → Security
2-Step Verification → App Passwords
Generate new password if needed
```

---

### Email Not Received?

**Check:**
1. **Spam folder** - Might be marked as spam
2. **Sent folder** - Check if it sent
3. **Activity feed** - Shows if logged
4. **Recipient address** - Verify it's correct

**Wait:**
- Sometimes takes 1-2 minutes
- Gmail queues can be slow
- Check again in 5 minutes

---

## 📊 ACTIVITY LOG

### View Sent Emails:

**On Dashboard:**
1. Scroll to "Recent Activity"
2. Click "Refresh Activity"
3. See all sent emails

**Log Shows:**
```
send_email
To: client@company.com
Subject: Project Update
✅ Success
Timestamp: 2026-03-10 19:30:45
```

**View Full Logs:**
- Click "Logs" button on Email card
- Opens Logs folder
- Shows complete email history

---

## 🎓 BEST PRACTICES

### Subject Lines:
- ✅ Be clear and specific
- ✅ Keep under 50 characters
- ✅ Use professional tone for work
- ✅ Include context (Project name, etc.)

### Email Content:
- ✅ Start with greeting
- ✅ Be concise but complete
- ✅ Use paragraphs for readability
- ✅ End with signature
- ✅ Proofread before sending

### Recipients:
- ✅ Double-check email address
- ✅ Use professional emails for work
- ✅ Avoid sending to wrong person
- ✅ CC when needed (future feature)

### Frequency:
- ✅ Don't spam (Gmail limits: ~500/day)
- ✅ Wait between bulk sends
- ✅ Monitor sent folder
- ✅ Respect Gmail's terms

---

## 💡 PRO TIPS

### Save Templates:

**Create text file with common emails:**
```
Meeting Reminder:
Subject: Meeting Reminder - [DATE]
Body: Hi team, reminder about our meeting...

Project Update:
Subject: Project Update - Week [X]
Body: Here's the weekly update...
```

**Copy-paste and customize when needed**

### Quick Send to Same Person:

```
1. Send first email
2. Recipient stays in field
3. Just change subject/message
4. Click send again
```

### Email Signature:

**Add to message end:**
```
Best regards,
Your Name
Your Title
Your Company
Phone: 123-456-7890
```

---

## 📖 COMPARISON

### Before (Old Way):
```
❌ Fixed recipient (solemanseher@gmail.com)
❌ Fixed subject
❌ Fixed message
❌ No customization
```

### After (New Way):
```
✅ Any recipient email
✅ Custom subject lines
✅ Custom messages
✅ Full control
✅ Professional emails
```

---

## 🔗 INTEGRATION

### API Endpoint:
```
POST /api/v1/test/email

Body:
{
    "to": "recipient@example.com",
    "subject": "Your Subject",
    "body": "Your message here..."
}

Response:
{
    "status": "success",
    "message": "Email sent successfully"
}
```

### Direct Send (Command Line):
```bash
python -c "from mcp.email_mcp import send_email; send_email('user@example.com', 'Subject', 'Message')"
```

---

## ✅ SUCCESS CHECKLIST

After sending, you should have:

- [ ] Entered recipient email
- [ ] Entered subject
- [ ] Entered message
- [ ] Clicked "Send Email"
- [ ] Watched toast notification
- [ ] Received success message
- [ ] Checked activity feed
- [ ] Verified in sent folder
- [ ] Recipient received email

---

## 📞 QUICK REFERENCE

### Dashboard URL:
```
http://localhost:8001/working.html
```

### Email Section:
- Look for: 📧 Gmail card
- Input 1: Recipient Email
- Input 2: Subject
- Input 3: Message
- Button: "Send Email"

### Email Format:
```
user@domain.com
Must have: @ and .
```

### Activity Feed:
- Location: Bottom of dashboard
- Button: "Refresh Activity"
- Shows: Last 10-15 actions

---

## 🎉 EXAMPLE WORKFLOWS

### Workflow 1: Client Communication
```
1. Open dashboard
2. Enter: client@company.com
3. Subject: Project Milestone Complete
4. Message: Dear Client, we've completed...
5. Click Send
6. Client receives in 1 minute
```

### Workflow 2: Team Coordination
```
1. Open dashboard
2. Enter: team@company.com
3. Subject: Meeting Rescheduled to 3 PM
4. Message: Hi team, meeting moved to...
5. Click Send
6. Team notified immediately
```

### Workflow 3: Customer Support
```
1. Open dashboard
2. Enter: customer@gmail.com
3. Subject: Re: Your Inquiry #12345
4. Message: Dear Customer, thank you for...
5. Click Send
6. Customer receives response
```

---

**Status:** ✅ **READY TO USE**  
**Recipient:** Any email address  
**Subject:** Custom  
**Message:** Custom  
**Send:** Via Gmail SMTP  

**OPEN DASHBOARD NOW AND SEND YOUR FIRST CUSTOM EMAIL!** 🚀
