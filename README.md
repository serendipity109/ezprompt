## 部屬流程
1. 安裝[前端環境](frontend/README.md)
2. 更改 docker-compose 後端環境變數IP={電腦的IP}
3. 更改前端環境變數的IP(/frontend/.env.internal)改成對應的前後端IP
3. 啟動 docker
```
make build
make run
```
4. 等待10秒前端部屬完成即可瀏覽 http://localhost:8080/home
5. 關閉服務
```
make down
```
## 本地測試
### gitlab runner
```
gitlab-runner exec docker {job}
```
### pytest
```
先進到安裝過requirements的環境
cd backend
pytest tests/test_unit.py
```
## 使用說明
### 初次使用
1. 點選右上角Login創帳號，google登入限定以local連線才可使用，Sign up則需要有效的email認證。
2. 用MySQL的GUI工具連上127.0.0.1:3306 root/password資料庫，在user, user_info table中都可以看到新增的帳戶資訊。
3. 加值帳號，點擊Account分頁，3個方案的Get started都可獲得不同的credits數。
4. 即可去首頁生成圖片。
### 管理API
可以上 http://localhost:9527/docs#/ 管理後端API
## k8s應用部屬
1. [安裝kubectl](https://kubernetes.io/zh-cn/docs/tasks/tools/install-kubectl-linux/)
2. [安裝minikube](https://minikube.sigs.k8s.io/docs/start/)
3. 啟動minikube
```
minikube start
```
4. 部屬k8s腳本
```
kubectl apply -f k8s.yaml
```
