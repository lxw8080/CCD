"""
文件验证工具
"""
import os
from django.core.exceptions import ValidationError
from .models import ALLOWED_EXTENSIONS, FILE_SIZE_LIMITS

# 允许的 MIME 类型映射，便于在缺少扩展名时识别文件类型
ALLOWED_MIME_TYPES = {
    'image': {
        'image/jpeg',
        'image/png',
        'image/gif',
        'image/bmp',
        'image/webp',
        'image/heic',
        'image/heif',
    },
    'video': {
        'video/mp4',
        'video/x-msvideo',
        'video/quicktime',
        'video/x-ms-wmv',
        'video/x-flv',
        'video/x-matroska',
        'video/3gpp',
        'video/3gpp2',
        'video/webm',
        'video/mpeg',
        'video/mp2t',
        'video/ogg',
    },
    'pdf': {
        'application/pdf',
    },
    'document': {
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain',
        'application/rtf',
    },
    'spreadsheet': {
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'text/csv',
    },
}


def get_file_extension(filename):
    """获取文件扩展名"""
    if not filename:
        return ''
    return os.path.splitext(filename)[1].lstrip('.').lower()


def _derive_type_from_extension(ext):
    for file_type, extensions in ALLOWED_EXTENSIONS.items():
        if ext in extensions:
            return file_type
    return None


def _derive_type_from_mime(mime):
    if not mime:
        return None

    normalized = mime.split(';')[0].strip().lower()

    for file_type, mime_types in ALLOWED_MIME_TYPES.items():
        if normalized in mime_types:
            return file_type

    if normalized.startswith('image/'):
        return 'image'
    if normalized.startswith('video/'):
        return 'video'

    return None


def get_file_type(filename, content_type=None):
    """
    根据文件扩展名或 MIME 类型获取文件类型
    """
    ext = get_file_extension(filename)
    file_type = _derive_type_from_extension(ext)
    if file_type:
        return file_type

    file_type = _derive_type_from_mime(content_type)
    if file_type:
        return file_type

    return None


def validate_file_type(file):
    """验证文件类型"""
    file_type = get_file_type(
        file.name,
        getattr(file, 'content_type', None)
    )

    if file_type is None:
        allowed_exts = []
        for extensions in ALLOWED_EXTENSIONS.values():
            allowed_exts.extend(extensions)
        raise ValidationError(
            f'不支持的文件类型。允许的文件扩展名: {", ".join(sorted(set(allowed_exts)))}'
        )

    return file_type


def validate_file_size(file, file_type):
    """验证文件大小（当前无大小限制）"""
    max_size = FILE_SIZE_LIMITS.get(file_type)

    if not max_size:
        return

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
        'spreadsheet': '表格',
    }
    return type_map.get(file_type, '未知')


def get_file_icon_class(file_type):
    """获取文件类型的图标类名"""
    icon_map = {
        'image': 'el-icon-picture',
        'video': 'el-icon-video-play',
        'pdf': 'el-icon-document-copy',
        'document': 'el-icon-document',
        'spreadsheet': 'el-icon-document',
    }
    return icon_map.get(file_type, 'el-icon-document')
