## 部屬流程
### 先設定 docker 內網
```
docker network create --driver bridge --subnet=172.18.0.0/16 --gateway=172.18.0.22 ezpmt
```

## 本地測試
### gitlab runner
```
gitlab-runner exec docker {job}
```
### pytest
```
cd backend
pytest tests/test_integration.py
```