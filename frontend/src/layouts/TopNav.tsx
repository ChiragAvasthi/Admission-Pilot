import React from 'react'
import { Bell, Search, User } from 'lucide-react'
import { useAppStore } from '@/store/useAppStore'

const TopNav = () => {
  const { currentOrganization, currentProject } = useAppStore()

  return (
    <header className="bg-card border-b border-border h-16 flex items-center justify-between px-6">
      <div className="flex items-center flex-1">
        {/* Search Bar */}
        <div className="relative w-96 hidden md:block">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-4 w-4 text-muted-foreground" />
          </div>
          <input
            type="text"
            className="block w-full pl-10 pr-3 py-2 border border-border rounded-md leading-5 bg-background placeholder-muted-foreground focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary sm:text-sm"
            placeholder="Search projects, reports, or agents..."
          />
        </div>
      </div>
      
      <div className="flex items-center space-x-4">
        {/* Context Indicators */}
        <div className="hidden lg:flex items-center space-x-2 text-sm">
          <span className="px-2 py-1 rounded bg-secondary text-secondary-foreground font-medium">
            {currentOrganization || 'No Org Selected'}
          </span>
          <span className="text-muted-foreground">/</span>
          <span className="px-2 py-1 rounded bg-secondary text-secondary-foreground font-medium">
            {currentProject || 'No Project Selected'}
          </span>
        </div>

        {/* Notifications & Profile */}
        <button className="p-2 rounded-full hover:bg-slate-100 text-muted-foreground transition-colors">
          <Bell className="h-5 w-5" />
        </button>
        <button className="p-2 rounded-full bg-slate-200 text-slate-600 hover:bg-slate-300 transition-colors">
          <User className="h-5 w-5" />
        </button>
      </div>
    </header>
  )
}

export default TopNav
