import React, { useState, useEffect } from 'react'
import { UploadCloud, FileText, CheckCircle, AlertCircle } from 'lucide-react'
import { useDropzone } from 'react-dropzone'
import { api } from '@/services/api'
import { useAppStore } from '@/store/useAppStore'

const Uploads = () => {
  const { currentProject } = useAppStore()
  const [uploads, setUploads] = useState<any[]>([])
  const [uploading, setUploading] = useState(false)

  useEffect(() => {
    if (currentProject) {
      loadUploads()
    } else {
      setUploads([])
    }
  }, [currentProject])

  const loadUploads = async () => {
    try {
      if (!currentProject) return
      const res = await api.get(`/uploads?project_id=${currentProject}`)
      setUploads(res.data)
    } catch (e) {
      console.error(e)
    }
  }

  const onDrop = async (acceptedFiles: File[]) => {
    if (!currentProject) {
      alert("Please select a project first")
      return
    }
    
    setUploading(true)
    try {
      for (const file of acceptedFiles) {
        const formData = new FormData()
        formData.append('project_id', currentProject)
        formData.append('file', file)
        
        await api.post('/uploads', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
      }
      loadUploads()
    } catch (e) {
      console.error(e)
      alert("Error uploading files")
    } finally {
      setUploading(false)
    }
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop })

  if (!currentProject) {
    return (
      <div className="flex justify-center items-center h-64 text-muted-foreground">
        Please select a Project first.
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold tracking-tight">Upload Documents</h2>
      </div>
      
      <div 
        {...getRootProps()} 
        className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors ${isDragActive ? 'border-primary bg-primary/5' : 'border-border hover:border-primary/50'} ${uploading ? 'opacity-50 pointer-events-none' : ''}`}
      >
        <input {...getInputProps()} />
        <UploadCloud className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
        <p className="text-lg font-medium">{uploading ? 'Uploading...' : 'Drag & drop files here, or click to select files'}</p>
        <p className="text-sm text-muted-foreground mt-2">Support for PDF, DOCX, TXT, CSV, Excel</p>
      </div>

      {uploads.length > 0 && (
        <div className="mt-8 bg-card border border-border rounded-lg p-6">
          <h3 className="font-semibold mb-4">Uploaded Files</h3>
          <ul className="space-y-3">
            {uploads.map((upload) => (
              <li key={upload.id} className="flex items-center justify-between p-3 bg-secondary rounded-md">
                <div className="flex items-center space-x-3">
                  <FileText className="h-5 w-5 text-primary" />
                  <div>
                    <p className="text-sm font-medium">{upload.filename}</p>
                    <p className="text-xs text-muted-foreground capitalize">{upload.status}</p>
                  </div>
                </div>
                {upload.status === 'failed' ? (
                  <AlertCircle className="h-5 w-5 text-red-500" />
                ) : (
                  <CheckCircle className="h-5 w-5 text-green-500" />
                )}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default Uploads
