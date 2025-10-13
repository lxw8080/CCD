from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserCreateSerializer(serializers.ModelSerializer):
    """用户创建序列化器"""
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'role', 'phone']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

