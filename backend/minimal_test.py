#!/usr/bin/env python
"""最小化Django测试 - 不依赖DRF"""
import os
import sys

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

# 设置环境变量
os.environ['USE_SQLITE'] = 'True'
os.environ['SECRET_KEY'] = 'test-secret-key-12345'
os.environ['DEBUG'] = 'True'

# Django最小化配置
from django.conf import settings

if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY='test-key',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'test_db.sqlite3',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
        ],
        USE_TZ=True,
    )

import django
django.setup()

print("[OK] Django version:", django.get_version())
print("[OK] Database:", settings.DATABASES['default']['ENGINE'])
print("\n[SUCCESS] Minimal Django test passed!")
print("\nDjango is working correctly.")
print("However, we need to install djangorestframework and other dependencies.")
print("\nTo proceed, you need to resolve the proxy issue.")
print("Please refer to PROXY_ISSUE_SOLUTION.md for solutions.")

