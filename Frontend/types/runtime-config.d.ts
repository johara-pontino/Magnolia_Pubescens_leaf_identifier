// types/runtime-config.d.ts
export interface PublicRuntimeConfig {
  apiBase: string
}

declare module '#app' {
  interface RuntimeConfig extends PublicRuntimeConfig {}
}
