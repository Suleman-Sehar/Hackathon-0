# Silver Tier Dashboard - Documentation

## 🎯 Overview

The **Silver Tier Dashboard** is an elegant, sophisticated, and modern web-based interface for monitoring and controlling your AI Employee automation system. It provides real-time visibility into Gmail, WhatsApp, and LinkedIn integrations with beautiful visualizations and one-click actions.

---

## ✨ Features

### 🎨 Modern UI/UX
- **Glassmorphism Design**: Frosted glass effects with backdrop blur
- **Gradient Backgrounds**: Animated silver and purple gradients
- **Smooth Animations**: Polished transitions and micro-interactions
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Dark/Light Compatible**: Adapts to system preferences

### 📊 Real-Time Monitoring
- **Live Metrics**: Emails sent, WhatsApp messages, LinkedIn posts
- **Platform Status**: Connection status for each integration
- **Activity Feed**: Recent actions with timestamps and status
- **System Health**: API status, session storage, error rates

### 🚀 Quick Actions
- **Send Email**: Create and send emails via Gmail SMTP
- **WhatsApp Message**: Send messages to any contact
- **LinkedIn Post**: Publish autonomous posts
- **Run Orchestrator**: Process all pending actions

### 🔔 Notifications
- **Toast Notifications**: Success, error, and warning messages
- **Auto-Refresh**: Dashboard updates every 30 seconds
- **Manual Refresh**: One-click data refresh

---

## 📁 Project Structure

```
Silver Tire/
├── dashboard/
│   ├── index.html              # Main dashboard HTML
│   └── static/
│       ├── css/
│       │   └── styles.css      # Sophisticated styling
│       └── js/
│           └── app.js          # Dashboard application logic
├── dashboard_api.py            # FastAPI backend
├── mcp/
│   ├── email_mcp.py           # Gmail integration
│   ├── whatsapp_mcp.py        # WhatsApp automation
│   └── linkedin_post.py       # LinkedIn posting
├── Logs/                       # Audit logs
├── whatsapp_session/           # WhatsApp browser session
├── linkedin_session/           # LinkedIn browser session
└── README_DASHBOARD.md         # This file
```

---

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed
2. **Playwright** for browser automation
3. **FastAPI** and **Uvicorn** for the API server
4. **Credentials** configured in `credentials.json`

### Installation

1. **Install dependencies:**
```bash
cd "D:\Hackathon 0\Silver Tire"
pip install fastapi uvicorn playwright
playwright install chromium
```

2. **Configure credentials:**
Create `credentials.json` in the root directory:
```json
{
    "email": "your-email@gmail.com",
    "email_app_password": "your-app-password",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587
}
```

3. **Start the dashboard:**
```bash
python dashboard_api.py
```

4. **Open in browser:**
Navigate to: `http://localhost:8001`

---

## 📱 Dashboard Sections

### 1. Header
- **Logo & Branding**: Silver Tier identity
- **System Status**: Real-time online indicator
- **Current DateTime**: Live clock
- **Refresh Button**: Manual data refresh

### 2. Welcome Banner
- **Greeting Message**: Welcome text
- **Quick Action Buttons**: Email, WhatsApp, LinkedIn

### 3. Metrics Grid
Four animated metric cards showing:
- **Emails Sent Today**: Gmail automation count
- **WhatsApp Messages**: Browser automation count
- **LinkedIn Posts**: Autonomous posting count
- **Total Actions**: Combined activity

### 4. Platform Status
Three platform cards displaying:
- **Gmail**: SMTP email status
- **WhatsApp**: Browser session status
- **LinkedIn**: Auto-posting status

Each card shows:
- Connection status (Connected/Disconnected)
- Sent/Posted count today
- Pending actions count
- Test and Logs buttons

### 5. Recent Activity
- **Live Feed**: Last 15 actions
- **Action Icons**: Platform-specific icons
- **Status Badges**: Success/Pending/Error
- **Timestamps**: Local time format

### 6. Quick Actions
Four clickable cards:
- **Send Email**: Opens email composition modal
- **Send WhatsApp**: Opens message modal
- **Post to LinkedIn**: Opens post creation modal
- **Run Orchestrator**: Processes pending actions

### 7. System Health
Real-time health indicators:
- **API Status**: Backend health
- **Session Storage**: Browser sessions
- **Auto-Processing**: Orchestrator status
- **Error Rate**: Percentage of failed actions

---

## 🔧 API Endpoints

### Dashboard
```
GET  /                          # Serve dashboard HTML
GET  /api/v1/health             # Health check
```

### Metrics & Status
```
GET  /api/v1/metrics            # Get today's metrics
GET  /api/v1/metrics?date=YYYY-MM-DD  # Get specific date
GET  /api/v1/platforms          # Platform connection status
GET  /api/v1/activity?limit=20  # Recent activity feed
```

### Actions
```
POST /api/v1/test/email         # Send test email
POST /api/v1/test/whatsapp      # Send test WhatsApp
POST /api/v1/test/linkedin      # Create test LinkedIn post
POST /api/v1/orchestrator/run   # Run orchestrator
```

---

## 📝 Usage Examples

### Send Email via Dashboard

1. Click **"New Email"** or **"Send Email"** quick action
2. Fill in the form:
   - **To**: recipient@example.com
   - **Subject**: Meeting Reminder
   - **Message**: Your message here
3. Click **"Send Email"**
4. Watch for success notification

### Send WhatsApp Message

1. Click **"Send WhatsApp"** quick action
2. Fill in the form:
   - **Phone**: +923322580130
   - **Message**: Hello from Silver Tier!
3. Click **"Send Message"**
4. Browser will open and send automatically

### Create LinkedIn Post

1. Click **"Post to LinkedIn"** quick action
2. Enter your post content
3. Click **"Publish Post"**
4. Browser will open and post automatically

### Run Orchestrator

1. Click **"Run Orchestrator"** quick action
2. System processes all pending actions:
   - Approved emails → Sent
   - Approved WhatsApp → Sent
   - Approved LinkedIn → Posted
3. Dashboard auto-refreshes with updated metrics

---

## 🎨 Customization

### Change Colors

Edit `dashboard/static/css/styles.css`:

```css
:root {
    --primary: #6366f1;        /* Main brand color */
    --secondary: #8b5cf6;      /* Secondary color */
    --accent: #06b6d4;         /* Accent color */
    --success: #10b981;        /* Success state */
    --danger: #ef4444;         /* Error state */
}
```

### Modify Refresh Interval

Edit `dashboard/static/js/app.js`:

```javascript
// Change from 30000ms (30s) to desired value
refreshInterval = setInterval(() => {
    loadDashboardData();
}, 60000);  // 60 seconds
```

### Add Custom Metrics

Edit `dashboard_api.py` and add to `get_metrics()` function.

---

## 🔐 Security Notes

### Credentials
- Store `credentials.json` securely
- Never commit to version control
- Use Gmail App Password, not regular password

### App Password Setup (Gmail)
1. Go to Google Account Settings
2. Security → 2-Step Verification
3. App Passwords → Generate
4. Copy 16-character password
5. Add to `credentials.json`

### Session Storage
- WhatsApp session saved in `whatsapp_session/`
- LinkedIn session saved in `linkedin_session/`
- Sessions persist across restarts
- Delete folders to reset sessions

---

## 🐛 Troubleshooting

### Dashboard Won't Load
```bash
# Check if server is running
python dashboard_api.py

# Verify port 8001 is not in use
netstat -ano | findstr :8001
```

### Metrics Show Zero
```bash
# Check audit logs exist
dir Logs\audit_*.json

# Verify logs folder permissions
```

### Platform Shows Disconnected

**Gmail:**
- Verify `credentials.json` exists
- Check email and app password are correct
- Test SMTP connection manually

**WhatsApp:**
- Run WhatsApp MCP once to create session
- Scan QR code with mobile app
- Session saves automatically

**LinkedIn:**
- Run LinkedIn MCP once to login
- Complete login in browser
- Session saves automatically

### Browser Automation Fails
```bash
# Reinstall Playwright browsers
playwright install chromium

# Check Playwright version
playwright --version
```

---

## 📊 Metrics Explanation

| Metric | Description | Source |
|--------|-------------|--------|
| Emails Sent | Total emails sent today | Gmail SMTP logs |
| WhatsApp Messages | Messages sent today | Browser automation |
| LinkedIn Posts | Posts published today | Browser automation |
| Total Actions | All combined actions | Audit log count |
| Error Rate | Percentage of failed actions | Calculated |

---

## 🎯 Best Practices

### Daily Workflow
1. **Morning**: Open dashboard, review overnight activity
2. **Check Pending**: Review pending approvals
3. **Run Orchestrator**: Process all pending actions
4. **Monitor**: Watch real-time metrics throughout day

### Weekly Tasks
1. **Review Logs**: Check activity feed for errors
2. **Clear Sessions**: Reset browser sessions if needed
3. **Update Credentials**: Rotate app passwords monthly

### Performance Tips
1. **Limit Activity Feed**: Keep last 15-20 items
2. **Archive Old Logs**: Move old audit logs monthly
3. **Clear Browser Cache**: Reset sessions weekly

---

## 📞 Support

### Common Issues

**Issue**: Email not sending
- **Solution**: Check Gmail app password, verify SMTP settings

**Issue**: WhatsApp not connecting
- **Solution**: Delete `whatsapp_session/` folder, re-scan QR code

**Issue**: LinkedIn post fails
- **Solution**: Login manually once, save session

**Issue**: Dashboard slow
- **Solution**: Clear browser cache, reduce refresh frequency

### Getting Help

1. Check audit logs: `Logs/audit_YYYY-MM-DD.json`
2. Review console errors: Browser DevTools → Console
3. Verify API health: `http://localhost:8001/api/v1/health`

---

## 🚀 Advanced Features

### Custom Integrations

Add new platform by:
1. Create MCP module in `mcp/` folder
2. Add API endpoint in `dashboard_api.py`
3. Add UI card in `index.html`
4. Add JavaScript handler in `app.js`

### Automated Reporting

Schedule daily email reports:
```python
# Add to dashboard_api.py
@app.get("/api/v1/report/daily")
async def daily_report():
    metrics = get_metrics()
    send_email(
        to="ceo@company.com",
        subject=f"Daily Report - {datetime.now().strftime('%Y-%m-%d')}",
        body=f"""
        Daily Automation Report
        
        Emails Sent: {metrics['emails_sent']}
        WhatsApp Messages: {metrics['whatsapp_sent']}
        LinkedIn Posts: {metrics['linkedin_posts']}
        Total Actions: {metrics['total_actions']}
        """
    )
```

### Webhook Integration

Trigger actions from external systems:
```python
@app.post("/api/v1/webhook")
async def webhook(data: dict):
    if data['type'] == 'email':
        send_email(data['to'], data['subject'], data['body'])
    elif data['type'] == 'whatsapp':
        send_whatsapp_message(data['phone'], data['message'])
    return {"status": "success"}
```

---

## 📈 Future Enhancements

- [ ] Real-time WebSocket updates
- [ ] Dark mode toggle
- [ ] Export metrics to CSV/PDF
- [ ] Custom dashboard themes
- [ ] Mobile app version
- [ ] Advanced analytics charts
- [ ] Multi-user support
- [ ] Role-based access control

---

## 📄 License

Part of Silver Tier AI Employee System - v0.2

---

## 🎉 Success!

Your Silver Tier Dashboard is now ready to use!

**Access it at**: `http://localhost:8001`

**Enjoy your elegant, sophisticated, and modern automation dashboard!** 🚀✨
