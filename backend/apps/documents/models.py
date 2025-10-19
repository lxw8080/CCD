import os
from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.customers.models import Customer


# 文件类型定义
FILE_TYPE_CHOICES = [
    ('image', '图片'),
    ('video', '视频'),
    ('pdf', 'PDF'),
    ('document', '文档'),
    ('spreadsheet', '表格'),
]

# 支持的文件扩展名
ALLOWED_EXTENSIONS = {
    'image': ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'],
    'video': ['mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv', 'm4v', '3gp', '3gpp', 'webm', 'ts', 'mpg', 'mpeg', 'ogg'],
    'pdf': ['pdf'],
    'document': ['doc', 'docx', 'txt', 'rtf'],
    'spreadsheet': ['xls', 'xlsx', 'csv']
}

# 文件大小限制（字节）- 统一取消限制，保留结构便于后续扩展
FILE_SIZE_LIMITS = {
    'image': None,
    'video': None,
    'pdf': None,
    'document': None,
    'spreadsheet': None,
}


def document_upload_path(instance, filename):
    """生成文件上传路径"""
    ext = os.path.splitext(filename)[1]
    # 使用当前时间，因为 uploaded_at 在文件保存时还未设置
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    new_filename = f"{instance.customer.id}_{instance.document_type.id}_{timestamp}{ext}"
    return os.path.join('documents', str(instance.customer.id), new_filename)


class DocumentType(models.Model):
    """资料类型模型"""
    name = models.CharField(max_length=100, unique=True, verbose_name='类型名称')
    is_required = models.BooleanField(default=True, verbose_name='是否必需')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    description = models.TextField(blank=True, null=True, verbose_name='说明')
    allowed_file_types = models.JSONField(
        default=list,
        blank=True,
        verbose_name='允许的文件类型',
        help_text='允许的文件类型列表，如 ["image", "video", "pdf"]，空列表表示允许所有类型'
    )
    max_file_count = models.IntegerField(
        default=0,
        verbose_name='最大文件数',
        help_text='每个资料类型最多允许上传的文件数，0 表示不限制'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'document_types'
        verbose_name = '资料类型'
        verbose_name_plural = '资料类型'
        ordering = ['sort_order', 'id']
    
    def __str__(self):
        return self.name


class Document(models.Model):
    """资料文档模型"""

    class Status(models.TextChoices):
        PENDING = 'pending', '待审核'
        APPROVED = 'approved', '已通过'
        REJECTED = 'rejected', '已拒绝'

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name='客户'
    )
    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.PROTECT,
        related_name='documents',
        verbose_name='资料类型'
    )
    file = models.FileField(
        upload_to=document_upload_path,
        verbose_name='文件'
    )
    file_name = models.CharField(max_length=255, verbose_name='文件名')
    file_size = models.IntegerField(default=0, verbose_name='文件大小(字节)')
    file_type = models.CharField(
        max_length=20,
        choices=FILE_TYPE_CHOICES,
        default='image',
        verbose_name='文件类型'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='状态'
    )
    notes = models.TextField(blank=True, null=True, verbose_name='备注')
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_documents',
        verbose_name='上传人'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'documents'
        verbose_name = '资料文档'
        verbose_name_plural = '资料文档'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.customer.name} - {self.document_type.name}"
    
    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
            if not self.file_name:
                self.file_name = os.path.basename(self.file.name)
        super().save(*args, **kwargs)

