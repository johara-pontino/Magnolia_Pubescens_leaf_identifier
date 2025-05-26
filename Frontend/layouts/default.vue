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
  background: #F3EDE3;
}

.site-layout-header {
  background-color: #18442A; /* Dark green */
  padding: 0 24px;
  color: #E4DBC4; /* Light beige text */
  display: flex;
  align-items: center;
  height: 64px;
  box-shadow: 0 2px 8px rgba(24, 68, 42, 0.3);
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
  font-size: 22px;
  font-weight: bold;
  line-height: 1;
  color: #E4DBC4;
  letter-spacing: 1.1px;
}

.nav-links {
  display: flex;
  gap: 24px;
}

.nav-link {
  color: #E4DBC4; /* Light beige */
  font-weight: 600;
  font-size: 16px;
  text-decoration: none;
  padding: 6px 12px;
  border-radius: 6px;
  transition: background-color 0.3s, color 0.3s;
}

.nav-link:hover {
  background-color: #45644A; /* Medium green */
  color: #F3EDE3; /* Very light beige */
  text-decoration: none;
}

.site-layout-content {
  flex-grow: 1;
  padding: 24px;
  background: #E4DBC4; /* Light beige background for content */
  max-width: 900px;
  margin: 16px auto;
  width: 100%;
  box-sizing: border-box;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(69, 100, 74, 0.15);
  color: #18442A; /* Dark green text */
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.site-layout-footer {
  background-color: #45644A; /* Medium green */
  text-align: center;
  padding: 12px 0;
  font-size: 13px;
  color: #F3EDE3; /* Very light beige */
  font-weight: 500;
  box-shadow: 0 -2px 8px rgba(69, 100, 74, 0.3);
  user-select: none;
}
</style>
