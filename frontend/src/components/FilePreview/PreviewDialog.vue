<template>
  <el-dialog
    v-model="visible"
    :title="title"
    width="80%"
    @close="handleClose"
  >
    <!-- 图片预览 -->
    <div v-if="isImageFile" class="preview-container">
      <img :src="fileUrl" style="max-width: 100%; max-height: 600px" />
    </div>

    <!-- 视频预览 -->
    <div v-else-if="isVideoFile" class="preview-container">
      <video
        ref="videoPlayer"
        :src="fileUrl"
        controls
        style="max-width: 100%; max-height: 600px"
      />
    </div>

    <!-- PDF预览 -->
    <div v-else-if="isPdfFile" class="preview-container pdf-preview">
      <div class="pdf-toolbar">
        <el-button :disabled="currentPage <= 1" @click="prevPage">上一页</el-button>
        <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
        <el-button :disabled="currentPage >= totalPages" @click="nextPage">下一页</el-button>
        <el-button type="primary" @click="handleDownload">下载</el-button>
      </div>
      <div class="pdf-canvas-container">
        <canvas ref="pdfCanvas" style="max-width: 100%; border: 1px solid #ddd;"></canvas>
      </div>
    </div>

    <!-- 不支持预览的文件 -->
    <div v-else class="preview-container no-preview">
      <el-empty description="不支持预览此文件类型" />
      <el-button type="primary" @click="handleDownload" style="margin-top: 20px">
        下载文件
      </el-button>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { isImage, isVideo, isPdf } from '@/utils/fileType'
import * as pdfjsLib from 'pdfjs-dist'

// 设置 PDF.js worker - 使用本地文件
pdfjsLib.GlobalWorkerOptions.workerSrc = '/pdf.worker.min.mjs'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  fileUrl: {
    type: String,
    required: true
  },
  fileName: {
    type: String,
    default: '文件'
  },
  fileType: {
    type: String,
    default: 'image'
  }
})

const emit = defineEmits(['update:modelValue'])

const videoPlayer = ref(null)
const pdfCanvas = ref(null)
const currentPage = ref(1)
const totalPages = ref(0)
let pdfDoc = null

const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const title = computed(() => `预览 - ${props.fileName}`)

const isImageFile = computed(() => isImage(props.fileType))
const isVideoFile = computed(() => isVideo(props.fileType))
const isPdfFile = computed(() => isPdf(props.fileType))

const handleClose = () => {
  // 停止视频播放
  if (videoPlayer.value) {
    videoPlayer.value.pause()
    videoPlayer.value.currentTime = 0
  }
  visible.value = false
}

const handleDownload = () => {
  const link = document.createElement('a')
  link.href = props.fileUrl
  link.download = props.fileName
  link.click()
}

// PDF 渲染函数
const renderPdfPage = async (pageNum) => {
  if (!pdfDoc) return

  try {
    const page = await pdfDoc.getPage(pageNum)
    const canvas = pdfCanvas.value
    const context = canvas.getContext('2d')
    const viewport = page.getViewport({ scale: 1.5 })

    canvas.width = viewport.width
    canvas.height = viewport.height

    await page.render({
      canvasContext: context,
      viewport: viewport
    }).promise
  } catch (error) {
    console.error('PDF 渲染失败:', error)
  }
}

// 加载 PDF
const loadPdf = async () => {
  if (!isPdfFile.value) return

  try {
    pdfDoc = await pdfjsLib.getDocument(props.fileUrl).promise
    totalPages.value = pdfDoc.numPages
    currentPage.value = 1
    await renderPdfPage(1)
  } catch (error) {
    console.error('PDF 加载失败:', error)
  }
}

// 上一页
const prevPage = async () => {
  if (currentPage.value > 1) {
    currentPage.value--
    await renderPdfPage(currentPage.value)
  }
}

// 下一页
const nextPage = async () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    await renderPdfPage(currentPage.value)
  }
}

// 监听对话框打开
watch(() => visible.value, (newVal) => {
  if (newVal && isPdfFile.value) {
    loadPdf()
  }
})

onMounted(() => {
  if (visible.value && isPdfFile.value) {
    loadPdf()
  }
})
</script>

<style scoped>
.preview-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  background: #f5f7fa;
  border-radius: 4px;
}

.preview-container.no-preview {
  flex-direction: column;
}

.preview-container.pdf-preview {
  flex-direction: column;
  align-items: stretch;
  justify-content: flex-start;
  min-height: 600px;
}

.pdf-toolbar {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background: #f5f7fa;
  border-bottom: 1px solid #ddd;
  margin-bottom: 10px;
}

.page-info {
  margin: 0 10px;
  font-size: 14px;
  color: #606266;
}

.pdf-canvas-container {
  flex: 1;
  overflow: auto;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 10px;
}
</style>

