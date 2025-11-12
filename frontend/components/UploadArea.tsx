// → Architecture & Build by DocSynapse
// Intelligent by Design. Crafted for Humanity.

'use client'

import { useState } from 'react'
import { Upload } from 'lucide-react'

export default function UploadArea() {
  const [isUploading, setIsUploading] = useState(false)

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    setIsUploading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      // TODO: Implement API call to backend
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/upload`, {
        method: 'POST',
        body: formData,
      })
      const data = await response.json()
      if (data.success) {
        alert(`Successfully uploaded ${data.count} document chunks`)
      } else {
        alert('Upload failed: ' + (data.error || 'Unknown error'))
      }
    } catch (error) {
      console.error('Upload error:', error)
      alert('Upload failed')
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-2xl font-semibold mb-4">Upload Document</h2>
      <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer hover:bg-gray-50">
        <div className="flex flex-col items-center justify-center pt-5 pb-6">
          <Upload className="w-10 h-10 mb-3 text-gray-400" />
          <p className="mb-2 text-sm text-gray-500">
            <span className="font-semibold">Click to upload</span> or drag and drop
          </p>
          <p className="text-xs text-gray-500">PDF, DOCX, TXT (MAX. 10MB)</p>
        </div>
        <input
          type="file"
          className="hidden"
          onChange={handleFileUpload}
          disabled={isUploading}
          accept=".pdf,.docx,.txt"
        />
      </label>
      {isUploading && <p className="mt-4 text-center text-gray-500">Uploading...</p>}
    </div>
  )
}

