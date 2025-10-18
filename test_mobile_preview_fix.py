#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试移动端文件预览问题修复
"""

import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_mobile_preview_fix():
    """检查移动端文件预览问题是否已修复"""
    
    mobile_detail_path = 'frontend/src/views/mobile/CustomerDetail.vue'
    mobile_preview_path = 'frontend/src/components/FilePreview/MobilePreviewDialog.vue'
    
    print("=" * 70)
    print("检查移动端文件预览问题修复")
    print("=" * 70)
    
    # 检查 CustomerDetail.vue
    print("\n1. 检查 CustomerDetail.vue:")
    print("-" * 70)
    
    if not os.path.exists(mobile_detail_path):
        print("[ERROR] 文件不存在: {}".format(mobile_detail_path))
        return False
    
    with open(mobile_detail_path, 'r', encoding='utf-8') as f:
        detail_content = f.read()
    
    detail_checks = [
        ('getFileType(doc.file_name)', '从文件名获取文件类型'),
        ('console.log(\'预览文件:\'', '添加调试日志'),
        ('rawType: doc.file_type', '记录原始文件类型'),
    ]
    
    all_detail_ok = True
    for check_str, check_desc in detail_checks:
        if check_str in detail_content:
            print("[OK] {} - {}".format(check_desc, check_str))
        else:
            print("[ERROR] {} - {} 未找到".format(check_desc, check_str))
            all_detail_ok = False
    
    # 检查 MobilePreviewDialog.vue
    print("\n2. 检查 MobilePreviewDialog.vue:")
    print("-" * 70)
    
    if not os.path.exists(mobile_preview_path):
        print("[ERROR] 文件不存在: {}".format(mobile_preview_path))
        return False
    
    with open(mobile_preview_path, 'r', encoding='utf-8') as f:
        preview_content = f.read()
    
    preview_checks = [
        ('import { showToast } from \'vant\'', '导入 showToast'),
        ('console.log(\'显示预览:\'', '添加预览调试日志'),
        ('console.log(\'显示图片预览\')', '添加图片预览日志'),
        ('console.log(\'显示视频预览\')', '添加视频预览日志'),
        ('console.log(\'显示 PDF 预览\')', '添加 PDF 预览日志'),
        ('console.log(\'加载 PDF:\'', '添加 PDF 加载日志'),
        ('console.log(\'PDF 加载成功', '添加 PDF 加载成功日志'),
        ('showToast(\'PDF 加载失败:', 'PDF 加载失败提示'),
        ('console.log(\'渲染 PDF 第\'', '添加 PDF 渲染日志'),
        ('showToast(\'PDF 渲染失败:', 'PDF 渲染失败提示'),
    ]
    
    all_preview_ok = True
    for check_str, check_desc in preview_checks:
        if check_str in preview_content:
            print("[OK] {} - {}".format(check_desc, check_str))
        else:
            print("[ERROR] {} - {} 未找到".format(check_desc, check_str))
            all_preview_ok = False
    
    # 检查错误处理
    print("\n3. 检查错误处理:")
    print("-" * 70)
    
    error_checks = [
        ('if (!canvas)', 'Canvas 元素检查'),
        ('console.error(\'Canvas 元素不存在\')', 'Canvas 错误日志'),
        ('console.error(\'PDF 加载失败:\'', 'PDF 加载错误日志'),
        ('console.error(\'PDF 渲染失败:\'', 'PDF 渲染错误日志'),
    ]
    
    all_error_ok = True
    for check_str, check_desc in error_checks:
        if check_str in preview_content:
            print("[OK] {} - {}".format(check_desc, check_str))
        else:
            print("[ERROR] {} - {} 未找到".format(check_desc, check_str))
            all_error_ok = False
    
    print("\n" + "=" * 70)
    print("检查结果总结")
    print("=" * 70)
    
    all_ok = all_detail_ok and all_preview_ok and all_error_ok
    
    if all_ok:
        print("\n[OK] 所有检查都通过了")
        print("\n修改内容:")
        print("  1. 改进了文件类型获取逻辑")
        print("  2. 添加了详细的调试日志")
        print("  3. 改进了错误处理")
        print("  4. 添加了用户友好的错误提示")
        print("\n预期效果:")
        print("  ✅ 能正确识别文件类型")
        print("  ✅ 图片能正常预览")
        print("  ✅ 视频能正常播放")
        print("  ✅ PDF 能正常显示")
        print("  ✅ 错误信息清晰明确")
        print("  ✅ 便于调试和排查问题")
        print("\n调试方法:")
        print("  1. 打开浏览器开发者工具")
        print("  2. 切换到 Console 标签")
        print("  3. 点击预览文件")
        print("  4. 查看控制台输出的调试信息")
        return True
    else:
        print("\n[ERROR] 检查失败，请检查上述错误")
        return False

def main():
    """主函数"""
    
    print("\n")
    print("*" * 70)
    print("移动端文件预览问题修复检查")
    print("*" * 70)
    print("\n")
    
    result = check_mobile_preview_fix()
    
    return 0 if result else 1

if __name__ == '__main__':
    sys.exit(main())

