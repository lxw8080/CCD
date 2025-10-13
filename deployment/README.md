# 部署文档

本目录包含部署客户资料收集系统所需的配置文件和脚本。

## 文件说明

- `nginx.conf` - Nginx配置文件
- `gunicorn_config.py` - Gunicorn配置文件
- `deploy.sh` - 自动化部署脚本
- `systemd/ccd-backend.service` - Systemd服务配置

## 部署步骤

### 1. 准备服务器环境

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装必要软件
sudo apt install -y python3 python3-pip python3-venv
sudo apt install -y postgresql postgresql-contrib
sudo apt install -y nginx
sudo apt install -y nodejs npm
```

### 2. 创建数据库

```bash
# 切换到postgres用户
sudo -u postgres psql

# 在PostgreSQL中执行
CREATE DATABASE ccd_db;
CREATE USER ccd_user WITH PASSWORD 'your_password';
ALTER ROLE ccd_user SET client_encoding TO 'utf8';
ALTER ROLE ccd_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ccd_user SET timezone TO 'Asia/Shanghai';
GRANT ALL PRIVILEGES ON DATABASE ccd_db TO ccd_user;
\q
```

### 3. 克隆项目

```bash
cd /var/www
git clone <repository-url> CCD
cd CCD
```

### 4. 配置后端

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
nano .env  # 编辑配置

# 运行迁移
python manage.py migrate

# 初始化数据
python manage.py init_document_types

# 创建超级管理员
python manage.py createsuperuser

# 收集静态文件
python manage.py collectstatic --noinput

# 创建media目录
mkdir -p media/documents
chmod -R 755 media
```

### 5. 配置前端

```bash
cd ../frontend

# 安装依赖
npm install

# 构建生产版本
npm run build
```

### 6. 配置Nginx

```bash
# 复制配置文件
sudo cp deployment/nginx.conf /etc/nginx/sites-available/ccd

# 修改配置文件中的路径
sudo nano /etc/nginx/sites-available/ccd

# 创建符号链接
sudo ln -s /etc/nginx/sites-available/ccd /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启Nginx
sudo systemctl restart nginx
```

### 7. 配置Systemd服务

```bash
# 复制服务文件
sudo cp deployment/systemd/ccd-backend.service /etc/systemd/system/

# 修改服务文件中的路径和用户
sudo nano /etc/systemd/system/ccd-backend.service

# 重新加载systemd
sudo systemctl daemon-reload

# 启用服务
sudo systemctl enable ccd-backend

# 启动服务
sudo systemctl start ccd-backend

# 查看状态
sudo systemctl status ccd-backend
```

### 8. 配置防火墙

```bash
# 如果使用ufw
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

## 使用自动部署脚本

修改 `deploy.sh` 中的路径配置，然后执行：

```bash
chmod +x deployment/deploy.sh
./deployment/deploy.sh
```

## SSL/HTTPS配置

### 使用Let's Encrypt

```bash
# 安装certbot
sudo apt install -y certbot python3-certbot-nginx

# 获取SSL证书
sudo certbot --nginx -d your-domain.com

# 自动续期测试
sudo certbot renew --dry-run
```

## 常用命令

### 查看日志

```bash
# Gunicorn日志
sudo journalctl -u ccd-backend -f

# Nginx访问日志
sudo tail -f /var/log/nginx/access.log

# Nginx错误日志
sudo tail -f /var/log/nginx/error.log
```

### 重启服务

```bash
# 重启后端
sudo systemctl restart ccd-backend

# 重启Nginx
sudo systemctl restart nginx

# 重新加载Nginx配置
sudo systemctl reload nginx
```

### 更新代码

```bash
cd /var/www/CCD
git pull origin main
./deployment/deploy.sh
```

## 性能优化

### PostgreSQL优化

编辑 `/etc/postgresql/*/main/postgresql.conf`：

```ini
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 4MB
min_wal_size = 1GB
max_wal_size = 4GB
```

### Gunicorn优化

根据服务器配置调整 `gunicorn_config.py` 中的workers数量：

```python
workers = (CPU核心数 * 2) + 1
```

## 监控和维护

### 设置定时任务

```bash
crontab -e

# 每天凌晨3点备份数据库
0 3 * * * pg_dump -U ccd_user ccd_db > /backup/ccd_db_$(date +\%Y\%m\%d).sql

# 每周清理过期日志
0 0 * * 0 find /var/log/nginx -name "*.log" -mtime +30 -delete
```

### 监控磁盘空间

```bash
# 查看磁盘使用情况
df -h

# 查看media目录大小
du -sh /var/www/CCD/backend/media
```

## 故障排除

### 502 Bad Gateway

1. 检查Gunicorn是否运行：`sudo systemctl status ccd-backend`
2. 检查端口是否监听：`sudo netstat -tlnp | grep 8000`
3. 查看错误日志：`sudo journalctl -u ccd-backend -n 50`

### 静态文件404

1. 确认静态文件已收集：`python manage.py collectstatic`
2. 检查Nginx配置中的路径是否正确
3. 检查文件权限：`ls -la /var/www/CCD/backend/staticfiles`

### 数据库连接失败

1. 确认PostgreSQL正在运行：`sudo systemctl status postgresql`
2. 检查数据库配置：`.env`文件中的数据库设置
3. 测试数据库连接：`psql -U ccd_user -d ccd_db -h localhost`

## 安全建议

1. 定期更新系统和依赖包
2. 使用强密码和密钥认证
3. 配置防火墙，只开放必要端口
4. 启用HTTPS
5. 定期备份数据库和上传文件
6. 设置日志轮转
7. 监控异常访问和错误日志

