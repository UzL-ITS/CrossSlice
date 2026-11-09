import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

// Build output goes into the Python package so graph_server.py can serve it
// without a Node runtime. `npm run dev` proxies /api to a running server.
export default defineConfig({
  plugins: [vue(), tailwindcss()],
  build: {
    outDir: '../crossslice/cross/webui',
    emptyOutDir: true,
  },
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:8000',
    },
  },
})
