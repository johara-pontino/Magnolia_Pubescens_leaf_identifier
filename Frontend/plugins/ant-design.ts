// plugins/ant-design.js
import {
  HomeOutlined,
  PictureOutlined,
  AppstoreOutlined,
  BarsOutlined // instead of CategoryOutlined
} from '@ant-design/icons-vue'

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.component('home-outlined', HomeOutlined)
  nuxtApp.vueApp.component('picture-outlined', PictureOutlined)
  nuxtApp.vueApp.component('appstore-outlined', AppstoreOutlined)
  nuxtApp.vueApp.component('bars-outlined', BarsOutlined)
})
