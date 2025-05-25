<template>
  <div class="landing">
    <!-- Banner -->
    <div class="header-image">
      <h1 class="title">MAGNOLIA PUBESCENS</h1>
      <img src="/leaves/leaf1.jpeg" class="banner-img" />
    </div>

    <!-- Info Sections -->
    <div class="info-section">
      <a-card>
        <h2>🌿 <i>Magnolia pubescens</i>: A Hidden Jewel of Philippine Flora</h2>
        <p>This app helps identify and conserve the rare species native to Mindanao using AI-powered tools.</p>
      </a-card>

      <a-collapse accordion>
        <a-collapse-panel key="1" header="🧬 Scientific Classification">
          <ul>
            <li><b>Scientific Name:</b> <i>Magnolia pubescens</i></li>
            <li><b>Family:</b> Magnoliaceae</li>
            <li><b>Genus:</b> <i>Magnolia</i></li>
            <li><b>Species:</b> <i>pubescens</i></li>
            <li><b>Authority:</b> Elmer Drew Merrill</li>
          </ul>
        </a-collapse-panel>

        <a-collapse-panel key="2" header="🌍 Geographic Distribution and Habitat">
          <p><i>Magnolia pubescens</i> is a <b>rare endemic</b> of <b>Lanao del Sur</b>, thriving in tropical montane forests.</p>
          <a-image src="/leaves/leaf2.jpeg" width="200" />
        </a-collapse-panel>

        <a-collapse-panel key="3" header="🌱 Botanical Description">
          <ul>
            <li><b>Leaves:</b> Large, leathery, with a hairy underside.</li>
            <li><b>Flowers:</b> Likely large and aromatic.</li>
            <li><b>Tree Form:</b> Medium-sized with a broad canopy.</li>
          </ul>
        </a-collapse-panel>

        <a-collapse-panel key="4" header="🛡️ Conservation Status">
          <p>Currently <b>Data Deficient</b> in IUCN, but likely endangered due to habitat loss and lack of protection.</p>
          <ul>
            <li>Logging and agriculture</li>
            <li>No targeted conservation policies</li>
            <li>Low public awareness</li>
          </ul>
        </a-collapse-panel>

        <a-collapse-panel key="5" header="🤖 Modern Tools for Identification">
          <p>Using models like <b>ResNet-50</b>, AI can identify Nilo leaves by analyzing features like shape and texture.</p>
        </a-collapse-panel>

        <a-collapse-panel key="6" header="🌱 Why Magnolia pubescens Matters">
          <ul>
            <li>Botanical uniqueness of the Philippines</li>
            <li>Supports forest biodiversity</li>
            <li>Endemic species protection</li>
            <li>Drives AI use in conservation</li>
          </ul>
        </a-collapse-panel>

        <a-collapse-panel key="7" header="📸 Call to Action">
          <ul>
            <li>Upload leaf photos for classification</li>
            <li>Promote reforestation efforts</li>
            <li>Spread awareness about this species</li>
          </ul>
        </a-collapse-panel>
      </a-collapse>
    </div>
  </div>
</template>
<style scoped>
.landing {
  padding-left: 64px;
  padding-bottom: 3rem;
}

.header-image {
  position: relative;
  width: 100%;
  height: 300px;
  overflow: hidden;
  border-radius: 12px;
}

.banner-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.title {
  position: absolute;
  top: 1rem;
  left: 1rem;
  color: white;
  font-size: 2rem;
  text-shadow: 1px 1px 4px black;
  z-index: 10;
}

.info-section {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
