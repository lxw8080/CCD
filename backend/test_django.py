#!/usr/bin/env python
"""测试Django是否正常工作"""
import os
import sys

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ['USE_SQLITE'] = 'True'
os.environ['SECRET_KEY'] = 'test-secret-key-12345'
os.environ['DEBUG'] = 'True'

try:
    import django
    print(f"[OK] Django version: {django.get_version()}")
    
    # 设置Django
    django.setup()
    print("[OK] Django setup successful")
    
    # 测试数据库配置
    from django.conf import settings
    print(f"[OK] Database engine: {settings.DATABASES['default']['ENGINE']}")
    print(f"[OK] Using SQLite: {settings.USE_SQLITE}")
    
    print("\n[SUCCESS] Django environment test passed!")
    print("\nYou can now run:")
    print("  python manage.py makemigrations")
    print("  python manage.py migrate")
    
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()

