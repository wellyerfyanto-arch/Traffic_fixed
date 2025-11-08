import os

# Basic Configuration
CHROME_MAX_PROFILES = int(os.getenv('CHROME_MAX_PROFILES', 10))
MIN_VISIT_TIME = int(os.getenv('MIN_VISIT_TIME', 30))
MAX_VISIT_TIME = int(os.getenv('MAX_VISIT_TIME', 120))

# Paths
PROFILES_DIR = os.path.join(os.getcwd(), 'chrome_profiles')

# User Agents Pool
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]
