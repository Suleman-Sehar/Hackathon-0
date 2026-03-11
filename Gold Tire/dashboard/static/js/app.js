// Gold Tier Dashboard - Real-time Control Center
const API_BASE = '/api/v1';
let refreshInterval;

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    console.log('🥇 Gold Tier Dashboard Initialized');
    updateDateTime();
    loadAllData();
    
    // Auto-refresh every 10 seconds
    refreshInterval = setInterval(loadAllData, 10000);
    
    // Update datetime every second
    setInterval(updateDateTime, 1000);
});

// Update datetime display
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

// Load all dashboard data
async function loadAllData() {
    try {
        await Promise.all([
            loadMetrics(),
            loadRalphWiggumState(),
            loadDomainStats(),
            loadSocialStatus(),
            loadActivityFeed(),
            loadAlerts()
        ]);
        showToast('Dashboard updated', 'success');
    } catch (error) {
        console.error('Failed to load data:', error);
        showToast('Failed to refresh dashboard', 'error');
    }
}

// Refresh all data manually
function refreshAllData() {
    const btn = document.querySelector('.btn-refresh');
    if (btn) {
        btn.style.animation = 'spin 1s linear';
        setTimeout(() => btn.style.animation = '', 1000);
    }
    loadAllData();
}

// Load metrics
async function loadMetrics() {
    try {
        const response = await fetch(`${API_BASE}/metrics`);
        const metrics = await response.json();
        
        // Update metric cards
        animateNumber('metricTasks', metrics.tasks_completed);
        animateNumber('metricRunning', metrics.tasks_running);
        animateNumber('metricSocial', metrics.social_posts);
        animateNumber('metricFB', metrics.facebook_posts);
        animateNumber('metricIG', metrics.instagram_posts);
        animateNumber('metricTW', metrics.twitter_posts);
        document.getElementById('metricRevenue').textContent = `PKR ${metrics.revenue.toLocaleString()}`;
        document.getElementById('metricProfit').textContent = `PKR ${metrics.profit.toLocaleString()}`;
        animateNumber('metricLoop', metrics.loop_iterations);
        document.getElementById('metricCurrentTask').textContent = metrics.current_task || 'None';
        animateNumber('metricErrors', metrics.errors);
        document.getElementById('metricUptime').textContent = metrics.uptime;
        
    } catch (error) {
        console.error('Failed to load metrics:', error);
    }
}

// Load Ralph Wiggum state
async function loadRalphWiggumState() {
    try {
        const response = await fetch(`${API_BASE}/ralph-wiggum/state`);
        const state = await response.json();
        
        const statusEl = document.getElementById('ralphStatus');
        const iterationEl = document.getElementById('ralphIteration');
        const taskEl = document.getElementById('ralphTask');
        
        if (statusEl) {
            const statusText = state.status === 'running' ? 'RUNNING' : 'IDLE';
            const statusClass = state.status === 'running' ? 'status-running' : '';
            statusEl.innerHTML = `Status: <span class="${statusClass}">${statusText}</span> | Iteration: <span id="ralphIteration">${state.iteration}</span> | Task: <span id="ralphTask">${state.current_task || 'None'}</span>`;
        }
        
        if (iterationEl) iterationEl.textContent = state.iteration;
        if (taskEl) taskEl.textContent = state.current_task || 'None';
        
    } catch (error) {
        console.error('Failed to load Ralph Wiggum state:', error);
    }
}

// Control Ralph Wiggum
async function controlRalph(action) {
    try {
        const response = await fetch(`${API_BASE}/ralph-wiggum/control`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showToast(`Ralph Wiggum: ${result.message}`, 'success');
            setTimeout(loadRalphWiggumState, 2000);
        } else {
            showToast(`Error: ${result.detail}`, 'error');
        }
    } catch (error) {
        showToast('Error: ' + error.message, 'error');
    }
}

// Load domain statistics
async function loadDomainStats() {
    try {
        const response = await fetch(`${API_BASE}/domains`);
        const stats = await response.json();
        
        document.getElementById('personalTasks').textContent = stats.personal.active_tasks;
        document.getElementById('personalStatus').textContent = stats.personal.status;
        document.getElementById('businessTasks').textContent = stats.business.active_tasks;
        document.getElementById('businessStatus').textContent = stats.business.status;
        
    } catch (error) {
        console.error('Failed to load domain stats:', error);
    }
}

// Load social media status
async function loadSocialStatus() {
    try {
        const response = await fetch(`${API_BASE}/social/status`);
        const status = await response.json();
        
        // Update platform cards
        updateSocialCard('socialFacebook', status.platforms.facebook);
        updateSocialCard('socialInstagram', status.platforms.instagram);
        updateSocialCard('socialTwitter', status.platforms.twitter);
        
    } catch (error) {
        console.error('Failed to load social status:', error);
    }
}

function updateSocialCard(cardId, isConnected) {
    const card = document.getElementById(cardId);
    if (card) {
        const statusEl = card.querySelector('.social-status');
        if (statusEl) {
            if (isConnected) {
                statusEl.className = 'social-status connected';
                statusEl.innerHTML = '<div class="status-dot"></div><span>Connected</span>';
            } else {
                statusEl.className = 'social-status disconnected';
                statusEl.innerHTML = '<div class="status-dot"></div><span>Disconnected</span>';
            }
        }
    }
}

// Trigger social post
async function triggerPost(platform) {
    showToast(`Opening ${platform} poster...`, 'info');
    // This would open a modal or redirect to posting interface
    setTimeout(() => {
        showToast(`${platform} post interface opened`, 'success');
    }, 1000);
}

// Load activity feed
async function loadActivityFeed() {
    const feedEl = document.getElementById('activityFeed');
    
    try {
        const response = await fetch(`${API_BASE}/activity?limit=10`);
        const logs = await response.json();
        
        if (logs.length === 0) {
            feedEl.innerHTML = `
                <div class="loading-spinner">
                    <i class="fas fa-inbox" style="font-size: 3rem; color: var(--text-secondary); margin-bottom: 1rem;"></i>
                    <p>No recent activity</p>
                </div>
            `;
            return;
        }
        
        feedEl.innerHTML = logs.map(log => createActivityItem(log)).join('');
        
    } catch (error) {
        console.error('Failed to load activity:', error);
        feedEl.innerHTML = '<div class="loading-spinner"><p>Error loading activity</p></div>';
    }
}

function createActivityItem(log) {
    const statusClass = log.status === 'success' ? 'success' : 'error';
    const time = new Date(log.timestamp).toLocaleTimeString();
    
    return `
        <div class="activity-item">
            <div class="activity-header">
                <div class="activity-title">${log.action.replace(/_/g, ' ').toUpperCase()}</div>
                <div class="activity-status ${statusClass}">${log.status}</div>
            </div>
            <div class="activity-time"><i class="far fa-clock"></i> ${time}</div>
        </div>
    `;
}

// Load alerts
async function loadAlerts() {
    const alertsEl = document.getElementById('alertsPanel');
    
    try {
        const response = await fetch(`${API_BASE}/alerts`);
        const data = await response.json();
        
        if (data.alerts.length === 0) {
            alertsEl.innerHTML = `
                <div style="text-align: center; padding: 2rem; color: var(--success);">
                    <i class="fas fa-check-circle" style="font-size: 3rem; margin-bottom: 1rem;"></i>
                    <p style="font-size: 1.25rem; font-weight: 700;">NO ACTIVE ALERTS</p>
                    <p style="color: var(--text-secondary);">All systems operational</p>
                </div>
            `;
        } else {
            alertsEl.innerHTML = data.alerts.map(alert => `
                <div class="alert-item">
                    <div class="alert-icon">
                        <i class="fas fa-exclamation-triangle"></i>
                    </div>
                    <div>
                        <div style="font-weight: 700; color: var(--warning);">${alert.type} ALERT</div>
                        <div style="font-size: 0.875rem; color: var(--text-secondary);">${alert.file}</div>
                        <div style="font-size: 0.75rem; color: var(--text-secondary);">${new Date(alert.created).toLocaleString()}</div>
                    </div>
                </div>
            `).join('');
        }
        
    } catch (error) {
        console.error('Failed to load alerts:', error);
        alertsEl.innerHTML = '<div class="loading-spinner"><p>Error loading alerts</p></div>';
    }
}

// Trigger CEO briefing
async function triggerBriefing() {
    try {
        const response = await fetch(`${API_BASE}/briefing/trigger`, {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showToast('CEO Briefing generation started', 'success');
        } else {
            showToast(`Error: ${result.detail}`, 'error');
        }
    } catch (error) {
        showToast('Error: ' + error.message, 'error');
    }
}

// View all activity
function viewAllActivity() {
    const logsDir = 'AI_Employee_Vault/Logs/';
    showToast(`Opening logs folder: ${logsDir}`, 'info');
    // In real implementation, this would open the folder
}

// View logs
function viewLogs() {
    showToast('Opening audit logs...', 'info');
}

// Open documentation
function openDocs() {
    showToast('Opening documentation...', 'info');
}

// Show toast notification
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const iconMap = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        info: 'fa-info-circle',
        warning: 'fa-exclamation-triangle'
    };
    
    toast.innerHTML = `
        <i class="fas ${iconMap[type]}" style="font-size: 1.5rem;"></i>
        <span style="flex: 1; font-weight: 600;">${message}</span>
    `;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// Animate number counter
function animateNumber(elementId, target) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const start = parseInt(element.textContent.replace(/,/g, '')) || 0;
    if (start === target) return;
    
    const duration = 1000;
    const increment = (target - start) / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= target) || (increment < 0 && current <= target)) {
            element.textContent = target.toLocaleString();
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current).toLocaleString();
        }
    }, 16);
}
