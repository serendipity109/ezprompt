import unittest
from utils.minioTool import MinioClient
import pytest


class TestMinioClient(unittest.TestCase):
    def setUp(self):
        self.client = MinioClient()

    @pytest.mark.run(order=1)
    def test_upload_file(self):
        # 檢查有無'test-bucket'
        self.assertFalse(self.client.bucket_exist("test-bucket"))
        # 上傳圖檔
        self.client.upload_file("test-bucket", "test.png", "tests/image/test.png")
        # 檢查有無'test-bucket'
        self.assertTrue(self.client.bucket_exist("test-bucket"))
        # 檢查'test-bucket'有無圖檔
        self.assertTrue(self.client.file_in_bucket("test-bucket", "test.png"))

    @pytest.mark.run(order=2)
    def test_share_url(self):
        url = self.client.share_url("test-bucket", "test.png")
        self.assertTrue(url.startswith("http://172.17"))

    @pytest.mark.run(order=3)
    def test_delete_file(self):
        # 刪除'test.png'
        self.client.delete_file("test-bucket", "test.png")
        # 檢查'test-bucket'有無圖檔
        self.assertFalse(self.client.file_in_bucket("test-bucket", "test.png"))
        # 刪除'test-bucket'
        self.client.remove_bucket("test-bucket")
        # 檢查有無'test-bucket'
        self.assertFalse(self.client.bucket_exist("test-bucket"))
