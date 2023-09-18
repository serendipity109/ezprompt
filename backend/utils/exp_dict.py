import threading
from collections import defaultdict
import time


class ExpiringDict:
    def __init__(self, default_ttl=3600):
        self.data = defaultdict(lambda: (None, time.time() + default_ttl))
        self.lock = threading.Lock()

    def __getitem__(self, key):
        with self.lock:
            value, expiration_time = self.data[key]
            if expiration_time < time.time():
                del self.data[key]
                raise KeyError("Key not found or has expired")
            return value

    def __setitem__(self, key, value, ttl=None):
        if ttl is None:
            ttl = 3600
        expiration_time = time.time() + ttl
        with self.lock:
            self.data[key] = (value, expiration_time)

    def __delitem__(self, key):
        with self.lock:
            del self.data[key]

    def __contains__(self, key):
        with self.lock:
            if key not in self.data:
                return False
            value, expiration_time = self.data[key]
            if expiration_time < time.time():
                del self.data[key]
                return False
            return True

    def keys(self):
        with self.lock:
            current_time = time.time()
            # 清除过期键
            for key, (_, expiration_time) in list(self.data.items()):
                if expiration_time < current_time:
                    del self.data[key]
            return list(self.data.keys())
