"""
更新"申请日期"字段的默认值为 TODAY
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.customers.models import CustomField

print("=" * 60)
print("更新申请日期字段的默认值")
print("=" * 60)

# 查找"申请日期"字段
try:
    field = CustomField.objects.get(name="申请日期", field_type="date")
    
    print(f"\n找到字段:")
    print(f"  ID: {field.id}")
    print(f"  名称: {field.name}")
    print(f"  类型: {field.field_type}")
    print(f"  当前默认值: {field.default_value or '(无)'}")
    
    # 更新默认值为 TODAY
    field.default_value = "TODAY"
    field.save()
    
    print(f"\n✓ 更新成功!")
    print(f"  新默认值: {field.default_value}")
    print(f"\n说明:")
    print(f"  - 前端会识别 'TODAY' 标记")
    print(f"  - 自动填充为当前系统日期")
    print(f"  - 用户可以修改这个日期")
    
except CustomField.DoesNotExist:
    print("\n✗ 未找到'申请日期'字段")
    print("  请检查字段是否存在")
except Exception as e:
    print(f"\n✗ 更新失败: {e}")

print("\n" + "=" * 60)

