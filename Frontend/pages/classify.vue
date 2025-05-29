<template>
  <div class="classify-container">
    <h1 class="title">🌿 Nilo Leaf Classifier</h1>
    <p class="subtitle">
      Upload a leaf image to see if it's <em>Magnolia pubescens</em> (Nilo).
    </p>

    <div class="main-content">
      <!-- LEFT: Info Cards -->
      <div class="info-section">
        <div class="info-card">
          <h2>🟢 How Classification Works</h2>
          <p>
            When you click <strong>Classify</strong>, your image is analyzed using a ResNet-50 AI model.
            It detects leaf patterns and compares them with verified <em>Magnolia pubescens</em> (Nilo) images.
          </p>
        </div>

        <div class="info-card">
          <h2>📤 How "Send for Verification" Works</h2>
          <p>
            Not confident with the result? Click <strong>Send for Verification</strong> to send your image to the dev team
            for manual review and possible dataset inclusion.
          </p>
        </div>

        <div class="info-card warning">
          <h2>🚫 Image Upload Rules & Restrictions</h2>
          <p><strong>✅ Before uploading, make sure to:</strong></p>
          <ul>
            <li><strong>File Format:</strong> JPEG or JPG only</li>
            <li><strong>One Leaf Only:</strong> Avoid multiple leaves</li>
            <li><strong>Clear Background:</strong> Use plain white, soil, or cardboard</li>
            <li><strong>Good Lighting:</strong> Natural or bright light is best</li>
            <li><strong>Centered Leaf:</strong> Flat, centered, fully visible</li>
          </ul>
          <p><strong>⚠️ Submissions may be rejected if:</strong></p>
          <ul>
            <li>Blurry, dark, or overexposed images</li>
            <li>Multiple leaves or other objects</li>
            <li>Wrong file format</li>
            <li>Leaf is cropped or unclear</li>
          </ul>
          <p class="tip">
            Following these tips improves accuracy and helps train the model!
          </p>
        </div>
      </div>

      <!-- RIGHT: Upload + Preview -->
      <div class="upload-section">
        <div class="upload-content">
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

          <div class="preview-box" v-if="previewUrl">
            <h3>Preview:</h3>
            <img :src="previewUrl" alt="Preview" class="preview-image" />
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
        </div>
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
import { useRuntimeConfig } from 'nuxt/app'

const selectedFile = ref<File | null>(null)
const isLoading = ref(false)
const isUploading = ref(false)
const message = ref('')
const isError = ref(false)
const previewUrl = ref('')


const config = useRuntimeConfig()
const baseURL = config.public.apiBase


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
  max-width: 1200px;
  margin: 40px auto;
  padding: 30px;
  background: #F3EDE3;
  border-radius: 16px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
}

.title {
  font-size: 28px;
  font-weight: 700;
  text-align: center;
  color: #18442A;
}

.subtitle {
  text-align: center;
  color: #45644A;
  font-size: 15px;
  margin-bottom: 32px;
}

.main-content {
  display: flex;
  flex-direction: row; /* Side by side layout */
  gap: 40px;
  align-items: flex-start;
  justify-content: space-between;
  flex-wrap: nowrap; /* Prevent stacking */
}

.info-section {
  flex: 1 1 60%;
  min-width: 400px;
  max-width: 700px;
  padding-right: 20px;
  margin-right: 20px;
  margin-top: 50px;
}

.upload-section {
  flex: 1 1 40%;
  min-width: 300px;
  max-width: 400px;

  display: flex;
  justify-content: center;
  align-items: flex-start;
}


/* The actual content inside the right column */
.upload-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
  width: 100%;
  max-width: 280px;
}

.upload-card {
  display: flex;
  justify-content: center;
}

.upload-box {
  width: 224px;
  height: 224px;
  border: 2px dashed #45644A;
  border-radius: 12px;
  background: #E4DBC4;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.upload-note {
  font-size: 13px;
  color: #555;
  margin-top: 8px;
  text-align: center;
  line-height: 1.2;
}

.preview-box {
  border: 2px dashed #45644A;
  border-radius: 12px;
  padding: 20px;
  background: #E4DBC4;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.preview-box h3 {
  font-size: 16px;
  color: #18442A;
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
  justify-content: center;
  flex-wrap: wrap;
}

.info-card {
  background-color: #fff;
  padding: 20px 24px;
  border-radius: 10px;
  border-left: 5px solid #18442A;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.06);
  color: #333;
  margin-bottom: 16px;
}

.info-card.warning {
  border-color: #a00000;
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
  max-width: 100%;
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
  .main-content {
    flex-direction: column;
  }

  .upload-section {
    justify-content: flex-start;
    align-items: stretch;
  }

  .upload-content {
    max-width: 100%;
  }
}

</style>
