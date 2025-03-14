# Add a new file: smartman/cache.py

import os
import json
import hashlib
from datetime import datetime, timedelta

class ResponseCache:
    def __init__(self, cache_dir=None, ttl_hours=24):
        if cache_dir is None:
            cache_dir = os.path.expanduser('~/.smartman/cache')
        self.cache_dir = cache_dir
        self.ttl = timedelta(hours=ttl_hours)
        
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    def get_cache_key(self, text):
        """Generate a unique cache key for the text."""
        return hashlib.md5(text.encode('utf-8')).hexdigest()
        
    def get_cached_response(self, prompt_text, action_type):
        """Get cached response if available and not expired."""
        cache_key = self.get_cache_key(f"{action_type}:{prompt_text}")
        cache_file = os.path.join(self.cache_dir, cache_key)
        
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                data = json.load(f)
                
            # Check if cache is valid
            cached_time = datetime.fromisoformat(data['timestamp'])
            if datetime.now() - cached_time < self.ttl:
                return data['response']
                
        return None
        
    def cache_response(self, prompt_text, action_type, response):
        """Cache the response for future use."""
        cache_key = self.get_cache_key(f"{action_type}:{prompt_text}")
        cache_file = os.path.join(self.cache_dir, cache_key)
        
        with open(cache_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'response': response
            }, f)