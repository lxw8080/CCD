from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count, Case, When
from .models import Customer
from .serializers import CustomerSerializer, CustomerListSerializer
from apps.documents.models import DocumentType, Document


class CustomerViewSet(viewsets.ModelViewSet):
    """客户视图集"""
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CustomerListSerializer
        return CustomerSerializer
    
    def get_queryset(self):
        queryset = Customer.objects.all()
        
        # 搜索功能
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(id_card__icontains=search) |
                Q(phone__icontains=search)
            )
        
        # 状态筛选
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def completeness(self, request, pk=None):
        """检查客户资料完整性"""
        customer = self.get_object()
        
        # 获取所有必需的资料类型
        required_types = DocumentType.objects.filter(is_required=True)
        
        # 获取客户已上传的资料类型
        uploaded_types = Document.objects.filter(
            customer=customer
        ).values_list('document_type_id', flat=True)
        
        # 计算完整性
        completeness_data = []
        missing_count = 0
        
        for doc_type in required_types:
            is_uploaded = doc_type.id in uploaded_types
            if not is_uploaded:
                missing_count += 1
            
            completeness_data.append({
                'type_id': doc_type.id,
                'type_name': doc_type.name,
                'is_required': doc_type.is_required,
                'is_uploaded': is_uploaded
            })
        
        total_required = required_types.count()
        uploaded_required = total_required - missing_count
        completion_rate = (uploaded_required / total_required * 100) if total_required > 0 else 100
        
        return Response({
            'customer_id': customer.id,
            'customer_name': customer.name,
            'total_required': total_required,
            'uploaded_required': uploaded_required,
            'missing_count': missing_count,
            'completion_rate': round(completion_rate, 2),
            'documents': completeness_data
        })

