/** @type {import('next').NextConfig} */
// → Architecture & Build by DocSynapse
// Intelligent by Design. Crafted for Humanity.

const nextConfig = {
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
  // TODO: Configure production API URL
  // TODO: Add environment-specific configurations
}

module.exports = nextConfig

