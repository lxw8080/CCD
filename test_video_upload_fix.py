#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试视频上传和显示问题修复
"""

import os
import sys
import re

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_video_upload_fix():
    """检查视频上传问题是否已修复"""
    
    mobile_detail_path = 'frontend/src/views/mobile/CustomerDetail.vue'
    
    print("=" * 70)
    print("检查视频上传和显示问题修复")
    print("=" * 70)
    
    if not os.path.exists(mobile_detail_path):
        print("[ERROR] 文件不存在: {}".format(mobile_detail_path))
        return False
    
    with open(mobile_detail_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查 afterRead 函数
    print("\n1. 检查 afterRead 函数:")
    print("-" * 70)
    
    if 'const afterRead = (file) => {' in content:
        print("[OK] afterRead 已改为同步函数")
        afterread_ok = True
    else:
        print("[ERROR] afterRead 未改为同步函数")
        afterread_ok = False
    
    # 检查是否移除了不必要的 await
    if 'await new Promise(resolve => setTimeout(resolve, 0))' not in content:
        print("[OK] 已移除不必要的异步延迟处理")
        no_await_ok = True
    else:
        print("[ERROR] 仍然存在不必要的异步延迟处理")
        no_await_ok = False
    
    # 检查 handleUpload 函数中的文件类型检查
    print("\n2. 检查 handleUpload 函数:")
    print("-" * 70)
    
    checks = [
        ('const fileType = getFileType(item.file.name)', '获取文件类型'),
        ('if (fileType === \'image\')', '图片类型判断'),
        ('uploadFile = await compressImage(item.file)', '图片压缩'),
        ('uploadFile = item.file', '使用原始文件'),
    ]
    
    all_checks_ok = True
    for check_str, check_desc in checks:
        if check_str in content:
            print("[OK] {} - {}".format(check_desc, check_str))
        else:
            print("[ERROR] {} - {} 未找到".format(check_desc, check_str))
            all_checks_ok = False
    
    # 检查错误处理
    print("\n3. 检查错误处理:")
    print("-" * 70)
    
    error_checks = [
        ('error.response?.data?.error', '后端错误处理'),
        ('error.message', '错误消息处理'),
        ('console.error(\'上传错误:\', error)', '错误日志'),
    ]
    
    all_error_ok = True
    for check_str, check_desc in error_checks:
        if check_str in content:
            print("[OK] {} - {}".format(check_desc, check_str))
        else:
            print("[ERROR] {} - {} 未找到".format(check_desc, check_str))
            all_error_ok = False
    
    # 检查验证逻辑是否保持不变
    print("\n4. 检查验证逻辑:")
    print("-" * 70)
    
    validation_checks = [
        ('uploadForm.documentType', '资料类型验证'),
        ('getFileType(file.file.name)', '文件类型检查'),
        ('allowed_file_types.includes(fileType)', '允许的文件类型检查'),
        ('getFileSizeLimit(fileType)', '文件大小限制检查'),
    ]
    
    all_validation_ok = True
    for check_str, check_desc in validation_checks:
        if check_str in content:
            print("[OK] {} - {}".format(check_desc, check_str))
        else:
            print("[ERROR] {} - {} 未找到".format(check_desc, check_str))
            all_validation_ok = False
    
    print("\n" + "=" * 70)
    print("检查结果总结")
    print("=" * 70)
    
    all_ok = afterread_ok and no_await_ok and all_checks_ok and all_error_ok and all_validation_ok
    
    if all_ok:
        print("\n[OK] 所有检查都通过了")
        print("\n修复效果:")
        print("  1. afterRead 已改为同步函数")
        print("  2. 已移除不必要的异步延迟处理")
        print("  3. handleUpload 只对图片文件进行压缩")
        print("  4. 其他文件类型直接上传")
        print("  5. 错误处理更加完善")
        print("\n预期改进:")
        print("  ✅ 视频拍摄后能正确显示到页面中")
        print("  ✅ 所有文件类型都能正常上传")
        print("  ✅ 视频可以正常上传")
        print("  ✅ PDF 可以正常上传")
        print("  ✅ 文档可以正常上传")
        print("  ✅ 图片仍然被压缩处理")
        print("  ✅ 错误提示更加清晰")
        return True
    else:
        print("\n[ERROR] 检查失败，请检查上述错误")
        return False

def main():
    """主函数"""
    
    print("\n")
    print("*" * 70)
    print("视频上传和显示问题修复检查")
    print("*" * 70)
    print("\n")
    
    result = check_video_upload_fix()
    
    return 0 if result else 1

if __name__ == '__main__':
    sys.exit(main())

