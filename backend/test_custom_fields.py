"""
测试脚本：创建示例自定义字段
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.customers.models import CustomField

# 清除现有的自定义字段（仅用于测试）
CustomField.objects.all().delete()

# 创建示例自定义字段
fields = [
    {
        'name': '产品',
        'field_type': 'select',
        'is_required': True,
        'sort_order': 1,
        'placeholder': '请选择产品类型',
        'help_text': '请选择客户申请的产品类型',
        'options': ['个人贷款', '企业贷款', '信用卡', '房屋贷款', '汽车贷款']
    },
    {
        'name': '贷款金额',
        'field_type': 'number',
        'is_required': True,
        'sort_order': 2,
        'placeholder': '请输入贷款金额',
        'help_text': '单位：万元',
        'min_value': 1,
        'max_value': 1000
    },
    {
        'name': '申请日期',
        'field_type': 'date',
        'is_required': True,
        'sort_order': 3,
        'placeholder': '请选择申请日期',
        'help_text': '客户提交申请的日期'
    },
    {
        'name': '工作单位',
        'field_type': 'text',
        'is_required': False,
        'sort_order': 4,
        'placeholder': '请输入工作单位',
        'help_text': '客户当前工作单位名称',
        'min_length': 2,
        'max_length': 100
    },
    {
        'name': '月收入',
        'field_type': 'number',
        'is_required': False,
        'sort_order': 5,
        'placeholder': '请输入月收入',
        'help_text': '单位：元',
        'min_value': 0,
        'max_value': 1000000
    },
    {
        'name': '联系邮箱',
        'field_type': 'email',
        'is_required': False,
        'sort_order': 6,
        'placeholder': '请输入邮箱地址',
        'help_text': '用于接收通知和文件'
    },
    {
        'name': '备用联系人',
        'field_type': 'text',
        'is_required': False,
        'sort_order': 7,
        'placeholder': '请输入备用联系人姓名',
        'help_text': '紧急联系人姓名'
    },
    {
        'name': '备用联系电话',
        'field_type': 'phone',
        'is_required': False,
        'sort_order': 8,
        'placeholder': '请输入备用联系电话',
        'help_text': '紧急联系人电话'
    },
    {
        'name': '特殊说明',
        'field_type': 'textarea',
        'is_required': False,
        'sort_order': 9,
        'placeholder': '请输入特殊说明',
        'help_text': '其他需要说明的信息'
    }
]

created_count = 0
for field_data in fields:
    field = CustomField.objects.create(**field_data)
    created_count += 1
    print(f"✓ 创建自定义字段: {field.name} ({field.get_field_type_display()})")

print(f"\n成功创建 {created_count} 个自定义字段！")
print("\n现在可以在客户表单中看到这些字段了。")

