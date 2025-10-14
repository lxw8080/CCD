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
    
    # 创建文档记录
    document = Document.objects.create(
        customer=customer,
        document_type=doc_type,
        file=serializer.validated_data['file'],
        remarks=serializer.validated_data.get('remarks', ''),
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
    for file in files:
        # 限制文件大小
        if file.size > 10 * 1024 * 1024:
            continue
        
        document = Document.objects.create(
            customer=customer,
            document_type=doc_type,
            file=file,
            uploaded_by=request.user
        )
        documents.append(document)
    
    # 返回创建的文档列表
    serializer = DocumentSerializer(
        documents, many=True, context={'request': request}
    )
    return Response(serializer.data, status=status.HTTP_201_CREATED)

