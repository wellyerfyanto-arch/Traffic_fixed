from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import json
import os
import threading
import time
from datetime import datetime
from models.profile_manager import ProfileManager
from services.browser_controller import BrowserController
from services.traffic_actions import TrafficActions
from config.settings import CHROME_MAX_PROFILES, MIN_VISIT_TIME, MAX_VISIT_TIME

app = Flask(__name__)
CORS(app)

# Global system state
system_state = {
    'running': False,
    'active_profiles': 0,
    'total_visits': 0,
    'start_time': None,
    'current_session': None
}

# Configuration file
CONFIG_FILE = 'system_config.json'

@app.route('/')
def index():
    return render_template('index.html')

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
        
        return jsonify({'status': 'success', 'message': f'{config_type} configuration saved'})
    except Exception as e:
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
        
        thread = threading.Thread(target=run_traffic_system, args=(target_url, profiles_count))
        thread.daemon = True
        thread.start()
        
        return jsonify({'status': 'success', 'message': 'Traffic system started'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/system/stop', methods=['POST'])
def stop_system():
    try:
        system_state['running'] = False
        system_state['current_session'] = None
        return jsonify({'status': 'success', 'message': 'Traffic system stopped'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/system/status', methods=['GET'])
def get_system_status():
    try:
        return jsonify({
            'status': 'success',
            'system_state': system_state
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/profiles/generate', methods=['POST'])
def generate_profiles():
    try:
        data = request.json
        count = data.get('count', 10)
        
        profile_manager = ProfileManager()
        # This will generate profiles on demand
        profiles = profile_manager.profiles[:count]
        
        return jsonify({
            'status': 'success', 
            'message': f'Generated {len(profiles)} profiles',
            'profiles': profiles
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/proxy/test', methods=['POST'])
def test_proxies():
    try:
        # Simulate proxy testing
        time.sleep(2)
        return jsonify({
            'status': 'success', 
            'message': 'Proxy test completed',
            'results': {
                'working': 8,
                'failed': 2,
                'total': 10
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

def run_traffic_system(target_url, profiles_count):
    """Background function to run traffic system"""
    profile_manager = ProfileManager()
    
    while system_state['running']:
        try:
            # Run sessions for each profile
            for i in range(min(profiles_count, len(profile_manager.profiles))):
                if not system_state['running']:
                    break
                    
                run_traffic_session(i, target_url)
                system_state['total_visits'] += 1
                
                # Stagger between profiles
                time.sleep(10)
            
            # Wait before next cycle
            if system_state['running']:
                time.sleep(3600)  # 1 hour between cycles
                
        except Exception as e:
            print(f"Error in traffic system: {e}")
            time.sleep(60)

def run_traffic_session(profile_index, target_url):
    """Run traffic session for a single profile"""
    try:
        profile_manager = ProfileManager()
        profile = profile_manager.get_profile(profile_index)
        
        if not profile:
            return
        
        browser = BrowserController(profile)
        
        if browser.start_browser():
            # Check data leak
            if browser.check_data_leak():
                traffic = TrafficActions(browser)
                
                # Execute traffic actions
                if traffic.search_and_open_url(target_url):
                    traffic.handle_popups()
                    traffic.random_scroll(MIN_VISIT_TIME, MAX_VISIT_TIME)
                    traffic.slow_scroll(20)
                    traffic.click_random_ads()
                    traffic.navigate_home()
                    traffic.clear_cache()
            
            browser.close_browser()
            
    except Exception as e:
        print(f"Error in session {profile_index}: {e}")

if __name__ == '__main__':
    # Ensure profiles directory exists
    os.makedirs('chrome_profiles', exist_ok=True)
    
    app.run(host='0.0.0.0', port=5000, debug=False)
