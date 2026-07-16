import React, { useEffect, useState } from 'react'
import { fetchProjects, createProject } from '@/services/api'
import { useAppStore } from '@/store/useAppStore'
import { FolderKanban } from 'lucide-react'

const Projects = () => {
  const [projects, setProjects] = useState<any[]>([])
  const [newProjectName, setNewProjectName] = useState('')
  const { currentOrganization, setProject, currentProject } = useAppStore()

  useEffect(() => {
    if (currentOrganization) {
      loadProjects()
    } else {
      setProjects([])
    }
  }, [currentOrganization])

  const loadProjects = async () => {
    try {
      if (!currentOrganization) return
      const data = await fetchProjects(currentOrganization)
      setProjects(data)
    } catch (e) {
      console.error(e)
    }
  }

  const handleCreate = async () => {
    if (!newProjectName.trim() || !currentOrganization) return
    try {
      await createProject({ 
        organization_id: currentOrganization,
        name: newProjectName, 
        description: 'New admissions project',
        website_url: 'https://example.com'
      })
      setNewProjectName('')
      loadProjects()
    } catch (e) {
      alert("Failed to create project")
    }
  }

  if (!currentOrganization) {
    return (
      <div className="flex justify-center items-center h-64 text-muted-foreground">
        Please select an Organization first.
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold tracking-tight">Projects</h2>
        <div className="flex space-x-2">
          <input 
            type="text" 
            placeholder="Project Name" 
            value={newProjectName} 
            onChange={(e) => setNewProjectName(e.target.value)}
            className="border border-border rounded-md px-3 py-1.5 text-sm"
          />
          <button onClick={handleCreate} className="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90">
            New Project
          </button>
        </div>
      </div>
      
      {projects.length === 0 ? (
        <div className="bg-card border border-border rounded-lg p-8 text-center text-muted-foreground">
          No projects found in this organization.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map(proj => (
            <div 
              key={proj.id} 
              onClick={() => setProject(proj.id)}
              className={`bg-card border rounded-lg p-6 hover:shadow-md transition-shadow cursor-pointer ${currentProject === proj.id ? 'border-primary ring-1 ring-primary' : 'border-border'}`}
            >
              <div className="flex items-center space-x-3">
                <FolderKanban className="text-primary" />
                <h3 className="font-semibold text-lg">{proj.name}</h3>
              </div>
              <p className="text-sm text-muted-foreground mt-2">{proj.description}</p>
              <div className="mt-4 pt-4 border-t border-border flex justify-between items-center text-sm">
                <span className="text-green-600 font-medium capitalize">{proj.status}</span>
                <span className="text-muted-foreground">ID: {proj.id.split('-')[0]}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default Projects
