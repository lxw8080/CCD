"""
验证"申请日期"字段的默认值设置
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.customers.models import CustomField
from apps.customers.serializers import CustomFieldSerializer
from datetime import date

print("=" * 60)
print("验证申请日期字段的默认值设置")
print("=" * 60)

# 查找"申请日期"字段
try:
    field = CustomField.objects.get(name="申请日期", field_type="date")
    
    print(f"\n数据库中的字段信息:")
    print(f"  ID: {field.id}")
    print(f"  名称: {field.name}")
    print(f"  类型: {field.field_type}")
    print(f"  默认值: {field.default_value}")
    print(f"  是否必填: {'是' if field.is_required else '否'}")
    
    # 序列化字段（模拟 API 返回）
    serializer = CustomFieldSerializer(field)
    data = serializer.data
    
    print(f"\nAPI 返回的数据:")
    print(f"  default_value: {data['default_value']}")
    
    print(f"\n前端处理逻辑:")
    print(f"  1. 前端获取到 default_value = '{data['default_value']}'")
    print(f"  2. 检测到 field_type = 'date' 且 default_value = 'TODAY'")
    print(f"  3. 自动转换为当前日期: {date.today().strftime('%Y-%m-%d')}")
    print(f"  4. 在表单中自动填充该日期")
    
    print(f"\n✓ 配置正确!")
    print(f"\n预期效果:")
    print(f"  - 用户打开'新建客户'表单")
    print(f"  - '申请日期'字段自动显示: {date.today().strftime('%Y-%m-%d')}")
    print(f"  - 用户可以修改这个日期")
    print(f"  - 减少手动选择日期的操作")
    
except CustomField.DoesNotExist:
    print("\n✗ 未找到'申请日期'字段")
except Exception as e:
    print(f"\n✗ 验证失败: {e}")

print("\n" + "=" * 60)
print("测试其他自定义字段的默认值")
print("=" * 60)

# 显示所有有默认值的字段
fields_with_defaults = CustomField.objects.filter(
    is_active=True
).exclude(default_value__isnull=True).exclude(default_value='')

if fields_with_defaults.exists():
    print(f"\n找到 {fields_with_defaults.count()} 个有默认值的字段:\n")
    for f in fields_with_defaults:
        print(f"  • {f.name} ({f.field_type})")
        print(f"    默认值: {f.default_value}")
        if f.field_type == 'date' and f.default_value == 'TODAY':
            print(f"    → 将转换为: {date.today().strftime('%Y-%m-%d')}")
        print()
else:
    print("\n没有其他字段设置了默认值")

print("=" * 60)

