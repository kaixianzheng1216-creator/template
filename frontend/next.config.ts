import type { NextConfig } from "next"

const backendUrl = process.env.BACKEND_URL

if (!backendUrl) throw new Error("必须配置 BACKEND_URL")

const nextConfig: NextConfig = {
  output: "standalone",
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${backendUrl}/api/:path*`,
      },
    ]
  },
}

export default nextConfig
