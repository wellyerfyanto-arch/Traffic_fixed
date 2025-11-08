from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import random

class TrafficActions:
    def __init__(self, browser_controller):
        self.bc = browser_controller
        self.driver = browser_controller.driver
        self.wait = browser_controller.wait
    
    def handle_popups(self):
        """Handle various popups and notifications"""
        close_selectors = [
            "button[aria-label*='close' i]",
            "button[class*='close' i]",
            "button[class*='dismiss' i]",
            ".close-btn",
            "#close-button",
            "[aria-label='Close']",
            "[title='Close']",
            "button:contains('Tutup')",
            "button:contains('Close')",
            "button:contains('Lanjutkan')",
            "button:contains('Continue')",
            "button:contains('Skip')",
            "button:contains('Lewati')",
            "div[role='button'][aria-label*='close' i]"
        ]
        
        for selector in close_selectors:
            try:
                # Try CSS selector first
                close_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                if close_btn.is_displayed():
                    close_btn.click()
                    time.sleep(1)
                    break
            except:
                continue
        
        # Handle JavaScript alerts
        try:
            alert = self.driver.switch_to.alert
            alert.dismiss()
            time.sleep(1)
        except:
            pass
    
    def search_and_open_url(self, url):
        """Search and open the top related URL"""
        try:
            # Use Google search to find related URLs
            search_query = url.replace('https://', '').replace('http://', '').split('/')[0]
            self.driver.get(f"https://www.google.com/search?q={search_query}")
            time.sleep(3)
            
            # Handle Google consent if present
            self.handle_google_consent()
            
            # Click on the first organic search result (skip ads)
            results = self.driver.find_elements(By.CSS_SELECTOR, "div.g a")
            if results:
                # Skip ads and take first organic result
                organic_results = [r for r in results if 'googleadservices.com' not in r.get_attribute('href')]
                if organic_results:
                    organic_results[0].click()
                    time.sleep(5)
                    return True
            
            return False
            
        except Exception as e:
            print(f"Error searching URL: {e}")
            # Fallback: go directly to URL
            try:
                self.driver.get(url)
                time.sleep(5)
                return True
            except:
                return False
    
    def handle_google_consent(self):
        """Handle Google consent popup"""
        consent_selectors = [
            "button[aria-label*='Accept all']",
            "button:contains('Accept all')",
            "button:contains('I agree')",
            "#L2AGLb"
        ]
        
        for selector in consent_selectors:
            try:
                consent_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                if consent_btn.is_displayed():
                    consent_btn.click()
                    time.sleep(2)
                    break
            except:
                continue
    
    def random_scroll(self, min_time, max_time):
        """Perform random scrolling"""
        scroll_duration = random.randint(min_time, max_time)
        start_time = time.time()
        
        while time.time() - start_time < scroll_duration:
            # Random scroll pattern
            scroll_height = random.randint(200, 600)
            scroll_direction = random.choice([-1, 1])  # up or down
            
            self.driver.execute_script(f"window.scrollBy(0, {scroll_height * scroll_direction});")
            
            # Random pause between scrolls
            time.sleep(random.uniform(0.5, 2))
            
            # Occasionally move mouse
            if random.random() < 0.3:
                actions = ActionChains(self.driver)
                actions.move_by_offset(random.randint(10, 100), random.randint(10, 100))
                actions.perform()
    
    def slow_scroll(self, duration=20):
        """Slow scroll for specified duration"""
        start_time = time.time()
        scroll_position = 0
        
        while time.time() - start_time < duration:
            scroll_increment = random.randint(30, 80)
            scroll_position += scroll_increment
            
            self.driver.execute_script(f"window.scrollTo(0, {scroll_position});")
            time.sleep(0.3)
    
    def click_random_ads(self):
        """Click on random Google ads if available"""
        ad_selectors = [
            "a[href*='googleadservices']",
            "[data-ad-client]",
            ".adsbygoogle
