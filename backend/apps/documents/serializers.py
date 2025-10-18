from rest_framework import serializers
from .models import Document, DocumentType
from apps.users.serializers import UserSerializer


class DocumentTypeSerializer(serializers.ModelSerializer):
    """资料类型序列化器"""
    
    class Meta:
        model = DocumentType
        fields = ['id', 'name', 'is_required', 'sort_order', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class DocumentSerializer(serializers.ModelSerializer):
    """资料文档序列化器"""
    uploaded_by_info = UserSerializer(source='uploaded_by', read_only=True)
    document_type_name = serializers.CharField(source='document_type.name', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            'id', 'customer', 'customer_name', 'document_type', 'document_type_name',
            'file', 'file_url', 'file_name', 'file_size', 'status', 'notes',
            'uploaded_by', 'uploaded_by_info', 'uploaded_at', 'updated_at'
        ]
        read_only_fields = ['id', 'uploaded_by', 'uploaded_at', 'updated_at', 'file_size']
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None
    
    def create(self, validated_data):
        # 自动设置上传人
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['uploaded_by'] = request.user
        return super().create(validated_data)


class DocumentUploadSerializer(serializers.Serializer):
    """文档上传序列化器"""
    customer = serializers.IntegerField(required=True)
    document_type = serializers.IntegerField(required=True)
    file = serializers.ImageField(required=True)
    
    def validate_file(self, value):
        # 限制文件大小为10MB
        max_size = 10 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError('文件大小不能超过10MB')
        return value

