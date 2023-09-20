# frontend

## 安裝環境
### 先安裝 nvm, node, npm
node 版本為 v14.21.3 
```
sudo apt-get update
sudo apt-get install build-essential libssl-dev
curl https://raw.githubusercontent.com/creationix/nvm/v0.39.5/install.sh | bash
source ~/.profile
nvm install v14.21.3 
```
### 再安裝用到的node_modules
```
npm install
npm ci
```
## 本地啟動
```
npm run serve
```

## unit測試
```
npm run test:unit
```