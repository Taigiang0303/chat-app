/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  output: 'standalone',
  images: {
    domains: ['avatars.githubusercontent.com', 'images.unsplash.com'],
    formats: ['image/avif', 'image/webp'],
  },
  async rewrites() {
    return [
      // API Gateway handles routing to specific services
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
      // Direct WebSocket connection to chat service
      {
        source: '/ws',
        destination: 'http://localhost:8002/ws',
      },
    ];
  },
};

module.exports = nextConfig; 