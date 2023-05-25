from unittest import mock
from fastapi.testclient import TestClient
from main import app


# 用 TestClient 包裝你的 FastAPI 應用
client = TestClient(app)


# 測試 GET / 路由
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Model": "EZPrompt"}


# 測試 GET /show 路由
@mock.patch("main.os.path.join")
@mock.patch("main.FileResponse")
def test_show_image(mock_file_response, mock_os_path_join):
    # 模擬 os.path.join 和 FileResponse 的行為
    mock_os_path_join.return_value = "/path/to/image"
    mock_file_response.return_value = "file_response"

    response = client.get("/show", params={"user_id": "user", "filename": "image.jpg"})

    # 驗證 os.path.join 被正確呼叫
    mock_os_path_join.assert_called_with("images", "user", "image.jpg")

    # 驗證 FileResponse 被正確呼叫
    mock_file_response.assert_called_with("/path/to/image", media_type="image/jpeg")

    # 驗證 HTTP 響應的狀態碼和內容
    assert response.status_code == 200
    assert response.content.decode() == '"file_response"'
