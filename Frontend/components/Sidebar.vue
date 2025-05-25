<script setup lang="ts">
import { HomeOutlined, PictureOutlined, AppstoreOutlined as CategoryOutlined } from '@ant-design/icons-vue'
</script>

<template>
  <!-- Green bar as the top of the page -->
  <header class="bg-[#2E7D32] text-white w-full shadow-md relative h-24">
    <!-- Centered title vertically -->
    <div class="flex justify-center items-center h-full">
      <!-- <h1 class="text-xl font-bold">MAGNOLIA PUBESCENS</h1> -->
    </div>

    <!-- <nav class="absolute bottom-1 left-0 right-0 flex justify-center space-x-6 text-sm">
      <router-link to="/" class="flex items-center space-x-1 hover:underline">
        <HomeOutlined />
        <span>Home</span>
      </router-link>

      <router-link to="/gallery" class="flex items-center space-x-1 hover:underline">
        <PictureOutlined />
        <span>Gallery</span>
      </router-link>

      <router-link to="/classify" class="flex items-center space-x-1 hover:underline">
        <CategoryOutlined />
        <span>Classify</span>
      </router-link>
    </nav> -->
  </header>
</template>

<style scoped>
body {
  margin: 0;         /* Removes default white margin */
  padding-top: 0;    /* Ensures no space above header */
}
</style>
