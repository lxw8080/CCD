from django.contrib import admin
from .models import Customer, CustomField, CustomFieldValue


@admin.register(CustomField)
class CustomFieldAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'field_type', 'is_required', 'sort_order',
        'is_active', 'created_at'
    ]
    list_filter = ['field_type', 'is_required', 'is_active', 'created_at']
    search_fields = ['name', 'help_text']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['sort_order', 'id']
    fieldsets = (
        ('基本信息', {
            'fields': (
                'name', 'field_type', 'is_required',
                'sort_order', 'is_active'
            )
        }),
        ('显示设置', {
            'fields': ('placeholder', 'help_text', 'default_value')
        }),
        ('选项设置', {
            'fields': ('options',),
            'description': '仅用于下拉菜单类型，格式: ["选项1", "选项2", "选项3"]'
        }),
        ('验证规则', {
            'fields': (
                'min_length', 'max_length',
                'min_value', 'max_value',
                'regex_pattern'
            ),
            'classes': ('collapse',)
        }),
        ('系统信息', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(CustomFieldValue)
class CustomFieldValueAdmin(admin.ModelAdmin):
    list_display = [
        'customer', 'custom_field', 'value', 'created_at'
    ]
    list_filter = ['custom_field', 'created_at']
    search_fields = ['customer__name', 'customer__id_card', 'value']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('关联信息', {
            'fields': ('customer', 'custom_field')
        }),
        ('字段值', {
            'fields': ('value',)
        }),
        ('系统信息', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'id_card', 'phone', 'status',
        'created_by', 'created_at'
    ]
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'id_card', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'id_card', 'phone', 'address')
        }),
        ('状态信息', {
            'fields': ('status',)
        }),
        ('系统信息', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )

