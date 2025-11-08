import os
import json
import random
from config.settings import PROFILES_DIR, USER_AGENTS, CHROME_MAX_PROFILES

class ProfileManager:
    def __init__(self):
        self.profiles = []
        self.load_or_create_profiles()
    
    def load_or_create_profiles(self):
        """Load existing profiles or create new ones"""
        if not os.path.exists(PROFILES_DIR):
            os.makedirs(PROFILES_DIR)
        
        # Load existing profiles
        existing_profiles = [d for d in os.listdir(PROFILES_DIR) 
                           if os.path.isdir(os.path.join(PROFILES_DIR, d))]
        
        # Create or update profiles
        for i in range(CHROME_MAX_PROFILES):
            profile_name = f"profile_{i+1:03d}"
            profile_path = os.path.join(PROFILES_DIR, profile_name)
            
            # Create directory if doesn't exist
            if profile_name not in existing_profiles:
                os.makedirs(profile_path, exist_ok=True)
            
            # Profile configuration
            profile_data = {
                'id': i + 1,
                'name': profile_name,
                'path': profile_path,
                'user_agent': random.choice(USER_AGENTS),
                'proxy_enabled': False,
                'proxy_config': None,
                'gmail_account': None,
                'created_at': os.path.getctime(profile_path) if os.path.exists(profile_path) else None,
                'last_used': None
            }
            
            # Save/update profile config
            config_file = os.path.join(profile_path, 'config.json')
            if os.path.exists(config_file):
                # Load existing config
                with open(config_file, 'r') as f:
                    existing_config = json.load(f)
                    profile_data.update(existing_config)
            
            # Save config
            with open(config_file, 'w') as f:
                json.dump(profile_data, f, indent=2)
            
            self.profiles.append(profile_data)
    
    def get_profile(self, profile_index):
        """Get profile by index"""
        if 0 <= profile_index < len(self.profiles):
            return self.profiles[profile_index]
        return None
    
    def update_profile(self, profile_index, updates):
        """Update profile configuration"""
        if 0 <= profile_index < len(self.profiles):
            self.profiles[profile_index].update(updates)
            
            # Save to config file
            config_file = os.path.join(self.profiles[profile_index]['path'], 'config.json')
            with open(config_file, 'w') as f:
                json.dump(self.profiles[profile_index], f, indent=2)
            
            return True
        return False
    
    def update_proxy_config(self, profile_index, proxy_config):
        """Update proxy configuration for profile"""
        return self.update_profile(profile_index, {
            'proxy_enabled': True,
            'proxy_config': proxy_config
        })
    
    def update_gmail_account(self, profile_index, gmail_account):
        """Update Gmail account for profile"""
        return self.update_profile(profile_index, {
            'gmail_account': gmail_account
        })
