<template>
  <a-layout class="main-layout">
    <a-layout-header class="site-layout-header">
      <div class="header-content">
        <h1 class="title">MAGNOLIA PUBESCENS</h1>
        <nav class="nav-links">
          <router-link to="/" class="nav-link">Home</router-link>
          <router-link to="/gallery" class="nav-link">Gallery</router-link>
          <router-link to="/classify" class="nav-link">Classify</router-link>
        </nav>
      </div>
    </a-layout-header>

    <a-layout-content class="site-layout-content">
      <NuxtPage />
    </a-layout-content>

    <a-layout-footer class="site-layout-footer">
      Nilo Leaf Classifier ©2025 | A thesis project on Magnolia pubescens
    </a-layout-footer>
  </a-layout>
</template>
<style scoped>
.main-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.site-layout-header {
  background-color: #2e7d32;
  padding: 0 24px;
  color: white;
  display: flex;
  align-items: center;
  height: 64px;
}

.header-content {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  margin: 0;
  font-size: 20px;
  font-weight: bold;
  line-height: 1;
}

.nav-links {
  display: flex;
  gap: 24px;
}

.nav-link {
  color: white;
  font-weight: 600;
  font-size: 16px;
  text-decoration: none;
  padding: 6px 10px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.2);
  text-decoration: none;
}

.site-layout-content {
  flex-grow: 1;
  padding: 24px;
  background: white;
  max-width: 900px;
  margin: 16px auto;
  width: 100%;
  box-sizing: border-box;
}

.site-layout-footer {
  background-color: #f0f2f5;
  text-align: center;
  padding: 10px 0;
  font-size: 12px;
}
</style>
