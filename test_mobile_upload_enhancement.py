#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试移动端文件上传功能增强
"""

import os
import sys
import re

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_mobile_customer_detail():
    """检查移动端 CustomerDetail.vue 中的文件上传功能增强"""
    
    mobile_detail_path = 'frontend/src/views/mobile/CustomerDetail.vue'
    
    print("=" * 70)
    print("检查移动端文件上传功能增强")
    print("=" * 70)
    
    if not os.path.exists(mobile_detail_path):
        print("[ERROR] 文件不存在: {}".format(mobile_detail_path))
        return False
    
    with open(mobile_detail_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查导入
    print("\n1. 检查文件类型工具函数导入:")
    print("-" * 70)
    
    required_imports = [
        'getFileType',
        'getFileTypeName',
        'getFileSizeLimit',
        'formatFileSizeLimit'
    ]
    
    all_imports_ok = True
    for import_name in required_imports:
        if import_name in content:
            print("[OK] {} - 已导入".format(import_name))
        else:
            print("[ERROR] {} - 未导入".format(import_name))
            all_imports_ok = False
    
    # 检查计算属性
    print("\n2. 检查计算属性:")
    print("-" * 70)
    
    computed_properties = [
        ('uploaderAccept', '动态 accept 属性'),
        ('uploaderCapture', '动态 capture 属性')
    ]
    
    all_computed_ok = True
    for prop_name, prop_desc in computed_properties:
        if 'const {} = computed'.format(prop_name) in content:
            print("[OK] {} - {} 已添加".format(prop_name, prop_desc))
        else:
            print("[ERROR] {} - {} 未添加".format(prop_name, prop_desc))
            all_computed_ok = False
    
    # 检查 van-uploader 配置
    print("\n3. 检查 van-uploader 配置:")
    print("-" * 70)
    
    uploader_checks = [
        (':accept="uploaderAccept"', 'accept 属性绑定'),
        (':capture="uploaderCapture"', 'capture 属性绑定')
    ]
    
    all_uploader_ok = True
    for check_str, check_desc in uploader_checks:
        if check_str in content:
            print("[OK] {} - {}".format(check_desc, check_str))
        else:
            print("[ERROR] {} - {} 未找到".format(check_desc, check_str))
            all_uploader_ok = False
    
    # 检查 afterRead 函数增强
    print("\n4. 检查 afterRead 函数增强:")
    print("-" * 70)
    
    afterread_checks = [
        ('getFileType(file.file.name)', '获取文件类型'),
        ('getFileSizeLimit(fileType)', '获取文件大小限制'),
        ('formatFileSizeLimit(fileType)', '格式化文件大小限制'),
        ('showToast', '显示提示信息')
    ]
    
    all_afterread_ok = True
    for check_str, check_desc in afterread_checks:
        if check_str in content:
            print("[OK] {} - {}".format(check_desc, check_str))
        else:
            print("[ERROR] {} - {} 未找到".format(check_desc, check_str))
            all_afterread_ok = False
    
    # 检查 handleUpload 函数增强
    print("\n5. 检查 handleUpload 函数增强:")
    print("-" * 70)
    
    handleupload_checks = [
        ('上传前再次验证所有文件', '上传前验证注释'),
        ('for (const item of fileList.value)', '文件循环验证'),
        ('getFileType(item.file.name)', '获取文件类型'),
        ('getFileSizeLimit(fileType)', '获取文件大小限制')
    ]
    
    all_handleupload_ok = True
    for check_str, check_desc in handleupload_checks:
        if check_str in content:
            print("[OK] {} - {}".format(check_desc, check_str))
        else:
            print("[ERROR] {} - {} 未找到".format(check_desc, check_str))
            all_handleupload_ok = False
    
    print("\n" + "=" * 70)
    print("检查结果总结")
    print("=" * 70)
    
    all_ok = all_imports_ok and all_computed_ok and all_uploader_ok and all_afterread_ok and all_handleupload_ok
    
    if all_ok:
        print("\n[OK] 所有检查都通过了")
        print("\n预期效果:")
        print("  1. 根据资料类型动态设置允许的文件类型")
        print("  2. 根据文件类型动态设置摄像头模式")
        print("  3. 支持从相册选择图片")
        print("  4. 支持拍照上传")
        print("  5. 支持录制视频")
        print("  6. 支持从文件管理器选择文件")
        print("  7. 文件类型和大小验证正常")
        print("  8. 错误提示清晰")
        return True
    else:
        print("\n[ERROR] 检查失败，请检查上述错误")
        return False

def main():
    """主函数"""
    
    print("\n")
    print("*" * 70)
    print("移动端文件上传功能增强检查")
    print("*" * 70)
    print("\n")
    
    result = check_mobile_customer_detail()
    
    return 0 if result else 1

if __name__ == '__main__':
    sys.exit(main())

