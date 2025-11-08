// Configuration management for different tabs

// Profiles Configuration
class ProfilesConfig {
    constructor() {
        this.maxProfiles = 10;
        this.gmailLogin = 'manual';
        this.userAgentMode = 'random';
    }
    
    save() {
        const config = {
            maxProfiles: parseInt(document.getElementById('maxProfiles').value) || 10,
            gmailLogin: document.getElementById('gmailLogin').value,
            userAgentMode: document.getElementById('userAgentMode').value
        };
        
        return saveConfig('profiles', config);
    }
    
    load(config) {
        if (config.maxProfiles) {
            document.getElementById('maxProfiles').value = config.maxProfiles;
        }
        if (config.gmailLogin) {
            document.getElementById('gmailLogin').value = config.gmailLogin;
        }
        if (config.userAgentMode) {
            document.getElementById('userAgentMode').value = config.userAgentMode;
        }
    }
}

// Traffic Configuration
class TrafficConfig {
    constructor() {
        this.targetUrl = '';
        this.visitStrategy = 'search';
        this.minVisitTime = 30;
        this.maxVisitTime = 120;
        this.scrollBehavior = 'random';
        this.clickAds = true;
        this.handlePopups = true;
        this.clearCache = true;
    }
    
    save() {
        const config = {
            targetUrl: document.getElementById('targetUrl').value,
            visitStrategy: document.getElementById('visitStrategy').value,
            minVisitTime: parseInt(document.getElementById('minVisitTime').value) || 30,
            maxVisitTime: parseInt(document.getElementById('maxVisitTime').value) || 120,
            scrollBehavior: document.getElementById('scrollBehavior').value,
            clickAds: document.getElementById('clickAds').checked,
            handlePopups: document.getElementById('handlePopups').checked,
            clearCache: document.getElementById('clearCache').checked
        };
        
        return saveConfig('traffic', config);
    }
    
    load(config) {
        if (config.targetUrl) {
            document.getElementById('targetUrl').value = config.targetUrl;
        }
        if (config.visitStrategy) {
            document.getElementById('visitStrategy').value = config.visitStrategy;
        }
        if (config.minVisitTime) {
            document.getElementById('minVisitTime').value = config.minVisitTime;
        }
        if (config.maxVisitTime) {
            document.getElementById('maxVisitTime').value = config.maxVisitTime;
        }
        if (config.scrollBehavior) {
            document.getElementById('scrollBehavior').value = config.scrollBehavior;
        }
        if (config.clickAds !== undefined) {
            document.getElementById('clickAds').checked = config.clickAds;
        }
        if (config.handlePopups !== undefined) {
            document.getElementById('handlePopups').checked = config.handlePopups;
        }
        if (config.clearCache !== undefined) {
            document.getElementById('clearCache').checked = config.clearCache;
        }
    }
}

// Initialize config managers
const profilesConfig = new ProfilesConfig();
const trafficConfig = new TrafficConfig();

// Export configuration
function exportConfig() {
    loadConfig().then(config => {
        const dataStr = JSON.stringify(config, null, 2);
        const dataBlob = new Blob([dataStr], {type: 'application/json'});
        
        const link = document.createElement('a');
        link.href = URL.createObjectURL(dataBlob);
        link.download = 'traffic_system_config.json';
        link.click();
    });
}

// Import configuration
function importConfig() {
    document.getElementById('configFile').click();
}

// Set up file input for import
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.id = 'configFile';
    fileInput.style.display = 'none';
    fileInput.accept = '.json';
    
    fileInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    const config = JSON.parse(e.target.result);
                    saveConfig('full', config).then(success => {
                        if (success) {
                            showNotification('Configuration imported successfully!', 'success');
                            // Reload the page to reflect changes
                            setTimeout(() => location.reload(), 1000);
                        }
                    });
                } catch (error) {
                    showNotification('Error importing configuration: ' + error.message, 'error');
                }
            };
            reader.readAsText(file);
        }
    });
    
    document.body.appendChild(fileInput);
});
