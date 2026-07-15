import React from 'react'

const Projects = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold tracking-tight">Projects</h2>
        <button className="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90">
          New Project
        </button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="bg-card border border-border rounded-lg p-6 hover:shadow-md transition-shadow cursor-pointer">
          <h3 className="font-semibold text-lg">Acme University Admission Drive</h3>
          <p className="text-sm text-muted-foreground mt-2">Targeting Fall 2027 admissions in the Midwest region.</p>
          <div className="mt-4 pt-4 border-t border-border flex justify-between items-center text-sm">
            <span className="text-green-600 font-medium">Active</span>
            <span className="text-muted-foreground">Updated 2h ago</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Projects
