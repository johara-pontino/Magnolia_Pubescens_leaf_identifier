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
      >
        <div class="upload-box">
          <a-button type="primary" size="large">Choose File</a-button>
          <p class="upload-note">JPEG or JPG format only</p>
        </div>
      </a-upload>

      <div class="button-group">
        <a-button type="primary" size="large">Classify</a-button>
        <a-button size="large">Send for Verification</a-button>
      </div>
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
function handleBeforeUpload(file: File) {
  console.log('Selected file:', file)
  return false // prevent auto-upload
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
  min-height: 80vh; /* NEW */
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
  justify-content: center; /* NEW */
  min-height: 400px; /* Ensures space for vertical centering */
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
