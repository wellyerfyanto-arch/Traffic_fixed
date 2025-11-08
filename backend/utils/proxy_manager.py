import random
import requests
from utils.helpers import format_proxy

class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.current_index = 0
    
    def load_proxies(self, proxy_list):
        """Load proxies from list of strings"""
        self.proxies = []
        
        for proxy_str in proxy_list:
            proxy = format_proxy(proxy_str)
            if proxy:
                self.proxies.append(proxy)
    
    def get_next_proxy(self, strategy='roundrobin'):
        """Get next proxy based on strategy"""
        if not self.proxies:
            return None
        
        if strategy == 'random':
            return random.choice(self.proxies)
        elif strategy == 'roundrobin':
            proxy = self.proxies[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.proxies)
            return proxy
        else:  # sticky (always return first)
            return self.proxies[0]
    
    def test_proxy(self, proxy, test_url="https://api.ipify.org?format=json"):
        """Test if proxy is working"""
        try:
            proxies = {
                'http': f"http://{proxy['username']}:{proxy['password']}@{proxy['host']}:{proxy['port']}",
                'https': f"https://{proxy['username']}:{proxy['password']}@{proxy['host']}:{proxy['port']}"
            }
            
            response = requests.get(test_url, proxies=proxies, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def test_all_proxies(self):
        """Test all loaded proxies"""
        results = {
            'working': [],
            'failed': []
        }
        
        for proxy in self.proxies:
            if self.test_proxy(proxy):
                results['working'].append(proxy)
            else:
                results['failed'].append(proxy)
        
        return results
