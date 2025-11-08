// Global variables
let systemState = {
    running: false,
    activeProfiles: 0,
    totalVisits: 0,
    successRate: 0,
    runningTime: '0h 0m'
};

// API Base URL
const API_BASE = window.location.origin + '/api';

// Tab navigation
function openTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from all buttons
    document.querySelectorAll('.nav-tab').forEach(button => {
        button.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(tabName).classList.add('active');
    
    // Add active class to clicked button
    event.currentTarget.classList.add('active');
}

// System control functions
async function startSystem() {
    const url = document.getElementById('quickStartUrl').value;
    
    if (!url) {
        alert('Please enter a target URL');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/system/start`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                target_url: url,
                profiles_count: 5
            })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            alert('System started successfully!');
            updateSystemStatus(true);
        } else {
            alert('Error: ' + data.message);
        }
    } catch (error) {
        alert('Error starting system: ' + error.message);
    }
}

async function stopSystem() {
    try {
        const response = await fetch(`${API_BASE}/system/stop`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            alert('System stopped successfully!');
            updateSystemStatus(false);
        } else {
            alert('Error: ' + data.message);
        }
    } catch (error) {
        alert('Error stopping system: ' + error.message);
    }
}

async function refreshStats() {
    try {
        const response = await fetch(`${API_BASE}/system/status`);
        const data = await response.json();
        
        if (data.status === 'success') {
            updateDashboard(data.system_state);
        }
    } catch (error) {
        console.error('Error refreshing stats:', error);
    }
}

// Update dashboard with current data
function updateDashboard(state) {
    systemState = state;
    
    // Update DOM elements
    document.getElementById('activeProfiles').textContent = state.active_profiles || 0;
    document.getElementById('totalVisits').textContent = state.total_visits || 0;
    document.getElementById('runningTime').textContent = state.running_time || '0h 0m';
    
    // Update system status
    updateSystemStatus(state.running);
}

function updateSystemStatus(isRunning) {
    const indicator = document.getElementById('systemStatusIndicator');
    const statusText = document.getElementById('systemStatusText');
    const progressBar = document.getElementById('systemProgress');
    
    if (isRunning) {
        indicator.className = 'status-indicator status-active';
        statusText.textContent = 'Running';
        progressBar.style.width = '75%';
    } else {
        indicator.className = 'status-indicator status-inactive';
        statusText.textContent = 'Stopped';
        progressBar.style.width = '0%';
    }
}

// Configuration management
async function saveConfig(type, config) {
    try {
        const response = await fetch(`${API_BASE}/config/save`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                type: type,
                config: config
            })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            showNotification('Configuration saved successfully!', 'success');
            return true;
        } else {
            showNotification('Error saving configuration: ' + data.message, 'error');
            return false;
        }
    } catch (error) {
        showNotification('Error saving configuration: ' + error.message, 'error');
        return false;
    }
}

async function loadConfig() {
    try {
        const response = await fetch(`${API_BASE}/config/load`);
        const data = await response.json();
        
        if (data.status === 'success') {
            return data.config;
        } else {
            showNotification('Error loading configuration: ' + data.message, 'error');
            return {};
        }
    } catch (error) {
        showNotification('Error loading configuration: ' + error.message, 'error');
        return {};
    }
}

// Utility functions
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()">×</button>
    `;
    
    // Add styles if not already added
    if (!document.querySelector('#notification-styles')) {
        const styles = document.createElement('style');
        styles.id = 'notification-styles';
        styles.textContent = `
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 15px 20px;
                border-radius: 5px;
                color: white;
                z-index: 1000;
                display: flex;
                justify-content: space-between;
                align-items: center;
                min-width: 300px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                animation: slideIn 0.3s ease;
            }
            .notification-success { background: #27ae60; }
            .notification-error { background: #e74c3c; }
            .notification-info { background: #3498db; }
            .notification button {
                background: none;
                border: none;
                color: white;
                font-size: 18px;
                cursor: pointer;
                margin-left: 10px;
            }
            @keyframes slideIn {
                from { transform: translateX(100%); }
                to { transform: translateX(0); }
            }
        `;
        document.head.appendChild(styles);
    }
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    // Load initial configuration
    loadConfig().then(config => {
        // Populate form fields with loaded config
        console.log('Loaded configuration:', config);
    });
    
    // Start periodic stats refresh
    setInterval(refreshStats, 5000);
    
    // Initial stats load
    refreshStats();
});
