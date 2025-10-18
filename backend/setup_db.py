#!/usr/bin/env python
"""
数据库初始化脚本
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command
from apps.users.models import User

def main():
    print("=" * 60)
    print("开始初始化数据库...")
    print("=" * 60)
    
    # 1. 运行迁移
    print("\n1. 运行数据库迁移...")
    try:
        call_command('migrate', verbosity=1)
        print("✓ 数据库迁移完成")
    except Exception as e:
        print(f"✗ 迁移失败: {e}")
        return False
    
    # 2. 初始化资料类型
    print("\n2. 初始化资料类型...")
    try:
        call_command('init_document_types', verbosity=1)
        print("✓ 资料类型初始化完成")
    except Exception as e:
        print(f"✗ 资料类型初始化失败: {e}")
    
    # 3. 创建演示数据
    print("\n3. 创建演示数据...")
    try:
        call_command('create_demo_data', verbosity=1)
        print("✓ 演示数据创建完成")
    except Exception as e:
        print(f"✗ 演示数据创建失败: {e}")
    
    # 4. 显示用户信息
    print("\n" + "=" * 60)
    print("数据库初始化完成！")
    print("=" * 60)
    print(f"\n用户总数: {User.objects.count()}")
    print("\n可用的测试账号:")
    for user in User.objects.all():
        print(f"  - {user.username} (角色: {user.get_role_display()})")
    
    print("\n提示: 使用 admin / admin123 登录管理后台")
    print("地址: http://127.0.0.1:8000/admin")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

