#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试文档 API 返回的数据
"""

import requests
import json

# API 基础 URL
BASE_URL = 'http://127.0.0.1:8000'

# 登录获取 token
def login():
    """登录获取 token"""
    url = f'{BASE_URL}/api/auth/login/'
    data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 登录成功")
            return result.get('access')
        else:
            print(f"❌ 登录失败: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ 登录错误: {e}")
        return None

# 获取客户文档
def get_documents(token, customer_id=3):
    """获取客户文档"""
    url = f'{BASE_URL}/api/documents/?customer={customer_id}'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(f"\n✅ 获取文档成功")
            print(f"响应类型: {type(response.text)}")
            print(f"响应内容前 200 字符: {response.text[:200]}")

            result = response.json()
            print(f"JSON 解析后类型: {type(result)}")

            if isinstance(result, list):
                print(f"文档数量: {len(result)}")

                # 打印每个文档的详细信息
                for i, doc in enumerate(result, 1):
                    print(f"\n文档 {i}:")
                    print(f"  ID: {doc.get('id')}")
                    print(f"  文件名: {doc.get('file_name')}")
                    print(f"  文件类型: {doc.get('file_type')}")
                    print(f"  文件大小: {doc.get('file_size')}")
                    print(f"  文件 URL: {doc.get('file_url')}")
                    print(f"  资料类型: {doc.get('document_type_name')}")
            else:
                print(f"结果不是列表: {result}")

            return result
        else:
            print(f"❌ 获取文档失败: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ 获取文档错误: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """主函数"""
    print("=" * 70)
    print("测试文档 API")
    print("=" * 70)
    
    # 登录
    token = login()
    if not token:
        return
    
    # 获取文档
    documents = get_documents(token)
    
    if documents:
        print("\n" + "=" * 70)
        print("测试结果")
        print("=" * 70)

        # 处理分页数据
        if isinstance(documents, dict) and 'results' in documents:
            results = documents['results']
        else:
            results = documents

        if len(results) > 0:
            # 检查第一个文档的 file_type 字段
            first_doc = results[0]
            file_type = first_doc.get('file_type')

            print(f"\n第一个文档的 file_type: '{file_type}'")
            print(f"file_type 类型: {type(file_type)}")

            # 检查是否是预期的格式
            expected_types = ['image', 'video', 'pdf', 'document', 'spreadsheet']
            if file_type in expected_types:
                print(f"✅ file_type 格式正确: {file_type}")
            else:
                print(f"❌ file_type 格式不正确: {file_type}")
                print(f"   预期格式: {expected_types}")

            # 检查所有文档的 file_type
            print(f"\n所有文档的 file_type:")
            for i, doc in enumerate(results[:5], 1):  # 只显示前 5 个
                print(f"  {i}. {doc.get('file_name')}: {doc.get('file_type')}")

if __name__ == '__main__':
    main()

