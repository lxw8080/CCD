"""
测试 API 访问外部数据库
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.customers.models import CustomField
from apps.customers.serializers import CustomFieldSerializer

print("=" * 60)
print("测试 API 序列化器访问外部数据库")
print("=" * 60)

# 获取所有活跃的自定义字段
fields = CustomField.objects.filter(is_active=True).order_by('sort_order')
print(f"\n✓ 从外部数据库获取到 {fields.count()} 个活跃的自定义字段\n")

# 序列化数据（模拟 API 返回）
serializer = CustomFieldSerializer(fields, many=True)
data = serializer.data

print("API 返回的数据格式:")
print("-" * 60)

import json
print(json.dumps(data, ensure_ascii=False, indent=2))

print("\n" + "=" * 60)
print("字段详情列表")
print("=" * 60)

for i, field_data in enumerate(data, 1):
    print(f"\n{i}. {field_data['name']} ({field_data['field_type']})")
    print(f"   ID: {field_data['id']}")
    print(f"   必填: {'是' if field_data['is_required'] else '否'}")
    print(f"   排序: {field_data['sort_order']}")
    if field_data.get('placeholder'):
        print(f"   占位符: {field_data['placeholder']}")
    if field_data.get('help_text'):
        print(f"   帮助文本: {field_data['help_text']}")
    if field_data.get('options'):
        print(f"   选项: {', '.join(field_data['options'])}")
    if field_data.get('min_value') is not None:
        print(f"   最小值: {field_data['min_value']}")
    if field_data.get('max_value') is not None:
        print(f"   最大值: {field_data['max_value']}")

print("\n" + "=" * 60)
print("✓ API 访问测试成功！")
print("=" * 60)
print("\n前端可以通过以下 API 获取这些字段:")
print("  GET /api/customers/custom-fields/")
print("\n这些字段将自动显示在客户表单中。")

