<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-4">Image Gallery</h1>
    <a-row :gutter="[16, 16]">
      <a-col
        v-for="(image, index) in images"
        :key="index"
        :xs="24"
        :sm="12"
        :md="8"
        :lg="6"
        :xl="4"
      >
        <a-card hoverable :cover="h('img', { src: `/leaves/${image}`, alt: image, style: 'height: 200px; object-fit: cover;' })">
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script setup>
import { h } from 'vue'

const images = [
  
  '01.jpg',
  '02.jpg',
  '03.jpg',
  '05.jpg',
  '06.jpg',
  '07.jpg',
  '10.jpg',
  '11.jpg',
  '13.jpg',
  '14.jpg',
  '15.jpg',
  '16.jpg',
  
 

]
</script>
