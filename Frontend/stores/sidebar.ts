// stores/sidebar.ts
import { defineStore } from 'pinia'

export const useSidebarStore = defineStore('sidebar', {
  state: () => ({
    collapsed: true,
  }),
  actions: {
    toggle() {
      this.collapsed = !this.collapsed
    },
    set(state: boolean) {
      this.collapsed = state
    },
  },
})
