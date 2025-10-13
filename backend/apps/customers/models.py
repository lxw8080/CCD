from django.db import models
from django.conf import settings


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
    remarks = models.TextField(blank=True, null=True, verbose_name='备注')
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

