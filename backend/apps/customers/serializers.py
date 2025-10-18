from rest_framework import serializers
from .models import Customer
from apps.users.serializers import UserSerializer


class CustomerSerializer(serializers.ModelSerializer):
    """客户序列化器"""
    created_by_info = UserSerializer(source='created_by', read_only=True)
    
    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'id_card', 'phone', 'address',
            'status', 'created_by', 'created_by_info',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # 自动设置创建人
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)


class CustomerListSerializer(serializers.ModelSerializer):
    """客户列表序列化器（简化版）"""
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'id_card', 'phone', 'status',
            'created_by_name', 'created_at', 'updated_at'
        ]

