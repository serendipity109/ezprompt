def test_e2e():
    print("hihihihi")
    assert 1 == 1


# from fastapi.testclient import TestClient
# from unittest.mock import patch
# from main import app  # replace this with your actual app import

# client = TestClient(app)

# @patch('main.client.StabilityInference')  # replace 'main' with your actual module name
# @patch('main.minioTool.MinioClient')
# def test_sdxl(mock_stability, mock_minio):
#     # Set up our mock objects
#     mock_stability.return_value.generate.return_value = ...  # fill this in
#     mock_minio.return_value.upload_file.return_value = ...  # fill this in
#     mock_minio.return_value.share_url.return_value = ...  # fill this in

#     # Set up our test data
#     test_data = {
#         "prompt": "...",  # fill this in
#         "nprompt": "...",  # fill this in
#         "hw": 1,
#         "n": 1,
#         "CFG": 7.0,
#     }

#     # Call the API
#     response = client.post("/sdxl", json=test_data)

#     # Verify the response
#     assert response.status_code == 200
#     assert 'code' in response.json()
#     assert response.json()['code'] == "200" # 你期望的代碼

#     # 檢查模擬對象的調用
#     mock_stability.return_value.generate.assert_called_once_with(...)  # 用你期望的參數填充
#     mock_minio.return_value.upload_file.assert_called_once_with(...)  # 用你期望的參數填充
#     mock_minio.return_value.share_url.assert_called_once_with(...)  # 用你期望的參數填充

# @patch('main.client.StabilityInference')  # 替換'main'為你的實際模組名稱
# @patch('main.minioTool.MinioClient')
# def test_ezpmt(mock_stability, mock_minio):
#     # 設置我們的模擬對象
#     mock_stability.return_value.generate.return_value = ...  # 填寫此處
#     mock_minio.return_value.upload_file.return_value = ...  # 填寫此處
#     mock_minio.return_value.share_url.return_value = ...  # 填寫此處

#     # 設置我們的測試數據
#     test_data = {
#         "prompt": "...",  # 填寫此處
#         "nprompt": "...",  # 填寫此處
#         "hw": 1,
#         "n": 1,
#         "CFG": 7.0,
#     }

#     # 調用API
#     response = client.post("/ezpmt", json=test_data)

#     # 驗證回應
#     assert response.status_code == 200
#     assert 'code' in response.json()
#     assert response.json()['code'] == "200"  # 你期望的代碼

#     # 檢查模擬對象的調用
#     mock_stability.return_value.generate.assert_called_once_with(...)  # 用你期望的參數填充
#     mock_minio.return_value.upload_file.assert_called_once_with(...)  # 用你期望的參數填充
#     mock_minio.return_value.share_url.assert_called_once_with(...)  # 用你期望的參數填充
