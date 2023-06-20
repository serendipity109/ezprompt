## 部屬 docker swarm
1. 初始化 manager
#### manager 主機上
```bash
docker swarm init --advertise-addr {ip}
```
2. 初始化 worker
#### worker 主機上
```bash
docker swarm join --token ....
```
3. 部屬工作
#### manager 主機上
```bash
docker stack deploy -c /path/to/your/docker-compose.yml myapp
```
4. 關閉工作
#### worker 主機上
```bash
docker swarm leave
```
#### manager 主機上
```bash
docker swarm leave --force
```