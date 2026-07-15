import React from 'react'

const Organizations = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold tracking-tight">Organizations</h2>
        <button className="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90">
          Create Organization
        </button>
      </div>
      <div className="bg-card border border-border rounded-lg p-8 text-center text-muted-foreground">
        No organizations found. Create one to get started.
      </div>
    </div>
  )
}

export default Organizations
