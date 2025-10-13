from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """自定义用户模型"""
    
    class Role(models.TextChoices):
        ADMIN = 'admin', '管理员'
        STAFF = 'staff', '客服人员'
        AUDITOR = 'auditor', '审核人员'
    
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STAFF,
        verbose_name='角色'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='手机号'
    )
    
    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = '用户'
    
    def __str__(self):
        return self.username

