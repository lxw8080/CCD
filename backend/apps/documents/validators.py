"""
文件验证器
"""
import os
from django.core.exceptions import ValidationError
from .models import ALLOWED_EXTENSIONS, FILE_SIZE_LIMITS


def get_file_extension(filename):
    """获取文件扩展名"""
    return os.path.splitext(filename)[1].lstrip('.').lower()


def get_file_type(filename):
    """根据文件扩展名获取文件类型"""
    ext = get_file_extension(filename)
    
    for file_type, extensions in ALLOWED_EXTENSIONS.items():
        if ext in extensions:
            return file_type
    
    return None


def validate_file_type(file):
    """验证文件类型"""
    file_type = get_file_type(file.name)
    
    if file_type is None:
        allowed_exts = []
        for extensions in ALLOWED_EXTENSIONS.values():
            allowed_exts.extend(extensions)
        raise ValidationError(
            f'不支持的文件类型。允许的文件类型: {", ".join(allowed_exts)}'
        )
    
    return file_type


def validate_file_size(file, file_type):
    """验证文件大小"""
    max_size = FILE_SIZE_LIMITS.get(file_type, 10 * 1024 * 1024)
    
    if file.size > max_size:
        max_size_mb = max_size / (1024 * 1024)
        raise ValidationError(
            f'{file_type}文件大小不能超过 {max_size_mb:.0f}MB'
        )


def validate_document_file(file):
    """验证文档文件"""
    # 验证文件类型
    file_type = validate_file_type(file)
    
    # 验证文件大小
    validate_file_size(file, file_type)
    
    return file_type


def get_file_type_display(file_type):
    """获取文件类型的显示名称"""
    type_map = {
        'image': '图片',
        'video': '视频',
        'pdf': 'PDF',
        'document': '文档',
        'spreadsheet': '表格'
    }
    return type_map.get(file_type, '未知')


def get_file_icon_class(file_type):
    """获取文件类型的图标类名"""
    icon_map = {
        'image': 'el-icon-picture',
        'video': 'el-icon-video-play',
        'pdf': 'el-icon-document-copy',
        'document': 'el-icon-document',
        'spreadsheet': 'el-icon-document'
    }
    return icon_map.get(file_type, 'el-icon-document')

