// → Architecture & Build by DocSynapse
// Intelligent by Design. Crafted for Humanity.

'use client'

import { useState } from 'react'
import SearchBar from '@/components/SearchBar'
import DocumentList from '@/components/DocumentList'
import UploadArea from '@/components/UploadArea'

export default function Home() {
  const [searchResults, setSearchResults] = useState([])
  const [isLoading, setIsLoading] = useState(false)

  const handleSearch = async (query: string) => {
    setIsLoading(true)
    try {
      // TODO: Implement API call to backend
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      })
      const data = await response.json()
      setSearchResults(data.results || [])
    } catch (error) {
      console.error('Search error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold mb-8">DocMemory</h1>
        <p className="text-lg mb-8">Semantic Document Memory System</p>
        
        <SearchBar onSearch={handleSearch} isLoading={isLoading} />
        
        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-8">
          <DocumentList documents={searchResults} />
          <UploadArea />
        </div>
      </div>
    </main>
  )
}

