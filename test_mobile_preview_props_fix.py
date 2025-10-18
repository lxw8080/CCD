#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试移动端文件预览 Props 传递问题修复
"""

import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_mobile_preview_props_fix():
    """检查移动端文件预览 Props 传递问题是否已修复"""
    
    mobile_detail_path = 'frontend/src/views/mobile/CustomerDetail.vue'
    
    print("=" * 70)
    print("检查移动端文件预览 Props 传递问题修复")
    print("=" * 70)
    
    # 检查 CustomerDetail.vue
    print("\n1. 检查 CustomerDetail.vue:")
    print("-" * 70)
    
    if not os.path.exists(mobile_detail_path):
        print("[ERROR] 文件不存在: {}".format(mobile_detail_path))
        return False
    
    with open(mobile_detail_path, 'r', encoding='utf-8') as f:
        detail_content = f.read()
    
    # 检查是否使用了 kebab-case
    kebab_case_checks = [
        (':file-url="previewUrl"', 'file-url prop (kebab-case)'),
        (':file-name="previewFileName"', 'file-name prop (kebab-case)'),
        (':file-type="previewFileType"', 'file-type prop (kebab-case)'),
    ]
    
    # 检查是否还有 camelCase（不应该存在）
    camel_case_checks = [
        (':fileUrl="previewUrl"', 'fileUrl prop (camelCase) - 不应该存在'),
        (':fileName="previewFileName"', 'fileName prop (camelCase) - 不应该存在'),
        (':fileType="previewFileType"', 'fileType prop (camelCase) - 不应该存在'),
    ]
    
    all_ok = True
    
    # 检查 kebab-case
    for check_str, check_desc in kebab_case_checks:
        if check_str in detail_content:
            print("[OK] {} - {}".format(check_desc, check_str))
        else:
            print("[ERROR] {} - {} 未找到".format(check_desc, check_str))
            all_ok = False
    
    # 检查 camelCase（不应该存在）
    for check_str, check_desc in camel_case_checks:
        if check_str in detail_content:
            print("[ERROR] {} - {} 仍然存在（应该已被替换）".format(check_desc, check_str))
            all_ok = False
        else:
            print("[OK] {} - 已正确替换为 kebab-case".format(check_desc))
    
    print("\n" + "=" * 70)
    print("检查结果总结")
    print("=" * 70)
    
    if all_ok:
        print("\n[OK] 所有检查都通过了")
        print("\n修改内容:")
        print("  1. 将 :fileUrl 改为 :file-url")
        print("  2. 将 :fileName 改为 :file-name")
        print("  3. 将 :fileType 改为 :file-type")
        print("\n问题原因:")
        print("  在 Vue 3 中，HTML 属性应该使用 kebab-case 格式")
        print("  使用 camelCase 会导致 props 无法正确传递")
        print("\n预期效果:")
        print("  ✅ Props 能正确传递给 MobilePreviewDialog 组件")
        print("  ✅ 图片能正常预览")
        print("  ✅ 视频能正常播放")
        print("  ✅ PDF 能正常显示")
        print("\n测试方法:")
        print("  1. 打开移动端页面: http://127.0.0.1:3001/customers/5")
        print("  2. 打开浏览器开发者工具")
        print("  3. 切换到 Console 标签")
        print("  4. 点击预览文件")
        print("  5. 查看控制台输出，确认 file-type 正确传递")
        print("  6. 确认文件能正常预览")
        return True
    else:
        print("\n[ERROR] 检查失败，请检查上述错误")
        return False

def main():
    """主函数"""
    
    print("\n")
    print("*" * 70)
    print("移动端文件预览 Props 传递问题修复检查")
    print("*" * 70)
    print("\n")
    
    result = check_mobile_preview_props_fix()
    
    return 0 if result else 1

if __name__ == '__main__':
    sys.exit(main())

