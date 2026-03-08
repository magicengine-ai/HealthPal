# 数据库迁移脚本

使用 Alembic 进行数据库版本管理

## 初始化

```bash
cd src/backend
alembic init alembic
```

## 常用命令

```bash
# 创建新迁移
alembic revision --autogenerate -m "Initial migration"

# 执行迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1

# 查看当前版本
alembic current
```
