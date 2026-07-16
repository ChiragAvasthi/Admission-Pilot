import React, { useEffect, useState } from 'react'
import { FileText, Download, Printer } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import { fetchReports } from '@/services/api'
import { useAppStore } from '@/store/useAppStore'

const Reports = () => {
  const { currentProject } = useAppStore()
  const [reports, setReports] = useState<any[]>([])
  const [selectedReport, setSelectedReport] = useState<any>(null)

  useEffect(() => {
    if (currentProject) {
      loadReports()
    }
  }, [currentProject])

  const loadReports = async () => {
    try {
      if (!currentProject) return
      const data = await fetchReports(currentProject)
      setReports(data)
      if (data.length > 0) {
        setSelectedReport(data[0])
      }
    } catch (e) {
      console.error(e)
    }
  }

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
        <h2 className="text-2xl font-bold tracking-tight">Generated Reports</h2>
        <div className="flex space-x-3">
          <button className="p-2 border border-border rounded-md hover:bg-slate-100 text-muted-foreground disabled:opacity-50" disabled={!selectedReport}>
            <Printer className="h-4 w-4" />
          </button>
          <button className="px-4 py-2 border border-border rounded-md text-sm font-medium hover:bg-slate-100 flex items-center disabled:opacity-50" disabled={!selectedReport}>
            <Download className="mr-2 h-4 w-4" /> Export PDF
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Report List */}
        <div className="bg-card border border-border rounded-lg p-4 space-y-2 overflow-y-auto h-[600px]">
          {reports.length === 0 ? (
            <p className="text-sm text-muted-foreground text-center mt-4">No reports found.</p>
          ) : (
            reports.map(report => (
              <div 
                key={report.id}
                onClick={() => setSelectedReport(report)}
                className={`p-3 rounded-md cursor-pointer transition-colors ${selectedReport?.id === report.id ? 'bg-primary/10 border-l-2 border-primary rounded-r-md' : 'hover:bg-secondary'}`}
              >
                <h4 className="font-semibold text-sm">{report.title}</h4>
                <p className="text-xs text-muted-foreground mt-1">{new Date(report.created_at).toLocaleString()}</p>
              </div>
            ))
          )}
        </div>

        {/* Report Viewer */}
        <div className="lg:col-span-3 bg-card border border-border rounded-lg p-8 shadow-sm prose prose-slate max-w-none overflow-y-auto h-[600px]">
          {selectedReport ? (
            <ReactMarkdown>{selectedReport.content}</ReactMarkdown>
          ) : (
            <div className="flex h-full items-center justify-center text-muted-foreground">
              Select a report to view
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Reports
