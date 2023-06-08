import unittest
import os
from fastapi.testclient import TestClient
from main import app


# 用 TestClient 包裝你的 FastAPI 應用
client = TestClient(app)


# 測試 GET / 路由
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Model": "EZPrompt"}


class TestShowImage(unittest.TestCase):
    def setUp(self):
        # 建立一個測試用的檔案
        self.test_folder = "/workspace/test_folder"
        self.test_image_name = "test_image.jpg"
        self.test_image_path = os.path.join(self.test_folder, self.test_image_name)
        os.makedirs(self.test_folder, exist_ok=True)
        with open(self.test_image_path, "w") as f:
            f.write("test")

    def tearDown(self):
        # 測試結束後，刪除測試用的檔案和目錄
        os.remove(self.test_image_path)
        os.rmdir(self.test_folder)

    def test_show_image_exists(self):
        response = client.get(f"/media/test_folder/{self.test_image_name}")
        self.assertEqual(response.status_code, 200)
        # 你可能需要根據實際情況，驗證返回的內容

    def test_show_image_not_exists(self):
        response = client.get("/media/test_folder/non_existent_image.jpg")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"error": "Image not found"})
