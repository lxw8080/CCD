from django.contrib import admin
from .models import DocumentType, Document


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_required', 'sort_order', 'created_at']
    list_filter = ['is_required']
    search_fields = ['name']
    ordering = ['sort_order', 'id']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = [
        'customer', 'document_type', 'file_name', 
        'status', 'uploaded_by', 'uploaded_at'
    ]
    list_filter = ['status', 'document_type', 'uploaded_at']
    search_fields = ['customer__name', 'customer__id_card', 'file_name']
    readonly_fields = ['file_size', 'uploaded_at']
    fieldsets = (
        ('关联信息', {
            'fields': ('customer', 'document_type')
        }),
        ('文件信息', {
            'fields': ('file', 'file_name', 'file_size')
        }),
        ('状态信息', {
            'fields': ('status',)
        }),
        ('系统信息', {
            'fields': ('uploaded_by', 'uploaded_at')
        }),
    )

