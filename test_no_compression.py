#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试移除压缩功能
"""

import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_no_compression():
    """检查是否已移除压缩功能"""
    
    mobile_detail_path = 'frontend/src/views/mobile/CustomerDetail.vue'
    
    print("=" * 70)
    print("检查移除压缩功能")
    print("=" * 70)
    
    if not os.path.exists(mobile_detail_path):
        print("[ERROR] 文件不存在: {}".format(mobile_detail_path))
        return False
    
    with open(mobile_detail_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否移除了 compressImage 导入
    print("\n1. 检查导入:")
    print("-" * 70)
    
    if 'compressImage' not in content:
        print("[OK] 已移除 compressImage 导入")
        import_ok = True
    else:
        print("[ERROR] 仍然存在 compressImage 导入")
        import_ok = False
    
    if 'formatFileSize' in content:
        print("[OK] formatFileSize 导入已保留")
        format_ok = True
    else:
        print("[ERROR] formatFileSize 导入被移除")
        format_ok = False
    
    # 检查 handleUpload 函数
    print("\n2. 检查 handleUpload 函数:")
    print("-" * 70)
    
    if 'formData.append(\'file\', item.file)' in content:
        print("[OK] 直接上传原始文件")
        upload_ok = True
    else:
        print("[ERROR] 未找到直接上传原始文件的代码")
        upload_ok = False
    
    if 'compressImage' not in content:
        print("[OK] 已移除所有压缩相关代码")
        no_compress_ok = True
    else:
        print("[ERROR] 仍然存在压缩相关代码")
        no_compress_ok = False
    
    # 检查验证逻辑是否保持不变
    print("\n3. 检查验证逻辑:")
    print("-" * 70)
    
    validation_checks = [
        ('uploadForm.documentType', '资料类型验证'),
        ('getFileType', '文件类型检查'),
        ('allowed_file_types', '允许的文件类型检查'),
        ('getFileSizeLimit', '文件大小限制检查'),
    ]
    
    all_validation_ok = True
    for check_str, check_desc in validation_checks:
        if check_str in content:
            print("[OK] {} - {}".format(check_desc, check_str))
        else:
            print("[ERROR] {} - {} 未找到".format(check_desc, check_str))
            all_validation_ok = False
    
    # 检查错误处理
    print("\n4. 检查错误处理:")
    print("-" * 70)
    
    error_checks = [
        ('error.response?.data?.error', '后端错误处理'),
        ('error.message', '错误消息处理'),
        ('console.error', '错误日志'),
    ]
    
    all_error_ok = True
    for check_str, check_desc in error_checks:
        if check_str in content:
            print("[OK] {} - {}".format(check_desc, check_str))
        else:
            print("[ERROR] {} - {} 未找到".format(check_desc, check_str))
            all_error_ok = False
    
    print("\n" + "=" * 70)
    print("检查结果总结")
    print("=" * 70)
    
    all_ok = import_ok and format_ok and upload_ok and no_compress_ok and all_validation_ok and all_error_ok
    
    if all_ok:
        print("\n[OK] 所有检查都通过了")
        print("\n修改内容:")
        print("  1. 已移除 compressImage 导入")
        print("  2. 已移除所有压缩相关代码")
        print("  3. 直接上传原始文件")
        print("  4. 验证逻辑保持不变")
        print("  5. 错误处理保持不变")
        print("\n预期效果:")
        print("  ✅ 所有文件类型都直接上传，不进行压缩")
        print("  ✅ 视频可以正常上传")
        print("  ✅ PDF 可以正常上传")
        print("  ✅ 文档可以正常上传")
        print("  ✅ 图片也不会被压缩，直接上传")
        print("  ✅ 上传速度更快")
        return True
    else:
        print("\n[ERROR] 检查失败，请检查上述错误")
        return False

def main():
    """主函数"""
    
    print("\n")
    print("*" * 70)
    print("移除压缩功能检查")
    print("*" * 70)
    print("\n")
    
    result = check_no_compression()
    
    return 0 if result else 1

if __name__ == '__main__':
    sys.exit(main())

