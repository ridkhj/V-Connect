import path from 'path'
import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src/ui"),
    },
  },

  base: './',
  build: {
    outDir: "dist-react"
  },
  server: {
    port: 5132,
    strictPort: true
  }
})
