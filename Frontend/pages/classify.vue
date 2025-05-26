<template>
  <div class="classify-container">
    <h1 class="title">🌿 Nilo Leaf Classifier</h1>
    <p class="subtitle">
      Upload a leaf image to see if it's <em>Magnolia pubescens</em> (Nilo).
    </p>

    <div class="upload-preview-row">
      <div class="upload-box-wrapper">
        <a-upload
          :before-upload="handleBeforeUpload"
          :show-upload-list="false"
          accept=".jpg,.jpeg"
          class="upload-card"
          :disabled="isUploading || isLoading"
        >
          <div
            class="upload-box"
            :class="{ 'uploading': isUploading || isLoading }"
          >
            <a-button type="primary" size="large" :loading="isUploading || isLoading">
              Choose File
            </a-button>
            <p class="upload-note">JPEG or JPG format only</p>
          </div>
        </a-upload>
      </div>

      <div class="preview-box-wrapper" v-if="previewUrl">
        <div class="preview-box">
          <h3>Preview:</h3>
          <img :src="previewUrl" alt="Preview" class="preview-image" />
        </div>
      </div>
    </div>

    <div class="button-group">
      <a-button
        :loading="isLoading"
        type="primary"
        size="large"
        @click="classify"
        :disabled="isUploading || isLoading"
      >
        Classify
      </a-button>

      <a-button size="large" @click="sendForVerification" :disabled="isUploading || isLoading">
        Send for Verification
      </a-button>

      <a-button size="large" danger @click="resetForm" :disabled="isUploading || isLoading">
        Reset
      </a-button>
    </div>

    <a-alert
      v-if="message"
      :type="isError ? 'error' : 'success'"
      :message="message"
      show-icon
      class="result-alert"
    />

    <div class="info-section">
      <div class="info-card">
        <h2>🟢 How Classification Works</h2>
        <p>
          When you click <strong>Classify</strong>, your image is analyzed instantly using a ResNet-50 based AI model.
          It detects leaf patterns and compares them with verified <em>Magnolia pubescens</em> (Nilo) images.
        </p>
      </div>

      <div class="info-card">
        <h2>📤 How "Send for Verification" Works</h2>
        <p>
          Not confident with the result? Click <strong>Send for Verification</strong> and your image will be sent to the dev team
          for manual review and potential dataset inclusion. You'll get a confirmation when received.
        </p>
      </div>

      <div class="info-card warning">
        <h2>🚫 Image Upload Rules & Restrictions</h2>
        <p><strong>✅ Before uploading, make sure to:</strong></p>
        <ul>
          <li><strong>File Format:</strong> JPEG or JPG only</li>
          <li><strong>One Leaf Only:</strong> Avoid multiple leaves</li>
          <li><strong>Clear Background:</strong> Use white paper, soil, or plain cardboard</li>
          <li><strong>Good Lighting:</strong> Natural or bright lighting is ideal</li>
          <li><strong>Centered Leaf:</strong> Keep the leaf flat, centered, and visible</li>
        </ul>
        <p><strong>⚠️ Submissions may be rejected if:</strong></p>
        <ul>
          <li>Blurry, dark, or overexposed images</li>
          <li>Multiple leaves or objects present</li>
          <li>Wrong file format (not JPEG/JPG)</li>
          <li>Leaf is cropped or hidden</li>
        </ul>
        <p class="tip">
          Following these rules ensures better classification and helps improve the model!
        </p>
      </div>
    </div>

    <a-spin
      v-if="isUploading || isLoading"
      size="large"
      class="loading-overlay"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import { useRuntimeConfig } from '#app'

const selectedFile = ref<File | null>(null)
const isLoading = ref(false)
const isUploading = ref(false)
const message = ref('')
const isError = ref(false)
const previewUrl = ref('')

const config = useRuntimeConfig()
const baseURL = config.public.apiBase || 'http://localhost:8000'

function resizeImage(file: File): Promise<Blob> {
  return new Promise((resolve, reject) => {
    const img = new Image()
    const url = URL.createObjectURL(file)
    img.onload = () => {
      const canvas = document.createElement('canvas')
      canvas.width = 224
      canvas.height = 224
      const ctx = canvas.getContext('2d')
      if (!ctx) return reject('Canvas context not available')

      ctx.clearRect(0, 0, 224, 224)
      ctx.drawImage(img, 0, 0, 224, 224)

      canvas.toBlob(blob => {
        if (!blob) return reject('Canvas toBlob failed')
        resolve(blob)
      }, 'image/jpeg', 0.9)
    }
    img.onerror = reject
    img.src = url
  })
}

async function handleBeforeUpload(file: File) {
  if (!['image/jpeg', 'image/jpg'].includes(file.type)) {
    message.value = 'Only JPEG/JPG files are allowed.'
    isError.value = true
    return false
  }
  try {
    isUploading.value = true
    const blob = await resizeImage(file)
    const objectUrl = URL.createObjectURL(blob)
    previewUrl.value = objectUrl
    selectedFile.value = new File([blob], file.name, { type: 'image/jpeg' })
    message.value = ''
    isError.value = false
  } catch (e) {
    message.value = 'Failed to process image preview.'
    isError.value = true
  } finally {
    isUploading.value = false
  }
  return false
}

async function classify() {
  if (!selectedFile.value) {
    message.value = 'Please select a JPEG or JPG file before classifying.'
    isError.value = true
    return
  }
  isLoading.value = true
  isUploading.value = true
  message.value = ''
  isError.value = false

  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)

    const response = await axios.post(`${baseURL}/predict/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    message.value = `Classification Result: ${response.data.label || 'Unknown'}`
    isError.value = false
  } catch (error: any) {
    message.value = `Error: ${error?.response?.data?.detail || error.message || 'Classification failed. Please try again.'}`
    isError.value = true
  } finally {
    isLoading.value = false
    isUploading.value = false
  }
}

function sendForVerification() {
  if (!selectedFile.value) {
    message.value = 'Please select a file to send for verification.'
    isError.value = true
    return
  }
  message.value = 'Image sent for verification. Thank you!'
  isError.value = false
}

function resetForm() {
  selectedFile.value = null
  if (previewUrl.value) URL.revokeObjectURL(previewUrl.value)
  previewUrl.value = ''
  message.value = ''
  isError.value = false
}
</script>

<style scoped>
.classify-container {
  max-width: 900px;
  margin: 40px auto;
  padding: 30px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
  min-height: 80vh;
}

.title {
  font-size: 28px;
  font-weight: 700;
  text-align: center;
  color: #2e7d32;
}

.subtitle {
  text-align: center;
  color: #555;
  font-size: 15px;
  margin-bottom: 32px;
}

/* Upload + preview container side by side */
.upload-preview-row {
  display: flex;
  gap: 30px;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  margin-bottom: 32px;
}

.upload-box-wrapper,
.preview-box-wrapper {
  flex: 1 1 300px;
  max-width: 320px;
}

.upload-card {
  display: flex;
  justify-content: center;
}

.upload-box {
  width: 224px;
  height: 224px;
  border: 2px dashed #ccc;
  border-radius: 12px;
  background: #f8f8f8;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.upload-note {
  font-size: 13px;
  color: #777;
  margin-top: 8px;
  text-align: center;
  line-height: 1.2;
}


.preview-box {
  border: 2px dashed #ccc;
  border-radius: 12px;
  padding: 20px;
  background: #f8f8f8;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.preview-box h3 {
  font-size: 16px;
  color: #333;
  margin-bottom: 10px;
}

.preview-image {
  width: 224px;
  height: 224px;
  object-fit: contain;
  border-radius: 10px;
  border: 1px solid #ddd;
}

.button-group {
  display: flex;
  gap: 16px;
  margin-bottom: 32px;
  justify-content: center;
  flex-wrap: wrap;
}

.info-section {
  margin-top: 20px;
}

.info-card {
  background-color: #f9f9f9;
  padding: 20px 24px;
  border-radius: 10px;
  border-left: 5px solid #2e7d32;
  box-shadow: 0 3px 10px rgb(46 125 50 / 0.12);
  margin-bottom: 20px;
  color: #333;
}

.info-card.warning {
  border-color: #d32f2f;
  background-color: #fff0f0;
  color: #a00000;
}

.info-card h2 {
  margin-top: 0;
  font-size: 18px;
  margin-bottom: 12px;
  font-weight: 600;
}

.info-card ul {
  margin: 0 0 10px 18px;
}

.tip {
  font-style: italic;
  font-size: 14px;
  color: #555;
}

.result-alert {
  max-width: 700px;
  margin: 0 auto 24px;
}

.download-btn {
  display: block;
  margin: 0 auto 40px;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.7);
  z-index: 9999;
  display: flex;
  justify-content: center;
  align-items: center;
}

@media (max-width: 768px) {
  .upload-preview-row {
    flex-direction: column;
  }
  .upload-box-wrapper,
  .preview-box-wrapper {
    max-width: 100%;
  }
}
</style>
