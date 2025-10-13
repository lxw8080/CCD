from django.core.management.base import BaseCommand
from apps.users.models import User
from apps.customers.models import Customer
from apps.documents.models import DocumentType


class Command(BaseCommand):
    help = '创建演示数据（仅用于开发测试）'
    
    def handle(self, *args, **options):
        self.stdout.write('开始创建演示数据...\n')
        
        # 1. 创建测试用户
        self.stdout.write('1. 创建测试用户...')
        
        users_data = [
            {
                'username': 'admin',
                'password': 'admin123',
                'email': 'admin@example.com',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True
            },
            {
                'username': 'staff1',
                'password': 'staff123',
                'email': 'staff1@example.com',
                'role': 'staff'
            },
            {
                'username': 'staff2',
                'password': 'staff123',
                'email': 'staff2@example.com',
                'role': 'staff'
            },
            {
                'username': 'auditor',
                'password': 'auditor123',
                'email': 'auditor@example.com',
                'role': 'auditor'
            }
        ]
        
        for user_data in users_data:
            password = user_data.pop('password')
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'  创建用户: {user.username} (密码: {password})')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'  用户已存在: {user.username}')
                )
        
        # 2. 创建测试客户
        self.stdout.write('\n2. 创建测试客户...')
        
        staff_user = User.objects.filter(role='staff').first()
        
        customers_data = [
            {
                'name': '张三',
                'id_card': '110101199001011234',
                'phone': '13800138001',
                'address': '北京市朝阳区XX街道XX号',
                'status': 'pending',
                'remarks': '测试客户1'
            },
            {
                'name': '李四',
                'id_card': '310101199002021234',
                'phone': '13800138002',
                'address': '上海市浦东新区XX街道XX号',
                'status': 'complete',
                'remarks': '测试客户2'
            },
            {
                'name': '王五',
                'id_card': '440101199003031234',
                'phone': '13800138003',
                'address': '广州市天河区XX街道XX号',
                'status': 'reviewing',
                'remarks': '测试客户3'
            },
            {
                'name': '赵六',
                'id_card': '330101199004041234',
                'phone': '13800138004',
                'address': '杭州市西湖区XX街道XX号',
                'status': 'approved',
                'remarks': '测试客户4'
            },
            {
                'name': '钱七',
                'id_card': '510101199005051234',
                'phone': '13800138005',
                'address': '成都市锦江区XX街道XX号',
                'status': 'pending',
                'remarks': '测试客户5'
            }
        ]
        
        for customer_data in customers_data:
            customer, created = Customer.objects.get_or_create(
                id_card=customer_data['id_card'],
                defaults={
                    **customer_data,
                    'created_by': staff_user
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'  创建客户: {customer.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'  客户已存在: {customer.name}')
                )
        
        # 3. 显示统计信息
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('演示数据创建完成！'))
        self.stdout.write('='*50)
        self.stdout.write(f'\n用户数量: {User.objects.count()}')
        self.stdout.write(f'客户数量: {Customer.objects.count()}')
        self.stdout.write(f'资料类型数量: {DocumentType.objects.count()}')
        
        self.stdout.write('\n测试账号:')
        self.stdout.write('  管理员: admin / admin123')
        self.stdout.write('  客服1: staff1 / staff123')
        self.stdout.write('  客服2: staff2 / staff123')
        self.stdout.write('  审核员: auditor / auditor123')
        
        self.stdout.write('\n提示: 请使用以上账号登录系统进行测试')

