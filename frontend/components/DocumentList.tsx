// → Architecture & Build by DocSynapse
// Intelligent by Design. Crafted for Humanity.

'use client'

interface Document {
  id: string
  title: string
  content: string
  score?: number
  tags?: string[]
}

interface DocumentListProps {
  documents: Document[]
}

export default function DocumentList({ documents }: DocumentListProps) {
  if (documents.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <p className="text-gray-500">No documents found. Try searching or uploading documents.</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold mb-4">Search Results</h2>
      {documents.map((doc) => (
        <div key={doc.id} className="bg-white rounded-lg shadow p-6">
          <h3 className="text-xl font-semibold mb-2">{doc.title}</h3>
          {doc.score !== undefined && (
            <p className="text-sm text-gray-500 mb-2">Score: {doc.score.toFixed(3)}</p>
          )}
          <p className="text-gray-700 mb-4">{doc.content}</p>
          {doc.tags && doc.tags.length > 0 && (
            <div className="flex gap-2 flex-wrap">
              {doc.tags.map((tag) => (
                <span key={tag} className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-sm">
                  {tag}
                </span>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}

