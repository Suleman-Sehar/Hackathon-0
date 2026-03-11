/**
 * Silver Tier Dashboard - JavaScript Application
 * Modern, sophisticated dashboard for AI Employee v0.2
 */

// Configuration
const API_BASE = '/api/v1';
let refreshInterval;
let isRefreshing = false;

// Initialize dashboard on load
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Silver Tier Dashboard initialized');
    updateDateTime();
    loadDashboardData();
    
    // Auto-refresh every 30 seconds
    refreshInterval = setInterval(() => {
        loadDashboardData();
    }, 30000);
    
    // Update datetime every second
    setInterval(updateDateTime, 1000);
});

/**
 * Update current date and time display
 */
function updateDateTime() {
    const now = new Date();
    const options = { 
        weekday: 'short', 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    };
    const dateTimeEl = document.getElementById('currentDateTime');
    if (dateTimeEl) {
        dateTimeEl.textContent = now.toLocaleDateString('en-US', options);
    }
}

/**
 * Load all dashboard data
 */
async function loadDashboardData() {
    if (isRefreshing) return;
    
    isRefreshing = true;
    try {
        await Promise.all([
            loadMetrics(),
            loadPlatformStatus(),
            loadActivityFeed()
        ]);
        showToast('Dashboard updated', 'success');
    } catch (error) {
        console.error('Failed to load dashboard data:', error);
        showToast('Failed to refresh dashboard', 'error');
    } finally {
        isRefreshing = false;
    }
}

/**
 * Refresh all data manually
 */
function refreshAllData() {
    const btn = document.querySelector('.btn-refresh');
    if (btn) {
        btn.style.animation = 'none';
        btn.offsetHeight; // Trigger reflow
        btn.style.animation = null;
    }
    loadDashboardData();
}

/**
 * Load metrics from API
 */
async function loadMetrics() {
    try {
        const response = await fetch(`${API_BASE}/metrics`);
        if (!response.ok) throw new Error('Failed to fetch metrics');
        
        const metrics = await response.json();
        updateMetricsUI(metrics);
    } catch (error) {
        console.error('Failed to load metrics:', error);
        // Fallback: parse audit logs directly
        parseAuditLogsForMetrics();
    }
}

/**
 * Update metrics UI
 */
function updateMetricsUI(metrics) {
    // Animate numbers
    animateNumber('metricEmails', metrics.emails_sent || 0);
    animateNumber('metricWhatsApp', metrics.whatsapp_sent || 0);
    animateNumber('metricLinkedIn', metrics.linkedin_posts || 0);
    animateNumber('metricTotal', metrics.total_actions || 0);
    
    // Update platform stats
    document.getElementById('gmailSent').textContent = metrics.emails_sent || 0;
    document.getElementById('whatsappSent').textContent = metrics.whatsapp_sent || 0;
    document.getElementById('linkedinPosts').textContent = metrics.linkedin_posts || 0;
    
    // Update error rate
    const errorRate = metrics.total_actions > 0 
        ? Math.round((metrics.errors / metrics.total_actions) * 100) 
        : 0;
    document.getElementById('errorRate').textContent = `${errorRate}%`;
}

/**
 * Parse audit logs directly (fallback)
 */
async function parseAuditLogsForMetrics() {
    try {
        const today = new Date().toISOString().split('T')[0];
        const response = await fetch(`../Logs/audit_${today}.json`);
        
        if (response.ok) {
            const logs = await response.json();
            const metrics = {
                emails_sent: logs.filter(l => l.action === 'send_email' && l.status === 'success').length,
                whatsapp_sent: logs.filter(l => l.action === 'send_whatsapp' && l.status === 'success').length,
                linkedin_posts: logs.filter(l => l.action === 'post_linkedin' && l.status === 'success').length,
                total_actions: logs.length,
                errors: logs.filter(l => l.status === 'error').length
            };
            updateMetricsUI(metrics);
        }
    } catch (error) {
        console.error('Failed to parse audit logs:', error);
    }
}

/**
 * Load platform status
 */
async function loadPlatformStatus() {
    try {
        const response = await fetch(`${API_BASE}/platforms`);
        if (!response.ok) throw new Error('Failed to fetch platform status');
        
        const data = await response.json();
        updatePlatformStatusUI(data.platforms);
    } catch (error) {
        console.error('Failed to load platform status:', error);
    }
}

/**
 * Update platform status UI
 */
function updatePlatformStatusUI(platforms) {
    platforms.forEach(platform => {
        const card = document.getElementById(`platform${capitalize(platform.platform)}`);
        if (!card) return;
        
        const statusEl = card.querySelector('.platform-status');
        const statusDot = card.querySelector('.status-dot');
        const statusText = statusEl.querySelector('span');
        
        if (platform.connected) {
            card.classList.add('connected');
            card.classList.remove('disconnected');
            statusEl.classList.add('connected');
            statusEl.classList.remove('disconnected');
            statusDot.style.background = 'var(--success)';
            statusText.textContent = 'Connected';
        } else {
            card.classList.remove('connected');
            card.classList.add('disconnected');
            statusEl.classList.add('disconnected');
            statusEl.classList.remove('connected');
            statusDot.style.background = 'var(--danger)';
            statusText.textContent = 'Disconnected';
        }
        
        // Update pending count
        const pendingEl = card.querySelector(`#${platform.platform}Pending`);
        if (pendingEl) {
            pendingEl.textContent = platform.pending || 0;
        }
    });
}

/**
 * Load recent activity
 */
async function loadActivityFeed() {
    const feedEl = document.getElementById('activityFeed');
    
    console.log('📊 [ACTIVITY] Starting to load activity feed...');
    
    // Show loading state immediately
    if (feedEl) {
        feedEl.innerHTML = `
            <div class="loading-spinner">
                <div class="spinner"></div>
                <p>Loading activity...</p>
                <p style="font-size: 0.75rem; color: var(--gray-light); margin-top: 0.5rem;">Fetching from API...</p>
            </div>
        `;
    }
    
    try {
        // Add cache-busting timestamp
        const timestamp = Date.now();
        const url = `${API_BASE}/activity?limit=15&_t=${timestamp}`;
        
        console.log('📊 [ACTIVITY] Fetching:', url);
        
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            },
            cache: 'no-store'
        });
        
        console.log('📊 [ACTIVITY] Response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const logs = await response.json();
        console.log('📊 [ACTIVITY] Received', logs.length, 'activities');
        
        renderActivityFeed(logs);
    } catch (error) {
        console.error('❌ [ACTIVITY] Failed to load:', error);
        
        // Show error state with helpful message and retry button
        if (feedEl) {
            feedEl.innerHTML = `
                <div class="loading-spinner">
                    <i class="fas fa-exclamation-triangle" style="font-size: 3rem; color: var(--warning); margin-bottom: 1rem;"></i>
                    <p style="font-weight: 600;">Could not load activity</p>
                    <p style="font-size: 0.75rem; color: var(--gray); margin-top: 0.5rem;">${error.message}</p>
                    <button class="btn btn-sm btn-primary" onclick="loadActivityFeed()" style="margin-top: 1rem;">
                        <i class="fas fa-sync"></i> Retry
                    </button>
                    <p style="font-size: 0.6875rem; color: var(--gray-light); margin-top: 1rem;">
                        Tip: Press Ctrl+Shift+R to hard refresh
                    </p>
                </div>
            `;
        }
    }
}

/**
 * Render activity feed
 */
function renderActivityFeed(logs) {
    const feedEl = document.getElementById('activityFeed');
    if (!feedEl) {
        console.error('❌ [ACTIVITY] Feed element not found');
        return;
    }

    console.log('📊 [ACTIVITY] Rendering', logs ? logs.length : 0, 'activities');

    if (!logs || logs.length === 0) {
        feedEl.innerHTML = `
            <div class="loading-spinner">
                <i class="fas fa-inbox" style="font-size: 3rem; color: var(--gray-light); margin-bottom: 1rem;"></i>
                <p style="font-weight: 600;">No recent activity</p>
                <p style="font-size: 0.75rem; color: var(--gray); margin-top: 0.5rem;">
                    Actions will appear here after sending emails, messages, or posts
                </p>
            </div>
        `;
        return;
    }

    feedEl.innerHTML = logs.map(log => createActivityItem(log)).join('');
    console.log('📊 [ACTIVITY] Render complete');
}

/**
 * Create activity item HTML
 */
function createActivityItem(log) {
    const iconMap = {
        'send_email': { icon: 'fa-envelope', class: 'email', label: 'Email' },
        'send_whatsapp': { icon: 'fa-whatsapp', class: 'whatsapp', label: 'WhatsApp' },
        'post_linkedin': { icon: 'fa-linkedin', class: 'linkedin', label: 'LinkedIn' },
        'post_facebook': { icon: 'fa-facebook', class: 'default', label: 'Facebook' },
        'post_twitter': { icon: 'fa-twitter', class: 'default', label: 'Twitter' }
    };

    const iconData = iconMap[log.action] || { icon: 'fa-info', class: 'default', label: 'Activity' };
    const statusClass = log.status === 'success' ? 'success' : log.status === 'error' ? 'error' : 'pending';
    const time = new Date(log.timestamp).toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    });

    const details = log.details || {};
    
    // Get recipient/profile info based on action type
    let recipient = '';
    let recipientLabel = '';
    let content = '';
    
    if (log.action === 'send_email') {
        recipient = details.to || '';
        recipientLabel = 'To:';
        content = details.subject || '';
    } else if (log.action === 'send_whatsapp') {
        recipient = details.phone || '';
        recipientLabel = 'Phone:';
        content = details.message ? details.message.substring(0, 50) + '...' : '';
    } else if (log.action === 'post_linkedin') {
        recipient = 'LinkedIn Profile';
        recipientLabel = 'Profile:';
        content = details.content ? details.content.substring(0, 50) + '...' : '';
    } else {
        recipient = log.action.replace(/_/g, ' ');
    }
    
    // Add error message if failed
    const errorInfo = log.error ? `<div class="activity-error"><i class="fas fa-exclamation-circle"></i> ${log.error}</div>` : '';

    return `
        <div class="activity-item">
            <div class="activity-icon ${iconData.class}">
                <i class="fas ${iconData.icon}"></i>
            </div>
            <div class="activity-content">
                <div class="activity-title">${formatActionName(log.action)}</div>
                <div class="activity-desc">
                    <strong>${recipientLabel}</strong> ${recipient}<br>
                    ${content ? `<span style="color: var(--gray);">${content}</span>` : ''}
                </div>
                <div class="activity-meta">
                    <span class="activity-time"><i class="far fa-clock"></i> ${time}</span>
                    <span class="activity-status ${statusClass}">${log.status}</span>
                </div>
                ${errorInfo}
            </div>
        </div>
    `;
}

/**
 * Format action name
 */
function formatActionName(action) {
    return action.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

/**
 * Test Gmail
 */
async function testGmail() {
    console.log('📧 Testing Gmail...');
    showToast('📧 Sending email to solemanseher@gmail.com...', 'warning');

    try {
        const response = await fetch(`${API_BASE}/test/email`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                to: 'solemanseher@gmail.com',
                subject: 'Silver Tier Test - Gmail Integration',
                body: 'This is a test email from the Silver Tier Dashboard.\n\nTimestamp: ' + new Date().toLocaleString()
            })
        });

        console.log('Response status:', response.status);
        
        // Try to parse response
        let result;
        const text = await response.text();
        console.log('Response text:', text);
        
        try {
            result = JSON.parse(text);
        } catch (e) {
            throw new Error('Invalid response from server: ' + text);
        }

        if (response.ok && result.status === 'success') {
            showToast('✅ Email sent successfully to solemanseher@gmail.com!', 'success');
            setTimeout(loadDashboardData, 2000);
        } else {
            showToast('❌ ' + (result.detail || 'Failed to send email'), 'error');
        }
    } catch (error) {
        console.error('Email test error:', error);
        showToast('❌ Error: ' + error.message, 'error');
    }
}

/**
 * Test WhatsApp
 */
async function testWhatsApp() {
    console.log('💬 Testing WhatsApp...');
    showToast('💬 Sending WhatsApp to +923322580130...', 'warning');
    
    try {
        const response = await fetch(`${API_BASE}/test/whatsapp`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                phone: '+923322580130',
                message: '🚀 Test message from Silver Tier Dashboard!\n\nThis is an automated message sent via browser automation.\n\nTimestamp: ' + new Date().toLocaleString()
            })
        });
        
        console.log('Response status:', response.status);
        
        let result;
        const text = await response.text();
        console.log('Response text:', text);
        
        try {
            result = JSON.parse(text);
        } catch (e) {
            throw new Error('Invalid response from server: ' + text);
        }
        
        if (response.ok && result.status === 'success') {
            showToast('✅ WhatsApp sent to +923322580130!', 'success');
            setTimeout(loadDashboardData, 2000);
        } else {
            showToast('❌ ' + (result.detail || 'Failed to send WhatsApp'), 'error');
        }
    } catch (error) {
        console.error('WhatsApp test error:', error);
        showToast('❌ Error: ' + error.message, 'error');
    }
}

/**
 * Test LinkedIn
 */
async function testLinkedIn() {
    console.log('💼 Testing LinkedIn...');
    showToast('💼 Posting to LinkedIn Profile...', 'warning');

    try {
        const response = await fetch(`${API_BASE}/test/linkedin`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                content: `🚀 Exciting Update from Silver Tier!

Testing autonomous posting capabilities with my AI Employee system.

✨ Features:
• Gmail integration - Automated emails
• WhatsApp automation - Browser-based messaging
• LinkedIn auto-posting - Autonomous content publishing

The future of work is here!

#AI #Automation #Productivity #SilverTier`}
            })
        });

        console.log('Response status:', response.status);
        
        let result;
        const text = await response.text();
        console.log('Response text:', text);
        
        try {
            result = JSON.parse(text);
        } catch (e) {
            throw new Error('Invalid response from server: ' + text);
        }

        if (response.ok && result.status === 'success') {
            showToast('✅ Posted to LinkedIn Profile successfully!', 'success');
            setTimeout(loadDashboardData, 2000);
        } else {
            showToast('❌ ' + (result.detail || 'Failed to create post'), 'error');
        }
    } catch (error) {
        console.error('LinkedIn test error:', error);
        showToast('❌ Error: ' + error.message, 'error');
    }
}

/**
 * Run orchestrator
 */
async function runOrchestrator() {
    showToast('Starting orchestrator...', 'warning');
    
    try {
        const response = await fetch(`${API_BASE}/orchestrator/run`, {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (response.ok && result.status === 'success') {
            showToast('Orchestrator started! Processing pending actions...', 'success');
            setTimeout(() => {
                loadDashboardData();
            }, 3000);
        } else {
            showToast(result.detail || 'Failed to start orchestrator', 'error');
        }
    } catch (error) {
        showToast('Error: ' + error.message, 'error');
    }
}

/**
 * Open quick action modal
 */
function openQuickAction(type) {
    const modal = document.getElementById('actionModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');
    
    let content = '';
    
    switch (type) {
        case 'email':
            modalTitle.textContent = 'Send Email';
            content = `
                <form onsubmit="submitEmail(event)">
                    <div class="form-group">
                        <label>To:</label>
                        <input type="email" name="to" required placeholder="recipient@example.com" class="form-input">
                    </div>
                    <div class="form-group">
                        <label>Subject:</label>
                        <input type="text" name="subject" required placeholder="Email subject" class="form-input">
                    </div>
                    <div class="form-group">
                        <label>Message:</label>
                        <textarea name="body" required rows="5" placeholder="Your message..." class="form-input"></textarea>
                    </div>
                    <div class="form-actions">
                        <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button>
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-paper-plane"></i>
                            Send Email
                        </button>
                    </div>
                </form>
            `;
            break;
            
        case 'whatsapp':
            modalTitle.textContent = 'Send WhatsApp Message';
            content = `
                <form onsubmit="submitWhatsApp(event)">
                    <div class="form-group">
                        <label>Phone Number:</label>
                        <input type="tel" name="phone" required placeholder="+1234567890" class="form-input">
                    </div>
                    <div class="form-group">
                        <label>Message:</label>
                        <textarea name="message" required rows="5" placeholder="Your message..." class="form-input"></textarea>
                    </div>
                    <div class="form-actions">
                        <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button>
                        <button type="submit" class="btn btn-primary">
                            <i class="fab fa-whatsapp"></i>
                            Send Message
                        </button>
                    </div>
                </form>
            `;
            break;
            
        case 'linkedin':
            modalTitle.textContent = 'Create LinkedIn Post';
            content = `
                <form onsubmit="submitLinkedIn(event)">
                    <div class="form-group">
                        <label>Post Content:</label>
                        <textarea name="content" required rows="6" placeholder="What do you want to share?" class="form-input"></textarea>
                    </div>
                    <div class="form-actions">
                        <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button>
                        <button type="submit" class="btn btn-accent">
                            <i class="fab fa-linkedin"></i>
                            Publish Post
                        </button>
                    </div>
                </form>
            `;
            break;
    }
    
    modalBody.innerHTML = content;
    modal.classList.add('active');
}

/**
 * Close modal
 */
function closeModal() {
    const modal = document.getElementById('actionModal');
    modal.classList.remove('active');
}

/**
 * Submit email form
 */
async function submitEmail(event) {
    event.preventDefault();
    const form = event.target;
    const data = new FormData(form);
    
    showToast('Sending email...', 'warning');
    
    try {
        const response = await fetch(`${API_BASE}/test/email`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                to: data.get('to'),
                subject: data.get('subject'),
                body: data.get('body')
            })
        });
        
        const result = await response.json();
        
        if (response.ok && result.status === 'success') {
            showToast('Email sent successfully!', 'success');
            closeModal();
            setTimeout(loadDashboardData, 2000);
        } else {
            showToast(result.detail || 'Failed to send email', 'error');
        }
    } catch (error) {
        showToast('Error: ' + error.message, 'error');
    }
}

/**
 * Submit WhatsApp form
 */
async function submitWhatsApp(event) {
    event.preventDefault();
    const form = event.target;
    const data = new FormData(form);
    
    showToast('Sending WhatsApp message...', 'warning');
    
    try {
        const response = await fetch(`${API_BASE}/test/whatsapp`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                phone: data.get('phone'),
                message: data.get('message')
            })
        });
        
        const result = await response.json();
        
        if (response.ok && result.status === 'success') {
            showToast('WhatsApp message sent!', 'success');
            closeModal();
            setTimeout(loadDashboardData, 2000);
        } else {
            showToast(result.detail || 'Failed to send message', 'error');
        }
    } catch (error) {
        showToast('Error: ' + error.message, 'error');
    }
}

/**
 * Submit LinkedIn form
 */
async function submitLinkedIn(event) {
    event.preventDefault();
    const form = event.target;
    const data = new FormData(form);
    
    showToast('Creating LinkedIn post...', 'warning');
    
    try {
        const response = await fetch(`${API_BASE}/test/linkedin`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                content: data.get('content')
            })
        });
        
        const result = await response.json();
        
        if (response.ok && result.status === 'success') {
            showToast('LinkedIn post published!', 'success');
            closeModal();
            setTimeout(loadDashboardData, 2000);
        } else {
            showToast(result.detail || 'Failed to create post', 'error');
        }
    } catch (error) {
        showToast('Error: ' + error.message, 'error');
    }
}

/**
 * View logs
 */
function viewLogs(platform) {
    const today = new Date().toISOString().split('T')[0];
    window.open(`../Logs/audit_${today}.json`, '_blank');
}

/**
 * View all activity
 */
function viewAllActivity() {
    window.open('../Logs/', '_blank');
}

/**
 * Show toast notification
 */
function showToast(message, type = 'success') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const iconMap = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        warning: 'fa-exclamation-triangle'
    };
    
    toast.innerHTML = `
        <i class="fas ${iconMap[type]} toast-icon"></i>
        <span class="toast-message">${message}</span>
    `;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'toastSlideIn 0.3s ease reverse';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

/**
 * Animate number counter
 */
function animateNumber(elementId, target) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const duration = 1000;
    const start = parseInt(element.textContent) || 0;
    const increment = (target - start) / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= target) || (increment < 0 && current <= target)) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

/**
 * Capitalize string
 */
function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

// Close modal on outside click
document.getElementById('actionModal')?.addEventListener('click', function(e) {
    if (e.target === this) {
        closeModal();
    }
});

// Help modal functions
function showHelp() {
    const helpModal = document.getElementById('helpModal');
    if (helpModal) {
        helpModal.classList.add('active');
    }
}

function closeHelp() {
    const helpModal = document.getElementById('helpModal');
    if (helpModal) {
        helpModal.classList.remove('active');
    }
}

// Close help modal on outside click
document.getElementById('helpModal')?.addEventListener('click', function(e) {
    if (e.target === this) {
        closeHelp();
    }
});

// Show help on first visit (optional)
// Uncomment to show help automatically on first visit
// if (!localStorage.getItem('helpShown')) {
//     showHelp();
//     localStorage.setItem('helpShown', 'true');
// }
