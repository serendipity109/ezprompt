import os
import json
import redis
from typing import Optional, Any, List


class RedisClient:
    def __init__(self):
        REDIS_HOST = os.environ.get("REDIS_HOST", "")
        REDIS_PORT = os.environ.get("REDIS_PORT", "")
        REDIS_PASS = os.environ.get("REDIS_PASSWORD", "")
        # 設定在 1，比較不會有衝突
        REDIS_DB = int(os.environ.get("REDIS_DB", "1"))

        try:
            self._client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                password=REDIS_PASS,
                db=REDIS_DB,
                health_check_interval=30,
            )
            if not self.ping():
                raise redis.ConnectionError
        except redis.ConnectionError:
            print("Failed to connect to Redis server")

    def ping(self) -> bool:
        try:
            return self._client.ping()
        except redis.ConnectionError:
            print("Lost connection to Redis server")
            return False

    def inspect(self) -> List[str]:
        try:
            keys = self._client.keys()
            keys = [key.decode("utf-8") for key in keys]
            return keys
        except Exception as e:
            print(f"Failed to inspect keys: {e}")
            return []

    def exists(self, key: str) -> int:
        try:
            return self._client.exists(key)
        except Exception as e:
            print(f"Failed to check key: {e}")
            return 0

    def set(self, key: str, value: Any, expire: Optional[int] = None):
        try:
            self._client.set(key, json.dumps(value), ex=expire)
        except Exception as e:
            print(f"Failed to set key: {e}")

    def set_hash(self, key: str, mapping: dict):
        try:
            for field, value in mapping.items():
                self._client.hset(key, field, json.dumps(value))
        except Exception as e:
            print(f"Failed to set hash: {e}")

    def append(self, image_name: str, pmt: str, npmt: str, dims: str, CFG: str):
        try:
            self._client.set(
                image_name,
                json.dumps({"prompt": pmt, "nprompt": npmt, "dims": dims, "CFG": CFG}),
            )
        except Exception as e:
            print(f"Failed to append key: {e}")

    def get(self, key: str) -> Any:
        try:
            res = self._client.get(key)
            if res is None:
                return []
            return json.loads(res)
        except Exception as e:
            print(f"Failed to get key: {e}")
            return None

    def get_hash(self, key: str) -> dict:
        try:
            res = self._client.hgetall(key)
            # 将结果的字节键值对转换为字符串
            res = {k.decode('utf-8'): json.loads(v.decode('utf-8')) for k, v in res.items()}
            return res
        except Exception as e:
            print(f"Failed to get hash: {e}")
            return {}

    def delete(self, key: str) -> int:
        try:
            return self._client.delete(key)
        except Exception as e:
            print(f"Failed to delete key: {e}")
            return 0
