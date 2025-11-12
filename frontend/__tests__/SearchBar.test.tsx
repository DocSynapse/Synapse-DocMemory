// → Architecture & Build by DocSynapse
// Intelligent by Design. Crafted for Humanity.

import { render, screen, fireEvent } from '@testing-library/react'
import SearchBar from '@/components/SearchBar'

describe('SearchBar', () => {
  it('renders search input and button', () => {
    const mockOnSearch = jest.fn()
    render(<SearchBar onSearch={mockOnSearch} />)
    
    expect(screen.getByPlaceholderText(/search documents/i)).toBeInTheDocument()
    expect(screen.getByText('Search')).toBeInTheDocument()
  })

  it('calls onSearch when form is submitted', () => {
    const mockOnSearch = jest.fn()
    render(<SearchBar onSearch={mockOnSearch} />)
    
    const input = screen.getByPlaceholderText(/search documents/i)
    const button = screen.getByText('Search')
    
    fireEvent.change(input, { target: { value: 'test query' } })
    fireEvent.click(button)
    
    expect(mockOnSearch).toHaveBeenCalledWith('test query')
  })

  // TODO: Add more test cases
})

