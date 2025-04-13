/** @type {import('vite').UserConfig} */
const config = {
  server: {
    port: 5173,
    strictPort: false,
    proxy: {
      // Proxy API requests to the MCP-Gateway
      '/mcp': {
        target: 'http://localhost:9000',
        changeOrigin: true,
        secure: false
      }
    }
  }
};

module.exports = config;