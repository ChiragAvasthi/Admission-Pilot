import React from 'react'

const Dashboard = () => {
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold tracking-tight text-foreground">Dashboard</h2>
      <p className="text-muted-foreground">Welcome to the AdmissionPilot command center.</p>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-card p-6 rounded-lg border border-border shadow-sm">
          <h3 className="text-sm font-medium text-muted-foreground">Active Projects</h3>
          <p className="text-3xl font-bold mt-2">12</p>
        </div>
        <div className="bg-card p-6 rounded-lg border border-border shadow-sm">
          <h3 className="text-sm font-medium text-muted-foreground">Agents Running</h3>
          <p className="text-3xl font-bold mt-2 text-primary">3</p>
        </div>
        <div className="bg-card p-6 rounded-lg border border-border shadow-sm">
          <h3 className="text-sm font-medium text-muted-foreground">Generated Reports</h3>
          <p className="text-3xl font-bold mt-2 text-green-600">45</p>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
