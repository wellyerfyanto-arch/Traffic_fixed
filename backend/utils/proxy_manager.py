import os
import json
import random
from config.settings import PROFILES_DIR, USER_AGENTS

class ProfileManager:
    def __init__(self):
        self.profiles = []
    
    def get_profile(self, profile_index):
        """Get profile by index - simplified for demo"""
        if 0 <= profile_index < 10:
            return {
                'id': profile_index + 1,
                'name': f'profile_{profile_index+1:03d}',
                'user_agent': random.choice(USER_AGENTS),
                'proxy_enabled': False
            }
        return None
