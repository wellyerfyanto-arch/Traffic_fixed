import os
from flask import Flask, render_template, request, jsonify
import json
import time
import threading
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global system state
system_state = {
    'running': False,
    'active_profiles': 0,
    'total_visits': 0,
    'start_time': None,
    'current_session': None,
    'last_error': None
}

# Configuration file
CONFIG_FILE = 'system_config.json'

# Simple profile manager (without actual Chrome for now)
class SimpleProfileManager:
    def __init__(self):
        self.profiles = []
        self.create_profiles()
    
    def create_profiles(self):
        """Create simple profiles for testing"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        ]
        
        for i in range(10):
            self.profiles.append({
                'id': i + 1,
                'name': f'profile_{i+1:03d}',
                'user_agent': user_agents[i % len(user_agents)],
                'status': 'Ready',
                'proxy_enabled': False
            })
    
    def get_all_profiles(self):
        return self.profiles
    
    def update_profile_status(self, profile_id, status):
        for profile in self.profiles:
            if profile['id'] == profile_id:
                profile['status'] = status
                return True
        return False

profile_manager = SimpleProfileManager()

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"""
        <html>
            <head><title>Auto Traffic System</title></head>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h1>Auto Traffic System - DEMO MODE</h1>
                <p>System is running in DEMO mode. Real traffic simulation is disabled.</p>
                <p>Template error: {str(e)}</p>
                <div style="background: #f5f5f5; padding: 15px; border-radius: 5px; margin-top: 20px;">
                    <h3>System Status:</h3>
                    <p>Running: {system_state['running']}</p>
                    <p>Total Visits: {system_state['total_visits']}</p>
                    <p>Active Profiles: {system_state['active_profiles']}</p>
                    <p>Last Error: {system_state['last_error'] or 'None'}</p>
                </div>
            </body>
        </html>
        """, 500

@app.route('/api/config/save', methods=['POST'])
def save_config():
    try:
        config_data = request.json
        config_type = config_data.get('type')
        config = config_data.get('config', {})
        
        # Load existing config
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                full_config = json.load(f)
        else:
            full_config = {}
        
        # Update specific config section
        full_config[config_type] = config
        
        # Save to file
        with open(CONFIG_FILE, 'w') as f:
            json.dump(full_config, f, indent=2)
        
        logger.info(f"Configuration saved: {config_type}")
        return jsonify({'status': 'success', 'message': f'{config_type} configuration saved'})
    except Exception as e:
        logger.error(f"Error saving config: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/config/load', methods=['GET'])
def load_config():
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
            return jsonify({'status': 'success', 'config': config})
        else:
            return jsonify({'status': 'success', 'config': {}})
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/system/start', methods=['POST'])
def start_system():
    try:
        data = request.json
        target_url = data.get('target_url')
        profiles_count = data.get('profiles_count', 5)
        
        if not target_url:
            return jsonify({'status': 'error', 'message': 'Target URL is required'}), 400
        
        # Start system in background thread
        system_state['running'] = True
        system_state['start_time'] = datetime.now().isoformat()
        system_state['current_session'] = {
            'target_url': target_url,
            'profiles_count': profiles_count
        }
        system_state['last_error'] = None
        
        logger.info(f"Starting traffic system for URL: {target_url} with {profiles_count} profiles")
        
        # Start simulation thread
        thread = threading.Thread(target=run_traffic_simulation, args=(target_url, profiles_count))
        thread.daemon = True
        thread.start()
        
        return jsonify({'status': 'success', 'message': 'Traffic system started in DEMO mode'})
    except Exception as e:
        logger.error(f"Error starting system: {e}")
        system_state['last_error'] = str(e)
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/system/stop', methods=['POST'])
def stop_system():
    try:
        system_state['running'] = False
        system_state['current_session'] = None
        logger.info("Traffic system stopped")
        return jsonify({'status': 'success', 'message': 'Traffic system stopped'})
    except Exception as e:
        logger.error(f"Error stopping system: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/system/status', methods=['GET'])
def get_system_status():
    try:
        # Calculate running time
        running_time = "0h 0m"
        if system_state['start_time']:
            start_time = datetime.fromisoformat(system_state['start_time'])
            current_time = datetime.now()
            duration = current_time - start_time
            hours = duration.seconds // 3600
            minutes = (duration.seconds % 3600) // 60
            running_time = f"{hours}h {minutes}m"
        
        return jsonify({
            'status': 'success',
            'system_state': {
                'running': system_state['running'],
                'active_profiles': system_state['active_profiles'],
                'total_visits': system_state['total_visits'],
                'start_time': system_state['start_time'],
                'running_time': running_time,
                'last_error': system_state['last_error']
            }
        })
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/profiles/generate', methods=['POST'])
def generate_profiles():
    try:
        data = request.json
        count = data.get('count', 10)
        
        # Get profiles from profile manager
        profiles = profile_manager.get_all_profiles()[:count]
        
        logger.info(f"Generated {len(profiles)} profiles")
        
        return jsonify({
            'status': 'success', 
            'message': f'Loaded {len(profiles)} profiles',
            'profiles': profiles
        })
    except Exception as e:
        logger.error(f"Error generating profiles: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/proxy/test', methods=['POST'])
def test_proxies():
    try:
        logger.info("Testing proxies (simulated)")
        time.sleep(2)
        return jsonify({
            'status': 'success', 
            'message': 'Proxy test completed (simulated)',
            'results': {
                'working': 5,
                'failed': 1,
                'total': 6
            }
        })
    except Exception as e:
        logger.error(f"Error testing proxies: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/debug/info', methods=['GET'])
def debug_info():
    """Debug endpoint to check system status"""
    try:
        return jsonify({
            'status': 'success',
            'debug_info': {
                'current_directory': os.getcwd(),
                'files_in_root': os.listdir('.'),
                'templates_exists': os.path.exists('templates'),
                'chrome_profiles_exists': os.path.exists('chrome_profiles'),
                'system_state': system_state,
                'python_version': os.sys.version,
                'environment_variables': {
                    'CHROME_MAX_PROFILES': os.getenv('CHROME_MAX_PROFILES'),
                    'MIN_VISIT_TIME': os.getenv('MIN_VISIT_TIME'),
                    'MAX_VISIT_TIME': os.getenv('MAX_VISIT_TIME')
                }
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

def run_traffic_simulation(target_url, profiles_count):
    """Run simulated traffic in background"""
    logger.info(f"Starting traffic simulation for {target_url}")
    
    cycle_count = 0
    while system_state['running'] and cycle_count < 10:  # Limit cycles for demo
        try:
            cycle_count += 1
            logger.info(f"Starting traffic cycle {cycle_count}")
            
            profiles = profile_manager.get_all_profiles()[:profiles_count]
            
            for i, profile in enumerate(profiles):
                if not system_state['running']:
                    break
                
                # Simulate traffic session
                logger.info(f"Simulating traffic for profile {profile['name']} to {target_url}")
                
                # Update system state
                system_state['active_profiles'] = len(profiles)
                system_state['total_visits'] += 1
                
                # Update profile status
                profile_manager.update_profile_status(profile['id'], 'Active')
                
                # Simulate work being done
                time.sleep(5)  # Simulate 5 seconds of "work"
                
                # Update profile status to completed
                profile_manager.update_profile_status(profile['id'], 'Completed')
                
                logger.info(f"Completed simulation for profile {profile['name']}")
                
                # Stagger between profiles
                if i < len(profiles) - 1:  # Don't sleep after last profile
                    time.sleep(2)
            
            # Wait before next cycle
            if system_state['running']:
                logger.info("Waiting 30 seconds before next cycle...")
                time.sleep(30)  # 30 seconds between cycles for demo
                
        except Exception as e:
            logger.error(f"Error in traffic simulation: {e}")
            system_state['last_error'] = str(e)
            time.sleep(10)
    
    logger.info("Traffic simulation completed")
    system_state['running'] = False

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs('chrome_profiles', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
