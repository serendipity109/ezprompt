import os
import json
import redis
from typing import Optional, Any, List
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
            logger.exception("Failed to connect to Redis server")
            raise redis.ConnectionError

    def ping(self) -> bool:
        try:
            return self._client.ping()
        except redis.ConnectionError:
            return False

    def inspect(self) -> List[str]:
        try:
            keys = self._client.keys()
            keys = [key.decode("utf-8") for key in keys]
            return keys
        except Exception as e:
            logger.exception(f"Failed to inspect keys: {e}")
            raise Exception(f"Failed to inspect keys: {e}")

    def exists(self, key: str) -> int:
        try:
            return self._client.exists(key)
        except Exception as e:
            logger.exception(f"Failed to check key: {e}")
            return 0

    def set(self, key: str, value: Any, expire: Optional[int] = None):
        try:
            self._client.set(key, json.dumps(value), ex=expire)
        except Exception as e:
            logger.exception(f"Failed to set key: {e}")
            raise Exception(f"Failed to set key: {e}")

    def set_hash(self, key: str, mapping: dict):
        try:
            for field, value in mapping.items():
                self._client.hset(key, field, json.dumps(value))
        except Exception as e:
            logger.exception(f"Failed to set hash: {e}")
            raise Exception(f"Failed to set hash: {e}")

    def append(self, image_name: str, pmt: str, npmt: str, dims: str, CFG: str):
        try:
            self._client.set(
                image_name,
                json.dumps({"prompt": pmt, "nprompt": npmt, "dims": dims, "CFG": CFG}),
            )
        except Exception as e:
            logger.exception(f"Failed to append key: {e}")
            raise Exception(f"Failed to append key: {e}")

    def get(self, key: str) -> Any:
        try:
            res = self._client.get(key)
            if res is None:
                return []
            return json.loads(res)
        except Exception as e:
            logger.exception(f"Failed to get key: {e}")
            raise Exception(f"Failed to get key: {e}")

    def get_hash(self, key: str) -> dict:
        try:
            res = self._client.hgetall(key)
            # 将结果的字节键值对转换为字符串
            res = {
                k.decode("utf-8"): json.loads(v.decode("utf-8")) for k, v in res.items()
            }
            return res
        except Exception as e:
            logger.exception(f"Failed to get hash: {e}")
            raise Exception(f"Failed to get hash: {e}")

    def delete(self, key: str) -> int:
        try:
            self._client.delete(key)
            logger.info(f"Successfully delete {key}")
            return {"code": 200, "message": f"Successfully delete {key}"}
        except Exception as e:
            logger.exception(f"Failed to delete key: {e}")
            raise Exception(f"Failed to delete key: {e}")


# map = {
#     "prompt": "(1girl:2), (chest upward long shot portrait:1.5), (perfectly-centered portrait:2), pose like anchor, (jazz bar beautiful wood stage dark background:1.5), (looking_at_viewer:1.5), (close mouth), (smart and casual:1.5), short_hair, professional, (elegant:1.3), hyper-realistic, nikon RAW photo,8 k,Fujifilm XT3, (masterpiece), best quality, realistic, photorealistic,ultra detailed,extremely detailed face,mina",
#     "nprompt": "(2 girls:2), (two girls:2), (worst quality:2), (low quality:2), (tilting head:2), (fingers:2), (cropped head), low contrast, underexposed, overexposed, ((poorly drawn face)), (((mutation))), (((deformed))), (((tiling))), ((naked)), ((tile)), ((fleshpile)), ((ugly)), (((abstract))), blurry, ((bad anatomy)), ((bad proportions)), ((extra limbs)), cloned face, glitchy, ((double torso)), (ugly face)), (nsfw)",
#     "CFG": "7",
#     "batch": ["http://192.168.3.16:9527/media/mock/s14.png", "http://192.168.3.16:9527/media/mock/s14_1.png"],
#     "model": "sdxl",
#     "size": "768x1024",
# }
# redis_client.set_hash('s14', map)
