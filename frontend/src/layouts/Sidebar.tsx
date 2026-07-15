import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { 
  LayoutDashboard, 
  Building2, 
  FolderKanban, 
  UploadCloud, 
  ActivitySquare, 
  FileText, 
  BookOpen, 
  Settings 
} from 'lucide-react'
import clsx from 'clsx'

const navigation = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Organizations', href: '/organizations', icon: Building2 },
  { name: 'Projects', href: '/projects', icon: FolderKanban },
  { name: 'Uploads', href: '/uploads', icon: UploadCloud },
  { name: 'Agent Execution', href: '/execution', icon: ActivitySquare },
  { name: 'Reports', href: '/reports', icon: FileText },
  { name: 'Knowledge Base', href: '/knowledge-base', icon: BookOpen },
  { name: 'Settings', href: '/settings', icon: Settings },
]

const Sidebar = () => {
  const location = useLocation()

  return (
    <div className="w-64 flex flex-col bg-card border-r border-border h-full">
      <div className="p-6">
        <h1 className="text-xl font-bold tracking-tight text-primary">AdmissionPilot</h1>
        <p className="text-xs text-muted-foreground mt-1">Enterprise Agentic AI</p>
      </div>
      
      <nav className="flex-1 px-4 space-y-1 overflow-y-auto">
        {navigation.map((item) => {
          const isActive = location.pathname === item.href || 
                           (item.href !== '/' && location.pathname.startsWith(item.href))
          return (
            <Link
              key={item.name}
              to={item.href}
              className={clsx(
                'group flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors',
                isActive 
                  ? 'bg-primary/10 text-primary' 
                  : 'text-foreground/80 hover:bg-slate-100 hover:text-foreground'
              )}
            >
              <item.icon
                className={clsx(
                  'mr-3 flex-shrink-0 h-5 w-5',
                  isActive ? 'text-primary' : 'text-muted-foreground group-hover:text-foreground'
                )}
                aria-hidden="true"
              />
              {item.name}
            </Link>
          )
        })}
      </nav>
    </div>
  )
}

export default Sidebar
