<template>
  <!-- 图片预览 -->
  <van-image-preview
    v-model:show="imagePreviewVisible"
    :images="previewImages"
    :start-position="previewIndex"
    @close="handleChildClose"
  />

  <!-- 视频预览 -->
  <van-popup
    v-model:show="videoPreviewVisible"
    position="center"
    :style="{ width: '100%', height: '100%' }"
    @closed="handleChildClose"
  >
    <div class="video-preview-container">
      <div class="video-header">
        <van-button type="primary" size="small" @click="closeVideoPreview">关闭</van-button>
      </div>
      <video
        :src="videoUrl"
        controls
        playsinline
        webkit-playsinline
        x5-playsinline
        preload="metadata"
        ref="videoElement"
        style="width: 100%; height: auto; max-height: 80vh; background: #000;"
      />
    </div>
  </van-popup>

  <!-- PDF 预览 -->
  <van-popup
    v-model:show="pdfPreviewVisible"
    position="center"
    :style="{ width: '100%', height: '100%' }"
    @closed="handleChildClose"
  >
    <div class="pdf-preview-container">
      <div class="pdf-header">
        <van-button type="primary" size="small" @click="closePdfPreview">关闭</van-button>
        <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
        <van-button type="primary" size="small" @click="downloadFile">下载</van-button>
      </div>
      <div class="pdf-canvas-wrapper">
        <canvas ref="mobilePdfCanvas" style="width: 100%;"></canvas>
      </div>
      <div class="pdf-footer">
        <van-button
          type="primary"
          size="small"
          :disabled="currentPage <= 1"
          @click="prevPage"
        >
          上一页
        </van-button>
        <van-button
          type="primary"
          size="small"
          :disabled="currentPage >= totalPages"
          @click="nextPage"
        >
          下一页
        </van-button>
      </div>
    </div>
  </van-popup>

  <!-- 文件下载提示 -->
  <van-popup
    v-model:show="downloadPromptVisible"
    position="center"
    @closed="handleChildClose"
  >
    <div class="download-prompt">
      <p>此文件类型不支持预览，请下载查看</p>
      <van-button type="primary" block @click="downloadFile">下载文件</van-button>
      <van-button block @click="closeDownloadPrompt">取消</van-button>
    </div>
  </van-popup>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { isImage, isVideo, isPdf } from '@/utils/fileType'
import { showToast } from 'vant'
import * as pdfjsLib from 'pdfjs-dist'

// 设置 PDF.js worker - 使用本地文件
const baseUrl = (import.meta && import.meta.env && import.meta.env.BASE_URL) ? import.meta.env.BASE_URL : '/'
pdfjsLib.GlobalWorkerOptions.workerSrc = `${baseUrl}pdf.worker.min.mjs`

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

// 图片预览
const imagePreviewVisible = ref(false)
const previewImages = ref([])
const previewIndex = ref(0)

// 视频预览
const videoPreviewVisible = ref(false)
const videoUrl = ref('')
const videoElement = ref(null)

const stopVideoPlayback = () => {
  try {
    const el = videoElement.value
    if (el) {
      el.pause()
      el.currentTime = 0
      el.removeAttribute('src')
      el.load()
    }
  } catch (error) {
    console.warn('stopVideoPlayback failed:', error)
  } finally {
    videoUrl.value = ''
  }
}

// PDF 预览
const pdfPreviewVisible = ref(false)
const mobilePdfCanvas = ref(null)
const currentPage = ref(1)
const totalPages = ref(0)
let pdfDoc = null

// 文件下载
const downloadPromptVisible = ref(false)

const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

// 显示预览
const showPreview = () => {
  console.log('显示预览:', {
    fileUrl: props.fileUrl,
    fileName: props.fileName,
    fileType: props.fileType
  })

  if (isImage(props.fileType)) {
    console.log('显示图片预览')
    previewImages.value = [props.fileUrl]
    previewIndex.value = 0
    imagePreviewVisible.value = true
  } else if (isVideo(props.fileType)) {
    console.log('显示视频预览')
    videoUrl.value = props.fileUrl
    videoPreviewVisible.value = true
  } else if (isPdf(props.fileType)) {
    console.log('显示 PDF 预览')
    loadPdf()
  } else {
    console.log('不支持预览，显示下载提示，文件类型:', props.fileType)
    downloadPromptVisible.value = true
  }
}

const handleChildClose = () => {
  if (visible.value) {
    visible.value = false
  }
}

const closeVideoPreview = () => {
  stopVideoPlayback()
  videoPreviewVisible.value = false
  handleChildClose()
}

const closePdfPreview = () => {
  pdfPreviewVisible.value = false
  handleChildClose()
}

// 加载 PDF
const loadPdf = async () => {
  try {
    console.log('加载 PDF:', props.fileUrl)
    pdfDoc = await pdfjsLib.getDocument(props.fileUrl).promise
    totalPages.value = pdfDoc.numPages
    currentPage.value = 1
    pdfPreviewVisible.value = true
    await renderPdfPage(1)
    console.log('PDF 加载成功，共', totalPages.value, '页')
  } catch (error) {
    console.error('PDF 加载失败:', error)
    showToast('PDF 加载失败: ' + error.message)
    downloadPromptVisible.value = true
  }
}

// 渲染 PDF 页面
const renderPdfPage = async (pageNum) => {
  if (!pdfDoc) return

  try {
    console.log('渲染 PDF 第', pageNum, '页')
    const page = await pdfDoc.getPage(pageNum)
    const canvas = mobilePdfCanvas.value

    if (!canvas) {
      console.error('Canvas 元素不存在')
      return
    }

    const context = canvas.getContext('2d')
    const viewport = page.getViewport({ scale: 1.5 })

    canvas.width = viewport.width
    canvas.height = viewport.height

    await page.render({
      canvasContext: context,
      viewport: viewport
    }).promise

    console.log('PDF 第', pageNum, '页渲染成功')
  } catch (error) {
    console.error('PDF 渲染失败:', error)
    showToast('PDF 渲染失败: ' + error.message)
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

// 下载文件
const downloadFile = () => {
  const link = document.createElement('a')
  link.href = props.fileUrl
  link.download = props.fileName
  link.click()
  downloadPromptVisible.value = false
  handleChildClose()
}

const closeDownloadPrompt = () => {
  downloadPromptVisible.value = false
  handleChildClose()
}

// 监听对话框打开
watch(() => visible.value, (newVal) => {
  if (newVal) {
    showPreview()
  } else {
    imagePreviewVisible.value = false
    videoPreviewVisible.value = false
    pdfPreviewVisible.value = false
    downloadPromptVisible.value = false
  }
})

watch(imagePreviewVisible, (val) => {
  if (!val && visible.value) {
    handleChildClose()
  }
})

watch(videoPreviewVisible, (val) => {
  if (!val) {
    stopVideoPlayback()
    if (visible.value) {
      handleChildClose()
    }
  }
})

watch(pdfPreviewVisible, (val) => {
  if (!val && visible.value) {
    handleChildClose()
  }
})

watch(downloadPromptVisible, (val) => {
  if (!val && visible.value) {
    handleChildClose()
  }
})
</script>

<style scoped>
.video-preview-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #000;
}

.video-header {
  padding: 10px;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: flex-end;
}

.pdf-preview-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
}

.pdf-header {
  padding: 10px;
  background: #fff;
  border-bottom: 1px solid #ddd;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
}

.page-info {
  font-size: 14px;
  color: #606266;
}

.pdf-canvas-wrapper {
  flex: 1;
  overflow: auto;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 10px;
}

.pdf-footer {
  padding: 10px;
  background: #fff;
  border-top: 1px solid #ddd;
  display: flex;
  gap: 10px;
  justify-content: center;
}

.download-prompt {
  padding: 20px;
  text-align: center;
  min-width: 250px;
}

.download-prompt p {
  margin-bottom: 20px;
  color: #606266;
}
</style>

