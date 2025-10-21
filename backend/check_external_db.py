"""
检查外部数据库中的自定义字段表
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from apps.customers.models import CustomField, CustomFieldValue

print("=" * 60)
print("外部数据库状态检查")
print("=" * 60)

# 检查数据库连接
with connection.cursor() as cursor:
    cursor.execute("SELECT current_database(), current_user, inet_server_addr(), inet_server_port()")
    db_info = cursor.fetchone()
    print(f"\n✓ 数据库连接成功:")
    print(f"  数据库名: {db_info[0]}")
    print(f"  用户名: {db_info[1]}")
    print(f"  主机: {db_info[2]}")
    print(f"  端口: {db_info[3]}")

# 检查表是否存在
print("\n" + "=" * 60)
print("检查自定义字段相关表")
print("=" * 60)

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name IN ('custom_fields', 'custom_field_values')
        ORDER BY table_name
    """)
    tables = cursor.fetchall()
    
    if tables:
        print(f"\n✓ 找到 {len(tables)} 个表:")
        for table in tables:
            print(f"  ✓ {table[0]}")
    else:
        print("\n✗ 未找到自定义字段表")
        print("  需要执行迁移: python manage.py migrate customers 0003")

# 检查表结构
if tables and len(tables) == 2:
    print("\n" + "=" * 60)
    print("检查 custom_fields 表结构")
    print("=" * 60)
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = 'custom_fields'
            ORDER BY ordinal_position
        """)
        columns = cursor.fetchall()
        
        print(f"\n表字段 ({len(columns)} 个):")
        for col in columns:
            nullable = "NULL" if col[2] == 'YES' else "NOT NULL"
            default = f", DEFAULT: {col[3]}" if col[3] else ""
            print(f"  • {col[0]:<20} {col[1]:<20} {nullable}{default}")
    
    print("\n" + "=" * 60)
    print("检查 custom_field_values 表结构")
    print("=" * 60)
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = 'custom_field_values'
            ORDER BY ordinal_position
        """)
        columns = cursor.fetchall()
        
        print(f"\n表字段 ({len(columns)} 个):")
        for col in columns:
            nullable = "NULL" if col[2] == 'YES' else "NOT NULL"
            default = f", DEFAULT: {col[3]}" if col[3] else ""
            print(f"  • {col[0]:<20} {col[1]:<20} {nullable}{default}")
    
    # 检查外键约束
    print("\n" + "=" * 60)
    print("检查外键约束")
    print("=" * 60)
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                tc.table_name,
                kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY'
            AND tc.table_name = 'custom_field_values'
        """)
        fks = cursor.fetchall()
        
        if fks:
            print(f"\n✓ 找到 {len(fks)} 个外键约束:")
            for fk in fks:
                print(f"  • {fk[0]}.{fk[1]} → {fk[2]}.{fk[3]}")
        else:
            print("\n✗ 未找到外键约束")
    
    # 检查唯一约束
    print("\n" + "=" * 60)
    print("检查唯一约束")
    print("=" * 60)
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                tc.constraint_name,
                string_agg(kcu.column_name, ', ' ORDER BY kcu.ordinal_position) as columns
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
            WHERE tc.constraint_type = 'UNIQUE'
            AND tc.table_name = 'custom_field_values'
            GROUP BY tc.constraint_name
        """)
        uniques = cursor.fetchall()
        
        if uniques:
            print(f"\n✓ 找到 {len(uniques)} 个唯一约束:")
            for unique in uniques:
                print(f"  • {unique[0]}: ({unique[1]})")
        else:
            print("\n✗ 未找到唯一约束")

# 测试模型访问
print("\n" + "=" * 60)
print("测试 Django ORM 访问")
print("=" * 60)

try:
    count_fields = CustomField.objects.count()
    count_values = CustomFieldValue.objects.count()
    
    print(f"\n✓ ORM 访问成功:")
    print(f"  CustomField 记录数: {count_fields}")
    print(f"  CustomFieldValue 记录数: {count_values}")
    
    if count_fields > 0:
        print(f"\n已有的自定义字段:")
        for field in CustomField.objects.all()[:10]:
            print(f"  • {field.name} ({field.get_field_type_display()}) - {'必填' if field.is_required else '可选'}")
    
except Exception as e:
    print(f"\n✗ ORM 访问失败: {e}")

print("\n" + "=" * 60)
print("检查完成")
print("=" * 60)

