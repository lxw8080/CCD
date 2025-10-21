from rest_framework import serializers
from .models import Customer, CustomField, CustomFieldValue
from apps.users.serializers import UserSerializer


class CustomFieldSerializer(serializers.ModelSerializer):
    """自定义字段序列化器"""

    class Meta:
        model = CustomField
        fields = [
            'id', 'name', 'field_type', 'is_required', 'sort_order',
            'placeholder', 'help_text', 'default_value', 'options',
            'min_length', 'max_length', 'min_value', 'max_value',
            'regex_pattern', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CustomFieldValueSerializer(serializers.ModelSerializer):
    """自定义字段值序列化器"""
    field_name = serializers.CharField(
        source='custom_field.name',
        read_only=True
    )
    field_type = serializers.CharField(
        source='custom_field.field_type',
        read_only=True
    )

    class Meta:
        model = CustomFieldValue
        fields = [
            'id', 'custom_field', 'field_name', 'field_type',
            'value', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CustomerSerializer(serializers.ModelSerializer):
    """客户序列化器"""
    created_by_info = UserSerializer(source='created_by', read_only=True)
    custom_field_values = CustomFieldValueSerializer(
        many=True,
        read_only=True
    )
    custom_fields = serializers.DictField(
        write_only=True,
        required=False,
        help_text='自定义字段值，格式: {"field_id": "value"}'
    )

    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'id_card', 'phone', 'address',
            'status', 'created_by', 'created_by_info',
            'custom_field_values', 'custom_fields',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        # 提取自定义字段数据
        custom_fields_data = validated_data.pop('custom_fields', {})

        # 自动设置创建人
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user

        # 创建客户
        customer = super().create(validated_data)

        # 保存自定义字段值
        self._save_custom_fields(customer, custom_fields_data)

        return customer

    def update(self, instance, validated_data):
        # 提取自定义字段数据
        custom_fields_data = validated_data.pop('custom_fields', {})

        # 更新客户基本信息
        customer = super().update(instance, validated_data)

        # 更新自定义字段值
        self._save_custom_fields(customer, custom_fields_data)

        return customer

    def _save_custom_fields(self, customer, custom_fields_data):
        """保存或更新自定义字段值"""
        for field_id, value in custom_fields_data.items():
            try:
                custom_field = CustomField.objects.get(
                    id=field_id,
                    is_active=True
                )
                CustomFieldValue.objects.update_or_create(
                    customer=customer,
                    custom_field=custom_field,
                    defaults={'value': value}
                )
            except CustomField.DoesNotExist:
                # 忽略不存在或未激活的字段
                pass


class CustomerListSerializer(serializers.ModelSerializer):
    """客户列表序列化器（简化版）"""
    created_by_name = serializers.CharField(
        source='created_by.username',
        read_only=True
    )

    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'id_card', 'phone', 'status',
            'created_by_name', 'created_at', 'updated_at'
        ]

