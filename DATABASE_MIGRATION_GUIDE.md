# 动态自定义字段功能 - 外部数据库迁移指南

## 📋 数据库变更概述

### 1. 新增的数据库表

本次功能实现在数据库中新增了 **2个表**：

#### 表1: `custom_fields` (自定义字段定义表)
存储自定义字段的配置信息

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | BIGINT | 主键 | PRIMARY KEY, AUTO_INCREMENT |
| name | VARCHAR(100) | 字段名称 | NOT NULL |
| field_type | VARCHAR(20) | 字段类型 | NOT NULL, DEFAULT 'text' |
| is_required | BOOLEAN | 是否必填 | NOT NULL, DEFAULT FALSE |
| sort_order | INTEGER | 排序 | NOT NULL, DEFAULT 0 |
| placeholder | VARCHAR(255) | 占位符 | NULL |
| help_text | VARCHAR(255) | 帮助文本 | NULL |
| default_value | VARCHAR(255) | 默认值 | NULL |
| options | JSON/JSONB | 选项列表 | NOT NULL, DEFAULT '[]' |
| min_length | INTEGER | 最小长度 | NULL |
| max_length | INTEGER | 最大长度 | NULL |
| min_value | DECIMAL(20,2) | 最小值 | NULL |
| max_value | DECIMAL(20,2) | 最大值 | NULL |
| regex_pattern | VARCHAR(255) | 正则表达式 | NULL |
| is_active | BOOLEAN | 是否启用 | NOT NULL, DEFAULT TRUE |
| created_at | TIMESTAMP | 创建时间 | NOT NULL, AUTO_NOW_ADD |
| updated_at | TIMESTAMP | 更新时间 | NOT NULL, AUTO_NOW |

**索引**:
- PRIMARY KEY: id
- INDEX: sort_order, id (用于排序查询)

#### 表2: `custom_field_values` (自定义字段值表)
存储客户的自定义字段值

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | BIGINT | 主键 | PRIMARY KEY, AUTO_INCREMENT |
| customer_id | BIGINT | 客户ID | NOT NULL, FOREIGN KEY |
| custom_field_id | BIGINT | 自定义字段ID | NOT NULL, FOREIGN KEY |
| value | TEXT | 字段值 | NULL |
| created_at | TIMESTAMP | 创建时间 | NOT NULL, AUTO_NOW_ADD |
| updated_at | TIMESTAMP | 更新时间 | NOT NULL, AUTO_NOW |

**约束**:
- PRIMARY KEY: id
- FOREIGN KEY: customer_id → customers_customer(id) ON DELETE CASCADE
- FOREIGN KEY: custom_field_id → custom_fields(id) ON DELETE CASCADE
- UNIQUE CONSTRAINT: (customer_id, custom_field_id) - 确保每个客户每个字段只有一个值
- INDEX: custom_field__sort_order, id (用于排序查询)

### 2. 对现有表的修改

**无修改** - 本次迁移不修改任何现有表结构，不会影响现有数据。

> ⚠️ **注意**: 迁移文件中有一个 `migrations.RemoveField` 操作（删除 remarks 字段），但这个操作在实际执行时已被我们移除，因为该字段在数据库中不存在。

## 🔍 迁移文件分析

### 迁移文件: `0003_customfield_remove_customer_remarks_customfieldvalue.py`

**位置**: `backend/apps/customers/migrations/0003_customfield_remove_customer_remarks_customfieldvalue.py`

**依赖**: 
- `customers.0002_initial`

**操作内容**:
1. ✅ 创建 `CustomField` 模型（custom_fields 表）
2. ✅ 创建 `CustomFieldValue` 模型（custom_field_values 表）
3. ❌ ~~删除 Customer.remarks 字段~~ (已移除，不会执行)

**迁移状态**: 
- 本地 SQLite: ✅ 已应用
- 外部 PostgreSQL: ❌ 未应用

## 🚀 外部数据库迁移步骤

### 前置准备

#### 1. 确认外部数据库连接信息

您的外部数据库配置（来自 `.env` 文件）：
```
数据库类型: PostgreSQL
数据库名: ccd_dev
用户名: flask_user
密码: flask_password
主机: 115.190.29.10
端口: 5433
```

#### 2. 备份外部数据库（强烈建议）

在执行迁移前，请先备份外部数据库：

```bash
# 使用 pg_dump 备份数据库
pg_dump -h 115.190.29.10 -p 5433 -U flask_user -d ccd_dev -F c -f ccd_dev_backup_$(date +%Y%m%d_%H%M%S).dump

# 或者只备份 schema
pg_dump -h 115.190.29.10 -p 5433 -U flask_user -d ccd_dev --schema-only -f ccd_dev_schema_backup_$(date +%Y%m%d_%H%M%S).sql
```

如果您没有 `pg_dump` 工具，可以通过数据库管理工具（如 pgAdmin、DBeaver）进行备份。

### 迁移执行步骤

#### 步骤1: 检查当前迁移状态

首先，检查外部数据库当前的迁移状态：

```bash
cd C:\Users\16094\Desktop\fsdownload\CCD\backend
python manage.py showmigrations customers
```

**预期输出**:
```
customers
 [X] 0001_initial
 [X] 0002_initial
 [ ] 0003_customfield_remove_customer_remarks_customfieldvalue
```

如果 `0003` 显示为 `[ ]`（未应用），继续下一步。

#### 步骤2: 生成 SQL 预览（可选但推荐）

在实际执行迁移前，先查看将要执行的 SQL 语句：

```bash
python manage.py sqlmigrate customers 0003
```

这会显示迁移将执行的 SQL 语句，您可以检查是否符合预期。

**预期 SQL 内容**（PostgreSQL）:
```sql
-- 创建 custom_fields 表
CREATE TABLE "custom_fields" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "field_type" varchar(20) NOT NULL,
    "is_required" boolean NOT NULL,
    "sort_order" integer NOT NULL,
    "placeholder" varchar(255) NULL,
    "help_text" varchar(255) NULL,
    "default_value" varchar(255) NULL,
    "options" jsonb NOT NULL,
    "min_length" integer NULL,
    "max_length" integer NULL,
    "min_value" numeric(20, 2) NULL,
    "max_value" numeric(20, 2) NULL,
    "regex_pattern" varchar(255) NULL,
    "is_active" boolean NOT NULL,
    "created_at" timestamp with time zone NOT NULL,
    "updated_at" timestamp with time zone NOT NULL
);

-- 创建 custom_field_values 表
CREATE TABLE "custom_field_values" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "value" text NULL,
    "created_at" timestamp with time zone NOT NULL,
    "updated_at" timestamp with time zone NOT NULL,
    "custom_field_id" bigint NOT NULL,
    "customer_id" bigint NOT NULL
);

-- 添加外键约束
ALTER TABLE "custom_field_values" 
    ADD CONSTRAINT "custom_field_values_custom_field_id_fkey" 
    FOREIGN KEY ("custom_field_id") 
    REFERENCES "custom_fields" ("id") 
    DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "custom_field_values" 
    ADD CONSTRAINT "custom_field_values_customer_id_fkey" 
    FOREIGN KEY ("customer_id") 
    REFERENCES "customers_customer" ("id") 
    DEFERRABLE INITIALLY DEFERRED;

-- 添加唯一约束
ALTER TABLE "custom_field_values" 
    ADD CONSTRAINT "custom_field_values_customer_id_custom_field_id_uniq" 
    UNIQUE ("customer_id", "custom_field_id");

-- 创建索引
CREATE INDEX "custom_fields_sort_order_id_idx" 
    ON "custom_fields" ("sort_order", "id");

CREATE INDEX "custom_field_values_custom_field_id_idx" 
    ON "custom_field_values" ("custom_field_id");

CREATE INDEX "custom_field_values_customer_id_idx" 
    ON "custom_field_values" ("customer_id");
```

#### 步骤3: 执行迁移

确认无误后，执行迁移：

```bash
python manage.py migrate customers 0003
```

**预期输出**:
```
Operations to perform:
  Target specific migration: 0003_customfield_remove_customer_remarks_customfieldvalue, from customers
Running migrations:
  Applying customers.0003_customfield_remove_customer_remarks_customfieldvalue... OK
```

#### 步骤4: 验证迁移结果

迁移完成后，验证表是否创建成功：

```bash
# 再次检查迁移状态
python manage.py showmigrations customers
```

**预期输出**:
```
customers
 [X] 0001_initial
 [X] 0002_initial
 [X] 0003_customfield_remove_customer_remarks_customfieldvalue
```

#### 步骤5: 验证数据库表结构

使用 Django shell 或数据库客户端验证表是否正确创建：

```bash
# 使用 Django shell
python manage.py shell
```

在 shell 中执行：
```python
from apps.customers.models import CustomField, CustomFieldValue
from django.db import connection

# 检查表是否存在
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name IN ('custom_fields', 'custom_field_values')
    """)
    tables = cursor.fetchall()
    print("找到的表:", tables)

# 检查模型是否可用
print("CustomField 模型:", CustomField._meta.db_table)
print("CustomFieldValue 模型:", CustomFieldValue._meta.db_table)

# 尝试查询（应该返回空结果）
print("CustomField 数量:", CustomField.objects.count())
print("CustomFieldValue 数量:", CustomFieldValue.objects.count())
```

**预期输出**:
```
找到的表: [('custom_fields',), ('custom_field_values',)]
CustomField 模型: custom_fields
CustomFieldValue 模型: custom_field_values
CustomField 数量: 0
CustomFieldValue 数量: 0
```

## ⚠️ 风险评估和注意事项

### 低风险操作 ✅

1. **只创建新表**: 本次迁移只创建新表，不修改现有表
2. **无数据迁移**: 不涉及数据的移动或转换
3. **外键约束安全**: 外键指向现有的 `customers_customer` 表，不会影响现有数据
4. **可回滚**: 如果出现问题，可以轻松回滚

### 需要注意的事项 ⚠️

1. **数据库权限**: 确保 `flask_user` 有创建表和索引的权限
2. **表名冲突**: 确保数据库中不存在同名表 `custom_fields` 和 `custom_field_values`
3. **JSON 字段**: PostgreSQL 使用 `JSONB` 类型，确保数据库版本支持（PostgreSQL 9.4+）
4. **外键约束**: 迁移会创建指向 `customers_customer` 表的外键，确保该表存在

### 回滚方案

如果迁移后发现问题，可以回滚到之前的状态：

```bash
# 回滚到 0002 版本
python manage.py migrate customers 0002
```

这会删除新创建的两个表。

或者手动删除表（如果自动回滚失败）：

```sql
-- 手动删除表（按顺序）
DROP TABLE IF EXISTS custom_field_values CASCADE;
DROP TABLE IF EXISTS custom_fields CASCADE;

-- 更新迁移记录
DELETE FROM django_migrations 
WHERE app = 'customers' 
AND name = '0003_customfield_remove_customer_remarks_customfieldvalue';
```

## 📝 迁移后的操作

### 1. 创建测试数据（可选）

迁移完成后，您可以在外部数据库中创建测试自定义字段：

```bash
# 在外部数据库环境下运行测试脚本
python test_custom_fields.py
```

或者通过 Django Admin 手动创建：
1. 访问 Django Admin
2. 导航到 Customers > Custom fields
3. 点击 "Add Custom field" 创建字段

### 2. 验证功能

1. 访问前端应用
2. 进入客户管理 > 新建客户
3. 确认自定义字段正确显示
4. 测试创建和编辑客户

## 🔧 故障排查

### 问题1: 权限不足

**错误信息**:
```
django.db.utils.ProgrammingError: permission denied for schema public
```

**解决方案**:
```sql
-- 授予用户创建表的权限
GRANT CREATE ON SCHEMA public TO flask_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO flask_user;
```

### 问题2: 表已存在

**错误信息**:
```
django.db.utils.ProgrammingError: relation "custom_fields" already exists
```

**解决方案**:
```bash
# 标记迁移为已应用（如果表确实已存在且结构正确）
python manage.py migrate customers 0003 --fake
```

### 问题3: 外键约束失败

**错误信息**:
```
django.db.utils.IntegrityError: foreign key constraint fails
```

**解决方案**:
确保 `customers_customer` 表存在：
```sql
SELECT * FROM information_schema.tables 
WHERE table_name = 'customers_customer';
```

## 📊 迁移检查清单

执行迁移前，请确认以下事项：

- [ ] 已备份外部数据库
- [ ] 确认数据库连接配置正确（.env 文件）
- [ ] 确认数据库用户有足够权限
- [ ] 已查看 SQL 预览，确认操作内容
- [ ] 已在测试环境验证（如果有）
- [ ] 已通知相关人员（如果是生产环境）

执行迁移后，请验证：

- [ ] 迁移状态显示为已应用 [X]
- [ ] 两个新表已创建（custom_fields, custom_field_values）
- [ ] 可以通过 Django ORM 访问新表
- [ ] 前端可以正常获取自定义字段列表
- [ ] 可以创建和编辑包含自定义字段的客户

## 📞 需要帮助？

如果在迁移过程中遇到任何问题，请：

1. 保存完整的错误信息
2. 检查数据库日志
3. 查看 Django 日志
4. 如果需要，可以回滚迁移并重新尝试

---

**文档版本**: 1.0  
**创建日期**: 2025-10-21  
**适用数据库**: PostgreSQL 9.4+  
**Django 版本**: 4.2.7

