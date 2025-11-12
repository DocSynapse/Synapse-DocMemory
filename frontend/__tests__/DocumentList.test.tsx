// → Architecture & Build by DocSynapse
// Intelligent by Design. Crafted for Humanity.

import { render, screen } from '@testing-library/react'
import DocumentList from '@/components/DocumentList'

describe('DocumentList', () => {
  it('renders a list of documents', () => {
    const documents = [
      { id: '1', title: 'Document 1', content: 'This is the first document.', score: 0.9 },
      { id: '2', title: 'Document 2', content: 'This is the second document.', score: 0.8 },
    ]
    render(<DocumentList documents={documents} />)

    expect(screen.getByText('Document 1')).toBeInTheDocument()
    expect(screen.getByText('Document 2')).toBeInTheDocument()
  })

  it('renders a message when there are no documents', () => {
    render(<DocumentList documents={[]} />)
    expect(screen.getByText('No documents found. Try searching or uploading documents.')).toBeInTheDocument()
  })
})
