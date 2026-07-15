import React from 'react'
import { render, screen } from '@testing-library/react'
import App from './App'

describe('App Layout', () => {
  it('renders the sidebar and topnav', () => {
    render(<App />)
    expect(screen.getByText('AdmissionPilot')).toBeInTheDocument()
    expect(screen.getByPlaceholderText(/Search projects/i)).toBeInTheDocument()
  })
})
