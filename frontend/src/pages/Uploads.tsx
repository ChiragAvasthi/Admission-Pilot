import React, { useState } from 'react'
import { UploadCloud, FileText, CheckCircle } from 'lucide-react'
import { useDropzone } from 'react-dropzone'

const Uploads = () => {
  const [files, setFiles] = useState<File[]>([])

  const onDrop = (acceptedFiles: File[]) => {
    setFiles([...files, ...acceptedFiles])
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop })

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold tracking-tight">Upload Documents</h2>
        <button className="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90">
          Process Uploads
        </button>
      </div>
      
      <div 
        {...getRootProps()} 
        className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors ${isDragActive ? 'border-primary bg-primary/5' : 'border-border hover:border-primary/50'}`}
      >
        <input {...getInputProps()} />
        <UploadCloud className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
        <p className="text-lg font-medium">Drag & drop files here, or click to select files</p>
        <p className="text-sm text-muted-foreground mt-2">Support for PDF, DOCX, TXT, CSV, Excel</p>
      </div>

      {files.length > 0 && (
        <div className="mt-8 bg-card border border-border rounded-lg p-6">
          <h3 className="font-semibold mb-4">Pending Uploads</h3>
          <ul className="space-y-3">
            {files.map((file, idx) => (
              <li key={idx} className="flex items-center justify-between p-3 bg-secondary rounded-md">
                <div className="flex items-center space-x-3">
                  <FileText className="h-5 w-5 text-primary" />
                  <span className="text-sm font-medium">{file.name}</span>
                </div>
                <CheckCircle className="h-5 w-5 text-green-500" />
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default Uploads
