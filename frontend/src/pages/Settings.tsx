import React from 'react'

const Settings = () => {
  return (
    <div className="space-y-6 max-w-4xl">
      <h2 className="text-2xl font-bold tracking-tight">Settings</h2>

      <div className="bg-card border border-border rounded-lg p-6 space-y-6">
        <div>
          <h3 className="text-lg font-medium">Application Settings</h3>
          <p className="text-sm text-muted-foreground mt-1">Manage your workspace preferences.</p>
        </div>
        
        <div className="space-y-4 pt-4 border-t border-border">
          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium text-sm">Theme</p>
              <p className="text-xs text-muted-foreground">Select light, dark, or system theme.</p>
            </div>
            <select className="border border-border rounded-md px-3 py-1.5 text-sm bg-background">
              <option>Light</option>
              <option>Dark</option>
              <option>System</option>
            </select>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium text-sm">API Endpoint</p>
              <p className="text-xs text-muted-foreground">Base URL for backend API.</p>
            </div>
            <input 
              type="text" 
              defaultValue="http://localhost:8000/api"
              className="border border-border rounded-md px-3 py-1.5 text-sm bg-background w-64" 
            />
          </div>

          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium text-sm">Default AI Model</p>
              <p className="text-xs text-muted-foreground">The model Master Agent uses by default.</p>
            </div>
            <select className="border border-border rounded-md px-3 py-1.5 text-sm bg-background w-64">
              <option>qwen3:8b</option>
              <option>llama3:8b</option>
              <option>mistral:7b</option>
            </select>
          </div>
        </div>
        
        <div className="pt-4 flex justify-end">
          <button className="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90">
            Save Changes
          </button>
        </div>
      </div>
    </div>
  )
}

export default Settings
