// nuxt.config.ts
import tsconfigPaths from 'vite-tsconfig-paths'

export default defineNuxtConfig({
  modules: [
    '@pinia/nuxt',
    '@ant-design-vue/nuxt',
  ],

  antd: {
    // Optional: You can configure Ant Design Vue here if needed
  },

  css: [
    'ant-design-vue/dist/reset.css',
  ],

  vite: {
    plugins: [tsconfigPaths()],
    define: {
      'process.env': {},
    },
  },

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'https://magnolia-pubescens-leaf-identifier.onrender.com',

    
    },
  },
})
