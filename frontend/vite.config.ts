import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Local only: a wider bind makes Windows Firewall ask for admin approval.
    host: '127.0.0.1',
    port: 5173,
    strictPort: true
  }
})

