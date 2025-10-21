"""
测试脚本：创建测试用户
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User

# 创建测试管理员用户
username = 'admin'
password = 'admin123'
email = 'admin@example.com'

if User.objects.filter(username=username).exists():
    print(f"用户 '{username}' 已存在")
    user = User.objects.get(username=username)
else:
    user = User.objects.create_superuser(
        username=username,
        password=password,
        email=email,
        role='admin'
    )
    print(f"✓ 创建超级管理员: {username}")
    print(f"  密码: {password}")
    print(f"  邮箱: {email}")

print(f"\n可以使用以下凭据登录:")
print(f"  用户名: {username}")
print(f"  密码: {password}")
print(f"\nDjango Admin: http://127.0.0.1:8000/admin/")
print(f"前端登录: http://localhost:5173/login")

