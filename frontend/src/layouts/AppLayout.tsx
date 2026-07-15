import React from 'react'
import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import TopNav from './TopNav'
import ChatPanel from '@/features/ChatPanel'

const AppLayout = () => {
  return (
    <div className="flex h-screen bg-background overflow-hidden">
      {/* Sidebar */}
      <Sidebar />
      
      {/* Main Content Area */}
      <div className="flex flex-col flex-1 overflow-hidden">
        <TopNav />
        
        <div className="flex flex-1 overflow-hidden">
          <main className="flex-1 overflow-y-auto p-6 bg-slate-50/50">
            <Outlet />
          </main>
          
          {/* Master Agent Chat Panel */}
          <ChatPanel />
        </div>
      </div>
    </div>
  )
}

export default AppLayout
