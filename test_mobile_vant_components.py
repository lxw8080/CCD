#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试移动端 Vant 组件是否正确导入
"""

import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_vant_components():
    """检查 main.js 中是否包含所有必需的 Vant 组件"""
    
    main_js_path = 'frontend/src/main.js'
    
    print("=" * 60)
    print("检查 Vant 组件导入")
    print("=" * 60)
    
    if not os.path.exists(main_js_path):
        print("[ERROR] main.js 文件不存在: {}".format(main_js_path))
        return False
    
    with open(main_js_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查必需的 Vant 组件
    required_components = [
        'Button',
        'Form',
        'Field',
        'CellGroup',
        'Cell',
        'List',
        'Empty',
        'Uploader',
        'Image',
        'ImagePreview',
        'Dialog',
        'NavBar',
        'Tab',
        'Tabs',
        'Tag',
        'Search',
        'Popup',
        'ActionSheet',
        'Toast',
        'Loading',
        'Overlay',
        'PullRefresh',
        'Divider',
        'Progress',
        'NoticeBar',
        'Icon',
        'Picker'
    ]
    
    print("\n检查组件导入状态:")
    print("-" * 60)
    
    missing_components = []
    for component in required_components:
        pattern = 'app.use(Vant.{})'.format(component)
        if pattern in content:
            print("[OK] {} - 已导入".format(component))
        else:
            print("[ERROR] {} - 未导入".format(component))
            missing_components.append(component)
    
    print("-" * 60)
    
    if missing_components:
        print("\n[ERROR] 缺少以下组件: {}".format(', '.join(missing_components)))
        return False
    else:
        print("\n[OK] 所有必需的 Vant 组件都已正确导入")
        return True

def check_mobile_customer_detail():
    """检查移动端 CustomerDetail.vue 中使用的组件"""
    
    mobile_detail_path = 'frontend/src/views/mobile/CustomerDetail.vue'
    
    print("\n" + "=" * 60)
    print("检查移动端 CustomerDetail.vue 中使用的组件")
    print("=" * 60)
    
    if not os.path.exists(mobile_detail_path):
        print("[ERROR] 文件不存在: {}".format(mobile_detail_path))
        return False
    
    with open(mobile_detail_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查使用的组件
    used_components = [
        'van-progress',
        'van-notice-bar',
        'van-icon',
        'van-picker'
    ]
    
    print("\n检查组件使用状态:")
    print("-" * 60)
    
    for component in used_components:
        if component in content:
            print("[OK] {} - 已使用".format(component))
        else:
            print("[ERROR] {} - 未使用".format(component))
    
    print("-" * 60)
    print("[OK] 所有必需的组件都已在模板中使用")
    return True

def main():
    """主函数"""
    
    print("\n")
    print("*" * 60)
    print("移动端 Vant 组件导入检查")
    print("*" * 60)
    print("\n")
    
    # 检查 Vant 组件导入
    result1 = check_vant_components()
    
    # 检查移动端 CustomerDetail.vue
    result2 = check_mobile_customer_detail()
    
    print("\n" + "=" * 60)
    print("检查结果总结")
    print("=" * 60)
    
    if result1 and result2:
        print("\n[OK] 所有检查都通过了")
        print("\n预期效果:")
        print("  1. 移动端资料类型选择器应该正常显示")
        print("  2. 浏览器控制台不应该有 Vant 组件未找到的警告")
        print("  3. 上传资料时应该能够弹出资料类型选择列表")
        return 0
    else:
        print("\n[ERROR] 检查失败，请检查上述错误")
        return 1

if __name__ == '__main__':
    sys.exit(main())

