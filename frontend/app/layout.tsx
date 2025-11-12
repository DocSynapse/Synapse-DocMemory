// → Architecture & Build by DocSynapse
// Intelligent by Design. Crafted for Humanity.

import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Aethersite - Semantic Document Memory System',
  description: 'Advanced document memory system with vector search capabilities',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}

