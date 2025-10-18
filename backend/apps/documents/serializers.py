from rest_framework import serializers
from .models import Document, DocumentType
from .validators import validate_document_file, get_file_type_display
from apps.users.serializers import UserSerializer


class DocumentTypeSerializer(serializers.ModelSerializer):
    """资料类型序列化器"""

    class Meta:
        model = DocumentType
        fields = [
            'id', 'name', 'is_required', 'sort_order', 'description',
            'allowed_file_types', 'max_file_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DocumentSerializer(serializers.ModelSerializer):
    """资料文档序列化器"""
    uploaded_by_info = UserSerializer(source='uploaded_by', read_only=True)
    document_type_name = serializers.CharField(source='document_type.name', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    file_url = serializers.SerializerMethodField()
    file_type_display = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            'id', 'customer', 'customer_name', 'document_type', 'document_type_name',
            'file', 'file_url', 'file_name', 'file_size', 'file_type', 'file_type_display',
            'status', 'notes', 'uploaded_by', 'uploaded_by_info', 'uploaded_at', 'updated_at'
        ]
        read_only_fields = ['id', 'uploaded_by', 'uploaded_at', 'updated_at', 'file_size', 'file_type']

    def get_file_url(self, obj):
        if not obj.file:
            return None

        url = obj.file.url
        request = self.context.get('request')

        if request:
            host = request.get_host()
            if url.startswith(('http://', 'https://')):
                return url
            if host not in {'127.0.0.1', '127.0.0.1:8000', 'localhost', 'localhost:8000'}:
                return request.build_absolute_uri(url)

        return url

    def get_file_type_display(self, obj):
        return get_file_type_display(obj.file_type)

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
    file = serializers.FileField(required=True)

    def validate_file(self, value):
        # 验证文件类型和大小，并缓存识别结果供后续使用
        from .validators import validate_document_file
        file_type = validate_document_file(value)
        setattr(value, 'detected_file_type', file_type)
        return value

