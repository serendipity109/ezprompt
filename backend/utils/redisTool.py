import os
import json
import redis

REDIS_HOST = os.environ.get("REDIS_HOST", "cache")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
REDIS_PASS = os.environ.get("REDIS_PASS", "eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81")
# 設定在 1，比較不會有衝突
REDIS_DB = int(os.environ.get("REDIS_DB", "1"))

'''
s0.png:{
    prompt: {pmt},
    nprompt: {npmt},
    dims: {dims},
    CFG: {cfg},
}
'''

class RedisClient:
    def __init__(self):
        self._client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASS,
            db=REDIS_DB,
            health_check_interval=30,
        )

    def ping(self):
        self._client.ping()

    def inspect(self):
        keys = self._client.keys()
        keys = [key.decode('utf-8') for key in keys]
        return keys

    def exists(self, key):
        return self._client.exists(key)

    def set(self, key, value, expire=None):
        if expire is None:
            self._client.set(key, json.dumps(value))
            self._client.persist(key) # 永不過期
        else:
            self._client.set(key, json.dumps(value), ex=expire)

    def append(self, image_name, pmt, npmt, dims, CFG):
        self._client.set(image_name, json.dumps(
            {'prompt': pmt,
             'nprompt': npmt,
             'dims': dims,
             'CFG': CFG
             }
        ))

    def get(self, key):
        res = self._client.get(key)
        if res is None:
            return []
        return json.loads(res)

    def delete(self, key):
        self._client.delete(key)
