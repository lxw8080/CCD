# Gunicorn配置文件
# 使用方法: gunicorn -c deployment/gunicorn_config.py config.wsgi:application

import multiprocessing

# 绑定地址和端口
bind = "127.0.0.1:8000"

# 工作进程数（建议为CPU核心数的2-4倍）
workers = multiprocessing.cpu_count() * 2 + 1

# 工作模式
worker_class = "sync"

# 每个worker的线程数
threads = 2

# 最大并发请求数
worker_connections = 1000

# 超时时间（秒）
timeout = 30

# 保持连接时间（秒）
keepalive = 2

# 最大请求数，超过后重启worker（防止内存泄漏）
max_requests = 1000
max_requests_jitter = 50

# 优雅重启超时时间
graceful_timeout = 30

# 日志
accesslog = "-"  # 标准输出
errorlog = "-"   # 标准错误输出
loglevel = "info"

# 进程名称
proc_name = "ccd_backend"

# Daemon模式（后台运行）
# daemon = False

# PID文件
# pidfile = "/var/run/gunicorn.pid"

# 用户和组（生产环境建议使用非root用户）
# user = "www-data"
# group = "www-data"

# 临时文件目录
# tmp_upload_dir = None

# 预加载应用（可以减少内存占用）
preload_app = True

# 重新加载代码时自动重启
reload = False  # 生产环境应设为False

# 静态文件处理
# sendfile = True

