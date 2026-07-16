import React, { useEffect, useState } from 'react'
import { fetchOrganizations, createOrganization } from '@/services/api'
import { useAppStore } from '@/store/useAppStore'
import { Building2 } from 'lucide-react'

const Organizations = () => {
  const [orgs, setOrgs] = useState<any[]>([])
  const [newOrgName, setNewOrgName] = useState('')
  const { setOrganization, currentOrganization } = useAppStore()

  useEffect(() => {
    loadOrgs()
  }, [])

  const loadOrgs = async () => {
    try {
      const data = await fetchOrganizations()
      setOrgs(data)
    } catch (e) {
      console.error(e)
    }
  }

  const handleCreate = async () => {
    if (!newOrgName.trim()) return
    try {
      await createOrganization({ name: newOrgName, description: 'Created from UI' })
      setNewOrgName('')
      loadOrgs()
    } catch (e) {
      alert("Failed to create organization")
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold tracking-tight">Organizations</h2>
        <div className="flex space-x-2">
          <input 
            type="text" 
            placeholder="Org Name" 
            value={newOrgName} 
            onChange={(e) => setNewOrgName(e.target.value)}
            className="border border-border rounded-md px-3 py-1.5 text-sm"
          />
          <button onClick={handleCreate} className="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90">
            Create Organization
          </button>
        </div>
      </div>
      
      {orgs.length === 0 ? (
        <div className="bg-card border border-border rounded-lg p-8 text-center text-muted-foreground">
          No organizations found. Create one to get started.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {orgs.map(org => (
            <div 
              key={org.id} 
              onClick={() => setOrganization(org.id)}
              className={`bg-card border rounded-lg p-6 hover:shadow-md transition-shadow cursor-pointer ${currentOrganization === org.id ? 'border-primary ring-1 ring-primary' : 'border-border'}`}
            >
              <div className="flex items-center space-x-3">
                <Building2 className="text-primary" />
                <h3 className="font-semibold text-lg">{org.name}</h3>
              </div>
              <p className="text-sm text-muted-foreground mt-2">{org.description}</p>
              <div className="mt-4 pt-4 border-t border-border text-xs text-muted-foreground">
                ID: {org.id.split('-')[0]}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default Organizations
