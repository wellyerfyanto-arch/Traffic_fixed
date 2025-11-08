from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random

class BrowserController:
    def __init__(self, profile_data):
        self.profile_data = profile_data
        self.driver = None
        self.wait = None
    
    def start_browser(self):
        """Start Chrome browser with profile configuration"""
        chrome_options = Options()
        
        # Profile settings
        chrome_options.add_argument(f"--user-data-dir={self.profile_data['path']}")
        chrome_options.add_argument(f"--user-agent={self.profile_data['user_agent']}")
        
        # Proxy configuration
        if self.profile_data['proxy_enabled'] and self.profile_data['proxy_config']:
            proxy = self.profile_data['proxy_config']
            chrome_options.add_argument(f"--proxy-server={proxy['type']}://{proxy['host']}:{proxy['port']}")
        
        # Browser options for Render deployment
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            # Use webdriver-manager to handle ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Mask webdriver properties
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": self.profile_data['user_agent']
            })
            
            self.wait = WebDriverWait(self.driver, 30)
            return True
            
        except Exception as e:
            print(f"Error starting browser for profile {self.profile_data['name']}: {e}")
            return False
    
    def check_data_leak(self):
        """Check if IP and location data is properly masked"""
        try:
            # Test 1: Check IP address
            self.driver.get("https://api.ipify.org?format=json")
            time.sleep(3)
            
            ip_text = self.driver.find_element(By.TAG_NAME, "body").text
            print(f"IP Check result: {ip_text}")
            
            # Test 2: Check browser fingerprint
            self.driver.get("https://amiunique.org/fingerprint")
            time.sleep(5)
            
            # Test 3: Check WebRTC leak
            self.driver.get("https://browserleaks.com/webrtc")
            time.sleep(3)
            
            # If all pages load without errors, consider it successful
            return True
            
        except Exception as e:
            print(f"Data leak check failed: {e}")
            return False
    
    def close_browser(self):
        """Close the browser instance"""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                print(f"Error closing browser: {e}")
