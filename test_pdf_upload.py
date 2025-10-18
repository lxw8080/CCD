#!/usr/bin/env python
"""
测试 PDF 上传和预览功能
"""
import os
import sys
import django
import requests
import json

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
django.setup()

from django.contrib.auth import get_user_model
from apps.customers.models import Customer
from apps.documents.models import DocumentType, Document

User = get_user_model()

def test_pdf_upload():
    """测试 PDF 上传"""
    print("=" * 60)
    print("测试 PDF 上传和预览功能")
    print("=" * 60)
    
    # 1. 获取测试数据
    print("\n1. 获取测试数据...")
    user = User.objects.first()
    customer = Customer.objects.first()
    doc_type = DocumentType.objects.first()
    
    if not user:
        print("[ERROR] 没有找到用户")
        return
    if not customer:
        print("[ERROR] 没有找到客户")
        return
    if not doc_type:
        print("[ERROR] 没有找到资料类型")
        return

    print("[OK] 用户: {}".format(user.username))
    print("[OK] 客户: {}".format(customer.name))
    print("[OK] 资料类型: {}".format(doc_type.name))
    
    # 2. 检查 PDF 文件
    print("\n2. 检查 PDF 文件...")
    pdf_path = r"C:\Users\16094\Desktop\01.pdf"
    if not os.path.exists(pdf_path):
        print("[ERROR] PDF 文件不存在: {}".format(pdf_path))
        return

    file_size = os.path.getsize(pdf_path)
    print("[OK] PDF 文件存在: {}".format(pdf_path))
    print("   文件大小: {:.2f} MB".format(file_size / 1024 / 1024))
    
    # 3. 上传 PDF 文件
    print("\n3. 上传 PDF 文件...")
    try:
        with open(pdf_path, 'rb') as f:
            files = {'file': f}
            data = {
                'customer': customer.id,
                'document_type': doc_type.id
            }
            
            # 获取 token
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            headers = {
                'Authorization': f'Bearer {access_token}'
            }
            
            response = requests.post(
                'http://127.0.0.1:8000/api/documents/upload/',
                files=files,
                data=data,
                headers=headers
            )
            
            if response.status_code == 201:
                result = response.json()
                print("[OK] PDF 上传成功")
                print("   文档 ID: {}".format(result.get('id')))
                print("   文件名: {}".format(result.get('file_name')))
                print("   文件类型: {}".format(result.get('file_type')))
                print("   文件 URL: {}".format(result.get('file_url')))
                print("\n   完整响应:")
                print(json.dumps(result, indent=2, ensure_ascii=False))

                # 4. 测试预览 URL
                print("\n4. 测试预览 URL...")
                file_url = result.get('file_url')
                if file_url:
                    # 检查 URL 是否已经是完整的
                    if file_url.startswith('http'):
                        preview_url = file_url
                    else:
                        preview_url = 'http://127.0.0.1:8000{}'.format(file_url)

                    print("   预览 URL: {}".format(preview_url))
                    preview_response = requests.get(preview_url, headers=headers)
                    if preview_response.status_code == 200:
                        print("[OK] 预览 URL 可访问")
                        print("   Content-Type: {}".format(preview_response.headers.get('Content-Type')))
                        print("   Content-Length: {}".format(preview_response.headers.get('Content-Length')))
                    else:
                        print("[ERROR] 预览 URL 不可访问: {}".format(preview_response.status_code))
            else:
                print("[ERROR] PDF 上传失败: {}".format(response.status_code))
                print("   错误信息: {}".format(response.text))
    except Exception as e:
        print("[ERROR] 上传过程出错: {}".format(e))
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == '__main__':
    test_pdf_upload()

