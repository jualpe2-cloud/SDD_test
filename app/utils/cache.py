class CacheManager:
    def __init__(self, redis_client=None):
        self.cache = {}  # In-memory cache
        self.redis_client = redis_client  # Redis client for caching

    def set(self, key, value, timeout=None):
        if self.redis_client:
            self.redis_client.set(key, value, timeout=timeout)
        self.cache[key] = value

    def get(self, key):
        if self.redis_client:
            value = self.redis_client.get(key)
            if value is not None:
                return value
        return self.cache.get(key)

    def delete(self, key):
        if self.redis_client:
            self.redis_client.delete(key)
        if key in self.cache:
            del self.cache[key]

    def clear(self):
        if self.redis_client:
            self.redis_client.flushall()  # Clear Redis cache
        self.cache.clear()  # Clear in-memory cache
