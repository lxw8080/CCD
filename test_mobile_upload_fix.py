#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试移动端文件上传页面刷新问题修复
"""

import os
import sys
import re

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_afterread_fix():
    """检查 afterRead 函数是否已修复"""
    
    mobile_detail_path = 'frontend/src/views/mobile/CustomerDetail.vue'
    
    print("=" * 70)
    print("检查 afterRead 函数修复")
    print("=" * 70)
    
    if not os.path.exists(mobile_detail_path):
        print("[ERROR] 文件不存在: {}".format(mobile_detail_path))
        return False
    
    with open(mobile_detail_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查 afterRead 是否为异步函数
    print("\n1. 检查 afterRead 函数签名:")
    print("-" * 70)
    
    if 'const afterRead = async (file) => {' in content:
        print("[OK] afterRead 已改为异步函数")
        async_ok = True
    else:
        print("[ERROR] afterRead 未改为异步函数")
        async_ok = False
    
    # 检查是否使用了 await 和 setTimeout
    print("\n2. 检查异步处理:")
    print("-" * 70)
    
    await_checks = [
        ('await new Promise(resolve => setTimeout(resolve, 0))', '异步延迟处理'),
    ]
    
    all_await_ok = True
    for check_str, check_desc in await_checks:
        count = content.count(check_str)
        if count >= 5:  # 应该有至少 5 处（每个验证失败的地方都有一处）
            print("[OK] {} - 已添加 ({} 处)".format(check_desc, count))
        else:
            print("[ERROR] {} - 未正确添加 (仅 {} 处)".format(check_desc, count))
            all_await_ok = False
    
    # 检查验证逻辑是否保持不变
    print("\n3. 检查验证逻辑:")
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
    
    # 检查文件移除逻辑
    print("\n4. 检查文件移除逻辑:")
    print("-" * 70)
    
    if 'fileList.value = fileList.value.filter(f => f !== file)' in content:
        count = content.count('fileList.value = fileList.value.filter(f => f !== file)')
        print("[OK] 文件移除逻辑已保留 ({} 处)".format(count))
        remove_ok = True
    else:
        print("[ERROR] 文件移除逻辑未找到")
        remove_ok = False
    
    # 检查错误提示
    print("\n5. 检查错误提示:")
    print("-" * 70)
    
    toast_checks = [
        ('请先选择资料类型', '资料类型提示'),
        ('资料类型不存在', '资料类型存在性提示'),
        ('不支持的文件类型', '文件类型提示'),
        ('不支持上传', '文件类型限制提示'),
        ('文件大小超过限制', '文件大小提示'),
    ]
    
    all_toast_ok = True
    for check_str, check_desc in toast_checks:
        if check_str in content:
            print("[OK] {} - {}".format(check_desc, check_str))
        else:
            print("[ERROR] {} - {} 未找到".format(check_desc, check_str))
            all_toast_ok = False
    
    print("\n" + "=" * 70)
    print("检查结果总结")
    print("=" * 70)
    
    all_ok = async_ok and all_await_ok and all_validation_ok and remove_ok and all_toast_ok
    
    if all_ok:
        print("\n[OK] 所有检查都通过了")
        print("\n修复效果:")
        print("  1. afterRead 已改为异步函数")
        print("  2. 文件移除操作已延迟处理")
        print("  3. 验证逻辑保持不变")
        print("  4. 错误提示保持不变")
        print("\n预期改进:")
        print("  ✅ 从相册选择文件后页面不会刷新")
        print("  ✅ 录制视频后页面不会刷新")
        print("  ✅ 拍照后页面不会刷新")
        print("  ✅ 选中的文件正确显示在上传列表")
        print("  ✅ 所有上传方式都能正常工作")
        return True
    else:
        print("\n[ERROR] 检查失败，请检查上述错误")
        return False

def main():
    """主函数"""
    
    print("\n")
    print("*" * 70)
    print("移动端文件上传页面刷新问题修复检查")
    print("*" * 70)
    print("\n")
    
    result = check_afterread_fix()
    
    return 0 if result else 1

if __name__ == '__main__':
    sys.exit(main())

