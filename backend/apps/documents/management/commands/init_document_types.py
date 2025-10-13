from django.core.management.base import BaseCommand
from apps.documents.models import DocumentType


class Command(BaseCommand):
    help = '初始化资料类型数据'
    
    def handle(self, *args, **options):
        document_types = [
            {'name': '身份证正面', 'is_required': True, 'sort_order': 1, 'description': '身份证人像面'},
            {'name': '身份证反面', 'is_required': True, 'sort_order': 2, 'description': '身份证国徽面'},
            {'name': '收入证明', 'is_required': True, 'sort_order': 3, 'description': '单位出具的收入证明'},
            {'name': '银行流水', 'is_required': True, 'sort_order': 4, 'description': '近6个月银行流水'},
            {'name': '房产证明', 'is_required': False, 'sort_order': 5, 'description': '房产证或购房合同'},
            {'name': '征信报告', 'is_required': True, 'sort_order': 6, 'description': '人民银行征信报告'},
            {'name': '户口本', 'is_required': False, 'sort_order': 7, 'description': '户口本首页及本人页'},
            {'name': '结婚证', 'is_required': False, 'sort_order': 8, 'description': '已婚需提供'},
            {'name': '其他资料', 'is_required': False, 'sort_order': 99, 'description': '其他补充资料'},
        ]
        
        created_count = 0
        for doc_type_data in document_types:
            doc_type, created = DocumentType.objects.get_or_create(
                name=doc_type_data['name'],
                defaults=doc_type_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'创建资料类型: {doc_type.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'资料类型已存在: {doc_type.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n完成！共创建 {created_count} 个资料类型')
        )

