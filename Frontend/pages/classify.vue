<template>
  <div class="classify-container">
    <h1 class="title">🌿 Nilo Leaf Classifier</h1>
    <p class="subtitle">
      Upload a leaf image to see if it's <em>Magnolia pubescens</em> (Nilo).
    </p>

      <div class="content-grid">
        <!-- Left Column: Upload & Actions -->
      <div class="upload-section">
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
        </div>

        <p v-if="message" :class="{ error: isError, success: !isError }">{{ message }}</p>
      </div>

      <!-- Right Column: Info Section -->
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
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

const selectedFile = ref<File | null>(null)
const isLoading = ref(false)
const isUploading = ref(false) // NEW reactive state for upload progress
const message = ref('')
const isError = ref(false)

const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

function handleBeforeUpload(file: File) {
  if (!['image/jpeg', 'image/jpg'].includes(file.type)) {
    message.value = 'Only JPEG/JPG files are allowed.'
    isError.value = true
    return false
  }
  selectedFile.value = file
  message.value = ''
  isError.value = false
  return false // prevent auto-upload by a-upload
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

    const response = await axios.post(`${baseURL}/predict`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    message.value = `Classification Result: ${response.data.label || 'Unknown'}`
    isError.value = false
  } catch (error) {
    message.value = 'Error during classification. Please try again later.'
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
  // Replace with your actual logic to send the file for verification
  message.value = 'Image sent for verification. Thank you!'
  isError.value = false
}
</script>

<style scoped>
.classify-container {
  max-width: 1200px;
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

.content-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 40px;
  justify-content: center;
}

.upload-section {
  flex: 1 1 350px;
  max-width: 450px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.upload-card {
  width: 100%;
  display: flex;
  justify-content: center;
}

.upload-box {
  width: 100%;
  max-width: 360px;
  border: 2px dashed #ccc;
  border-radius: 12px;
  padding: 50px 20px;
  background: #f8f8f8;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  /* transition for smooth visual change */
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.upload-box.uploading {
  border-color: #52c41a; /* Ant Design green */
  background-color: #f6ffed;
}

.upload-note {
  font-size: 13px;
  color: #777;
  margin-top: 10px;
}

.button-group {
  display: flex;
  gap: 16px;
  margin-top: 24px;
  justify-content: center;
  flex-wrap: wrap;
}

.info-section {
  flex: 1 1 450px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.info-card {
  background-color: #f9f9f9;
  padding: 20px 24px;
  border-radius: 10px;
  border-left: 5px solid #2e7d32;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.info-card.warning {
  border-left-color: #d32f2f;
}

.info-card h2 {
  margin-bottom: 10px;
  font-size: 18px;
  color: #2e7d32;
}

.info-card.warning h2 {
  color: #d32f2f;
}

.info-card ul {
  padding-left: 20px;
  margin: 8px 0;
}

.info-card li,
.info-card p {
  font-size: 14px;
  color: #333;
  line-height: 1.6;
}

.tip {
  font-style: italic;
  color: #555;
  margin-top: 10px;
  font-size: 13px;
}

p.success {
  color: #2e7d32;
  margin-top: 20px;
  font-weight: 600;
}

p.error {
  color: #d32f2f;
  margin-top: 20px;
  font-weight: 600;
}

/* Responsive behavior */
@media (max-width: 900px) {
  .content-grid {
    flex-direction: column;
    align-items: center;
  }

  .upload-section,
  .info-section {
    max-width: 100%;
  }
}
</style>
