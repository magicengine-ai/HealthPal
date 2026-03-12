# 🚀 HealthPal 快速启动（网络受限环境）

由于 Docker Hub 网络连接问题，提供以下替代方案：

## 方案一：使用国内镜像源（推荐）

编辑 `config/docker-compose.yml`，在顶部添加镜像加速器：

```yaml
services:
  mysql:
    image: registry.cn-hangzhou.aliyuncs.com/library/mysql:8.0
    # ... 其他配置不变
```

## 方案二：先启动后端 API 服务（无数据库）

```bash
cd HealthPal/src/backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动服务（仅 API，需要手动配置数据库）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 方案三：手动下载镜像

```bash
# 使用国内镜像源
docker pull registry.cn-hangzhou.aliyuncs.com/library/mysql:8.0
docker pull registry.cn-hangzhou.aliyuncs.com/library/mongo:6
docker pull registry.cn-hangzhou.aliyuncs.com/library/redis:7

# 然后启动
cd HealthPal/config
docker-compose up -d
```

## 方案四：使用外部数据库服务

- 使用云服务（阿里云 RDS、MongoDB Atlas 等）
- 或本地安装数据库

---

**建议：** 使用方案三，先手动拉取国内镜像源的镜像。
