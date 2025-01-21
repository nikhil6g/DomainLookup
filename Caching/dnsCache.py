import time

class DNSCache:
    def __init__(self):
        self.cache = {}

    def get(self, domain, query_type):
        """Retrieve a cached record for the given domain and query type."""
        key = (domain, query_type)
        if key in self.cache:
            record = self.cache[key]
            # Check if the record has expired
            if record['expiry'] > time.time():
                return record['data']
            else:
                # Remove expired record
                del self.cache[key]
        return None

    def set(self, domain, query_type, data, ttl):
        """Store a record in the cache."""
        key = (domain, query_type)
        expiry = time.time() + ttl
        self.cache[key] = {'data': data, 'expiry': expiry}

    def clear_expired(self):
        """Remove all expired records from the cache."""
        now = time.time()
        expired_keys = [key for key, record in self.cache.items() if record['expiry'] <= now]
        for key in expired_keys:
            del self.cache[key]

    def clear_all(self):
        """Clear all records from the cache."""
        self.cache.clear()

    def get_all(self):
        """Retrieve all cache records."""
        return {
            (domain, query_type): {'data': record['data'], 'expiry': record['expiry']}
            for (domain, query_type), record in self.cache.items()
        }
