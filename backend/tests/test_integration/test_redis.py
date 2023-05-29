import unittest
from utils.redisTool import RedisClient
import pytest


class TestRedisClient(unittest.TestCase):
    def setUp(self):
        self.client = RedisClient()

    @pytest.mark.run(order=1)
    def test_append(self):
        # 檢查有無'test-key'
        self.assertFalse(self.client.exists("image_name"))
        # 新增 mock data
        self.client.append("image_name", "a chubby cat", "ugly", "512x512", 7.0)
        # 檢查有無新增成功
        self.assertTrue(self.client.exists("image_name"))
        # 檢查新增的資料是否符合預期
        mock_input = {
            "prompt": "a chubby cat",
            "nprompt": "ugly",
            "dims": "512x512",
            "CFG": 7.0,
        }
        self.assertEqual(self.client.get("image_name"), mock_input)

    @pytest.mark.run(order=2)
    def test_delete_file(self):
        # 檢查有無'test-key'
        self.assertTrue(self.client.exists("image_name"))
        # 刪除資料
        self.client.delete("image_name")
        # 檢查有無'test-key'
        self.assertFalse(self.client.exists("image_name"))
