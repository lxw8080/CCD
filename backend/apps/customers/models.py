from django.db import models
from django.conf import settings


class CustomField(models.Model):
    """自定义字段模型"""

    class FieldType(models.TextChoices):
        TEXT = 'text', '文本'
        NUMBER = 'number', '数字'
        DATE = 'date', '日期'
        SELECT = 'select', '下拉菜单'
        TEXTAREA = 'textarea', '多行文本'
        EMAIL = 'email', '邮箱'
        PHONE = 'phone', '手机号'
        URL = 'url', '网址'

    name = models.CharField(max_length=100, verbose_name='字段名称')
    field_type = models.CharField(
        max_length=20,
        choices=FieldType.choices,
        default=FieldType.TEXT,
        verbose_name='字段类型'
    )
    is_required = models.BooleanField(default=False, verbose_name='是否必填')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    placeholder = models.CharField(max_length=255, blank=True, null=True, verbose_name='占位符')
    help_text = models.CharField(max_length=255, blank=True, null=True, verbose_name='帮助文本')
    default_value = models.CharField(max_length=255, blank=True, null=True, verbose_name='默认值')

    # For select type fields - store options as JSON
    options = models.JSONField(
        default=list,
        blank=True,
        verbose_name='选项列表',
        help_text='下拉菜单的选项，格式: ["选项1", "选项2", "选项3"]'
    )

    # Validation rules
    min_length = models.IntegerField(blank=True, null=True, verbose_name='最小长度')
    max_length = models.IntegerField(blank=True, null=True, verbose_name='最大长度')
    min_value = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name='最小值')
    max_value = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name='最大值')
    regex_pattern = models.CharField(max_length=255, blank=True, null=True, verbose_name='正则表达式')

    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'custom_fields'
        verbose_name = '自定义字段'
        verbose_name_plural = '自定义字段'
        ordering = ['sort_order', 'id']

    def __str__(self):
        return f"{self.name} ({self.get_field_type_display()})"


class Customer(models.Model):
    """客户模型"""

    class Status(models.TextChoices):
        PENDING = 'pending', '资料收集中'
        COMPLETE = 'complete', '资料已齐全'
        REVIEWING = 'reviewing', '审核中'
        APPROVED = 'approved', '已通过'
        REJECTED = 'rejected', '已拒绝'

    name = models.CharField(max_length=100, verbose_name='姓名')
    id_card = models.CharField(max_length=18, unique=True, verbose_name='身份证号')
    phone = models.CharField(max_length=20, verbose_name='手机号')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='地址')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='状态'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_customers',
        verbose_name='创建人'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'customers'
        verbose_name = '客户'
        verbose_name_plural = '客户'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.id_card}"


class CustomFieldValue(models.Model):
    """自定义字段值模型"""

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='custom_field_values',
        verbose_name='客户'
    )
    custom_field = models.ForeignKey(
        CustomField,
        on_delete=models.CASCADE,
        related_name='values',
        verbose_name='自定义字段'
    )
    value = models.TextField(blank=True, null=True, verbose_name='字段值')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'custom_field_values'
        verbose_name = '自定义字段值'
        verbose_name_plural = '自定义字段值'
        unique_together = ['customer', 'custom_field']
        ordering = ['custom_field__sort_order', 'id']

    def __str__(self):
        return f"{self.customer.name} - {self.custom_field.name}: {self.value}"

