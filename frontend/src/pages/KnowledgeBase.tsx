import React from 'react'
import { Search } from 'lucide-react'

const KnowledgeBase = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold tracking-tight">Knowledge Base</h2>
      </div>

      <div className="relative max-w-xl">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <Search className="h-5 w-5 text-muted-foreground" />
        </div>
        <input
          type="text"
          className="block w-full pl-10 pr-3 py-3 border border-border rounded-lg leading-5 bg-card placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary text-sm shadow-sm"
          placeholder="Search semantic memory, documents, or websites..."
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mt-6">
        {['Past Campaigns', 'Website Snapshots', 'Competitor Profiles', 'Internal Policies'].map((category) => (
          <div key={category} className="bg-card border border-border rounded-lg p-5 hover:border-primary/50 cursor-pointer transition-colors">
            <h3 className="font-semibold">{category}</h3>
            <p className="text-xs text-muted-foreground mt-2">12 items indexed</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default KnowledgeBase
