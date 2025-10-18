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
        :src="fileUrl"
        controls
        style="max-width: 100%; max-height: 600px"
      />
    </div>

    <!-- PDF预览 -->
    <div v-else-if="isPdfFile" class="preview-container">
      <iframe
        :src="`${fileUrl}#toolbar=1&navpanes=0&scrollbar=1`"
        style="width: 100%; height: 600px; border: none"
      />
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
import { ref, computed } from 'vue'
import { isImage, isVideo, isPdf } from '@/utils/fileType'

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

const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const title = computed(() => `预览 - ${props.fileName}`)

const isImageFile = computed(() => isImage(props.fileType))
const isVideoFile = computed(() => isVideo(props.fileType))
const isPdfFile = computed(() => isPdf(props.fileType))

const handleClose = () => {
  visible.value = false
}

const handleDownload = () => {
  const link = document.createElement('a')
  link.href = props.fileUrl
  link.download = props.fileName
  link.click()
}
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
</style>

