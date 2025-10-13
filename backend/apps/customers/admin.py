from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'id_card', 'phone', 'status', 'created_by', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'id_card', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'id_card', 'phone', 'address')
        }),
        ('状态信息', {
            'fields': ('status', 'remarks')
        }),
        ('系统信息', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )

