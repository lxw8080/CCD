# 📋 实施方案 - PDF 预览和移动端预览功能扩展

**制定日期**: 2025-10-18  
**项目**: 客户资料收集系统  
**版本**: 1.0

---

## 🔍 诊断结果

### 问题 1: PC 端 PDF 预览失败

**根本原因**: Django 的 `X-Frame-Options` 安全策略阻止了 iframe 加载

**错误信息**:
```
[ERROR] Refused to display 'http://127.0.0.1:8000/' in a frame because it set 'X-Frame-Options' to '...'
```

**当前实现**: 使用 iframe 加载 PDF
```vue
<iframe :src="`${fileUrl}#toolbar=1&navpanes=0&scrollbar=1`" 
        style="width: 100%; height: 600px; border: none" />
```

**解决方案**: 使用 PDF.js 库进行客户端 PDF 渲染

---

### 问题 2: 移动端预览功能不完整

**当前状态**:
- ✅ 图片预览已实现（使用 van-image-preview）
- ❌ 视频预览未实现
- ❌ PDF 预览未实现
- ❌ 其他文件下载未实现

**handlePreview 函数**:
```javascript
const handlePreview = (doc) => {
  previewImages.value = [doc.file_url]
  previewIndex.value = 0
  previewVisible.value = true
}
```

**问题**: 只处理图片，其他文件类型会导致错误

---

## 📐 实施方案

### 方案 1: PC 端 PDF 预览修复

#### 1.1 安装 PDF.js 库

```bash
npm install pdfjs-dist
```

#### 1.2 修改 PreviewDialog.vue 组件

**修改内容**:
- 导入 PDF.js 库
- 添加 PDF 渲染逻辑
- 添加 PDF 页码控制
- 移除 iframe 方式

**新的 PDF 预览实现**:
```vue
<div v-else-if="isPdfFile" class="pdf-preview-container">
  <div class="pdf-toolbar">
    <button @click="prevPage" :disabled="currentPage <= 1">上一页</button>
    <span>{{ currentPage }} / {{ totalPages }}</span>
    <button @click="nextPage" :disabled="currentPage >= totalPages">下一页</button>
  </div>
  <canvas ref="pdfCanvas" style="width: 100%; border: 1px solid #ddd;"></canvas>
</div>
```

#### 1.3 添加 PDF 渲染脚本

```javascript
import * as pdfjsLib from 'pdfjs-dist'

pdfjsLib.GlobalWorkerOptions.workerSrc = 
  `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.min.js`

const renderPdf = async (url, pageNum) => {
  const pdf = await pdfjsLib.getDocument(url).promise
  const page = await pdf.getPage(pageNum)
  const canvas = pdfCanvas.value
  const context = canvas.getContext('2d')
  const viewport = page.getViewport({ scale: 1.5 })
  
  canvas.width = viewport.width
  canvas.height = viewport.height
  
  await page.render({
    canvasContext: context,
    viewport: viewport
  }).promise
  
  totalPages.value = pdf.numPages
}
```

---

### 方案 2: 移动端预览功能实现

#### 2.1 创建移动端预览组件

**文件**: `frontend/src/components/FilePreview/MobilePreviewDialog.vue`

**功能**:
- 图片预览（使用 van-image-preview）
- 视频预览（使用 video 标签）
- PDF 预览（使用 PDF.js）
- 文件下载

#### 2.2 修改 handlePreview 函数

```javascript
const handlePreview = (doc) => {
  if (isImage(doc.file_type)) {
    previewImages.value = [doc.file_url]
    previewIndex.value = 0
    previewVisible.value = true
  } else if (isVideo(doc.file_type)) {
    showVideoPreview(doc)
  } else if (isPdf(doc.file_type)) {
    showPdfPreview(doc)
  } else {
    downloadFile(doc)
  }
}
```

#### 2.3 添加视频预览

```vue
<van-popup v-model:show="videoPreviewVisible" position="center">
  <div style="width: 100%; max-width: 100vw;">
    <video 
      :src="videoUrl" 
      controls 
      style="width: 100%; height: auto;"
    />
  </div>
</van-popup>
```

#### 2.4 添加 PDF 预览

```vue
<van-popup v-model:show="pdfPreviewVisible" position="center">
  <div style="width: 100%; height: 80vh; overflow: auto;">
    <canvas ref="mobilePdfCanvas" style="width: 100%;"></canvas>
  </div>
</van-popup>
```

---

### 方案 3: 资料类型管理功能扩展

#### 3.1 后端 DocumentType 模型修改

**添加字段**:
```python
class DocumentType(models.Model):
    # 现有字段...
    
    # 新增：支持的文件格式
    allowed_file_types = models.JSONField(
        default=list,
        help_text='支持的文件类型: image, video, file'
    )
    
    # 新增：最大文件数量
    max_file_count = models.IntegerField(
        default=0,
        help_text='最大文件数量，0 表示不限制'
    )
```

#### 3.2 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 3.3 管理后台配置

```python
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_required', 'allowed_file_types', 'max_file_count']
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'is_required')
        }),
        ('文件限制', {
            'fields': ('allowed_file_types', 'max_file_count')
        }),
    )
```

#### 3.4 序列化器更新

```python
class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'id', 'name', 'is_required', 
            'allowed_file_types', 'max_file_count'
        ]
```

---

### 方案 4: 前端文件格式和数量限制

#### 4.1 PC 端实现

**修改 CustomerDetail.vue**:
- 根据选择的资料类型动态调整 accept 属性
- 检查已上传文件数量
- 达到限制时禁用上传按钮

#### 4.2 移动端实现

**修改 mobile/CustomerDetail.vue**:
- 同样的文件格式限制
- 同样的文件数量限制

---

## 📊 实施步骤

| 步骤 | 任务 | 优先级 | 预计时间 |
|------|------|--------|---------|
| 1 | 安装 PDF.js 库 | 高 | 5 分钟 |
| 2 | 修复 PC 端 PDF 预览 | 高 | 30 分钟 |
| 3 | 实现移动端预览功能 | 高 | 45 分钟 |
| 4 | 扩展 DocumentType 模型 | 中 | 20 分钟 |
| 5 | 实现文件格式限制 | 中 | 30 分钟 |
| 6 | 实现文件数量限制 | 中 | 30 分钟 |
| 7 | 测试所有功能 | 高 | 45 分钟 |
| 8 | 生成报告 | 低 | 15 分钟 |

**总计**: 约 3.5 小时

---

## 🎯 成功标准

- ✅ PC 端 PDF 预览正常工作
- ✅ 移动端支持图片、视频、PDF 预览
- ✅ 移动端支持文件下载
- ✅ 资料类型支持文件格式限制
- ✅ 资料类型支持文件数量限制
- ✅ 前端正确验证和显示限制
- ✅ 所有功能测试通过

---

## 📝 风险评估

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| PDF.js 库加载失败 | 高 | 使用 CDN 备用方案 |
| 移动端性能问题 | 中 | 优化渲染，添加加载指示器 |
| 浏览器兼容性 | 低 | 测试主流浏览器 |

---

**方案制定完成** ✅

