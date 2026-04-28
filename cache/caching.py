import json

class Cache:
    def __init__(self):
        self.cache = {}

    def get_cache(self, key):
        return self.cache.get(key)
    
    def add_cache(self, key, value):
        self.cache[key] = value
    
    def save_cache(self, filename="cache/cache.json"):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(self.cache, file, indent=4, ensure_ascii=False)
    
    def load_cache(self, filename="cache/cache.json"):
        with open(filename, "r", encoding="utf-8") as file:
            self.cache = json.load(file)