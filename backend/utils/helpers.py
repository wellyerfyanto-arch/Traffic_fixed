import random
import time
import json
from datetime import datetime

def random_delay(min_delay=1, max_delay=3):
    """Wait for random time between min and max seconds"""
    time.sleep(random.uniform(min_delay, max_delay))

def format_proxy(proxy_string):
    """Format proxy string to dictionary"""
    if not proxy_string:
        return None
    
    parts = proxy_string.split(':')
    if len(parts) == 4:
        return {
            'host': parts[0],
            'port': parts[1],
            'username': parts[2],
            'password': parts[3],
            'type': 'http'  # default type
        }
    elif len(parts) == 2:
        return {
            'host': parts[0],
            'port': parts[1],
            'username': None,
            'password': None,
            'type': 'http'
        }
    return None

def validate_url(url):
    """Validate and format URL"""
    if not url:
        return None
    
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    return url

def calculate_running_time(start_time_str):
    """Calculate running time from start time string"""
    if not start_time_str:
        return "0h 0m"
    
    try:
        start_time = datetime.fromisoformat(start_time_str)
        current_time = datetime.now()
        duration = current_time - start_time
        
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        
        return f"{hours}h {minutes}m"
    except:
        return "0h 0m"

def generate_user_agent():
    """Generate random user agent"""
    from config.settings import USER_AGENTS
    return random.choice(USER_AGENTS)
