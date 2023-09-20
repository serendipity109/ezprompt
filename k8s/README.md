## k8s應用部屬
1. [安裝kubectl](https://kubernetes.io/zh-cn/docs/tasks/tools/install-kubectl-linux/)
2. [安裝minikube](https://minikube.sigs.k8s.io/docs/start/)
3. 啟動minikube
```
minikube start
```
4. 把image從local轉到minikube可以讀到的環境
```
docker save ezpmt_nginx > ezpmt_nginx.tar
eval $(minikube docker-env -u)
docker load <  ezpmt_nginx.tar
```
5. 部屬k8s腳本
```
kubectl apply -f deployment.yaml
```
6. 啟動k8s服務
```
kubectl apply -f service.yaml
```
7. 瀏覽網站
```
minikube service ezpmt --url
```
8. 關閉服務
```
kubectl delete service ezpmt
```
9. 刪除部屬
```
kubectl delete -f deployment.yaml
```
## 查詢狀態
```
kubectl get deployments
kubectl get services
kubectl get pods
```