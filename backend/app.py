import os
from flask import Flask, render_template, request, jsonify
import json
import time
from datetime import datetime

app = Flask(__name__)

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
    try:
        return render_template('index.html')
    except Exception as e:
        return f"""
        <html>
            <head><title>Auto Traffic System</title></head>
            <body>
                <h1>Auto Traffic System</h1>
                <p>System is running. Template issue: {str(e)}</p>
                <p>Current directory: {os.getcwd()}</p>
                <p>Files in directory: {os.listdir('.')}</p>
                <p>Templates exists: {os.path.exists('templates')}</p>
                {% if os.path.exists('templates') %}
                <p>Files in templates: {os.listdir('templates')}</p>
                {% endif %}
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
        
        # Start system
        system_state['running'] = True
        system_state['start_time'] = datetime.now().isoformat()
        system_state['current_session'] = {
            'target_url': target_url,
            'profiles_count': profiles_count
        }
        
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
        # Simulate some stats for demo
        if system_state['running']:
            system_state['active_profiles'] = 3
            system_state['total_visits'] += 1
            
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
        
        # Simulate profile generation
        profiles = []
        for i in range(min(count, 10)):
            profiles.append({
                'id': i + 1,
                'name': f'profile_{i+1:03d}',
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'status': 'Ready'
            })
        
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

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs('chrome_profiles', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
