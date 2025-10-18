from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import Document, DocumentType
from .serializers import (
    DocumentSerializer, DocumentTypeSerializer, DocumentUploadSerializer
)
from .validators import get_file_type
from apps.customers.models import Customer


class DocumentTypeViewSet(viewsets.ModelViewSet):
    """资料类型视图集"""
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None  # 禁用分页，返回所有资料类型


class DocumentViewSet(viewsets.ModelViewSet):
    """资料文档视图集"""
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_queryset(self):
        queryset = Document.objects.select_related(
            'customer', 'document_type', 'uploaded_by'
        )
        
        # 按客户筛选
        customer_id = self.request.query_params.get('customer_id', None)
        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)
        
        # 按资料类型筛选
        doc_type_id = self.request.query_params.get('document_type', None)
        if doc_type_id:
            queryset = queryset.filter(document_type_id=doc_type_id)
        
        # 按状态筛选
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_document(request):
    """上传资料文档"""
    serializer = DocumentUploadSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 验证客户和资料类型是否存在
    customer = get_object_or_404(Customer, id=serializer.validated_data['customer'])
    doc_type = get_object_or_404(DocumentType, id=serializer.validated_data['document_type'])

    # 自动检测文件类型
    file_obj = serializer.validated_data['file']
    file_type = getattr(file_obj, 'detected_file_type', None)
    if not file_type:
        file_type = get_file_type(
            file_obj.name,
            getattr(file_obj, 'content_type', None)
        )

    if not file_type:
        return Response(
            {'error': '无法识别文件类型，请检查文件是否支持上传'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # ===== 新增：验证文件类型限制 =====
    if doc_type.allowed_file_types and len(doc_type.allowed_file_types) > 0:
        if file_type not in doc_type.allowed_file_types:
            return Response(
                {'error': f'不支持的文件类型: {file_type}。允许的类型: {", ".join(doc_type.allowed_file_types)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    # ===== 新增：验证文件数量限制 =====
    if doc_type.max_file_count > 0:
        existing_count = Document.objects.filter(
            customer=customer,
            document_type=doc_type
        ).count()
        if existing_count >= doc_type.max_file_count:
            return Response(
                {'error': f'该资料类型最多只能上传 {doc_type.max_file_count} 个文件，已上传 {existing_count} 个'},
                status=status.HTTP_400_BAD_REQUEST
            )

    # 创建文档记录
    document = Document.objects.create(
        customer=customer,
        document_type=doc_type,
        file=file_obj,
        file_type=file_type or 'image',
        uploaded_by=request.user
    )

    # 返回创建的文档信息
    result_serializer = DocumentSerializer(document, context={'request': request})
    return Response(result_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def batch_upload(request):
    """批量上传资料文档"""
    files = request.FILES.getlist('files')
    customer_id = request.data.get('customer')
    doc_type_id = request.data.get('document_type')

    if not files:
        return Response(
            {'error': '没有上传文件'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not customer_id or not doc_type_id:
        return Response(
            {'error': '缺少客户ID或资料类型ID'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 验证客户和资料类型是否存在
    customer = get_object_or_404(Customer, id=customer_id)
    doc_type = get_object_or_404(DocumentType, id=doc_type_id)

    # 批量创建文档
    documents = []
    errors = []
    for file in files:
        try:
            # 验证文件
            from .validators import validate_document_file
            file_type = validate_document_file(file)

            # ===== 新增：验证文件类型限制 =====
            if doc_type.allowed_file_types and len(doc_type.allowed_file_types) > 0:
                if file_type not in doc_type.allowed_file_types:
                    errors.append(f'{file.name}: 不支持的文件类型')
                    continue

            # ===== 新增：验证文件数量限制 =====
            if doc_type.max_file_count > 0:
                existing_count = Document.objects.filter(
                    customer=customer,
                    document_type=doc_type
                ).count()
                if existing_count + len(documents) >= doc_type.max_file_count:
                    errors.append(f'{file.name}: 已达到最大文件数限制')
                    continue

            document = Document.objects.create(
                customer=customer,
                document_type=doc_type,
                file=file,
                file_type=file_type,
                uploaded_by=request.user
            )
            documents.append(document)
        except Exception as e:
            # 记录错误
            errors.append(f'{file.name}: {str(e)}')
            continue

    # 返回创建的文档列表和错误信息
    serializer = DocumentSerializer(
        documents, many=True, context={'request': request}
    )
    response_data = {
        'documents': serializer.data,
        'errors': errors if errors else None
    }
    return Response(response_data, status=status.HTTP_201_CREATED)

