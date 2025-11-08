import os
from dotenv import load_dotenv

load_dotenv()

# Basic Configuration
CHROME_MAX_PROFILES = int(os.getenv('CHROME_MAX_PROFILES', 10))
MIN_VISIT_TIME = int(os.getenv('MIN_VISIT_TIME', 30))
MAX_VISIT_TIME = int(os.getenv('MAX_VISIT_TIME', 120))
SCROLL_DURATION = int(os.getenv('SCROLL_DURATION', 20))

# Paths
PROFILES_DIR = os.path.join(os.getcwd(), 'chrome_profiles')
CONFIG_DIR = os.path.join(os.getcwd(), 'config')

# User Agents Pool
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
]

# Default Proxy Configuration
DEFAULT_PROXIES = [
    "192.168.1.1:8080:user:pass",
    "192.168.1.2:8080:user:pass",
    "192.168.1.3:8080:user:pass"
]
