import React from 'react'
import { FileText, Download, Printer } from 'lucide-react'
import ReactMarkdown from 'react-markdown'

const Reports = () => {
  const markdownContent = `
# Executive Summary
The Acme University Admission Drive for Fall 2027 shows strong potential in the Midwest region.

## Website Audit
* **Strengths**: Good navigation structure.
* **Weaknesses**: Mobile load times are >3s.

## Competitor Matrix
Competitors in the region are currently outspending on digital ad channels by 20%.
  `

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold tracking-tight">Generated Reports</h2>
        <div className="flex space-x-3">
          <button className="p-2 border border-border rounded-md hover:bg-slate-100 text-muted-foreground">
            <Printer className="h-4 w-4" />
          </button>
          <button className="px-4 py-2 border border-border rounded-md text-sm font-medium hover:bg-slate-100 flex items-center">
            <Download className="mr-2 h-4 w-4" /> Export PDF
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Report List */}
        <div className="bg-card border border-border rounded-lg p-4 space-y-2 overflow-y-auto h-[600px]">
          <div className="p-3 bg-primary/10 border-l-2 border-primary rounded-r-md cursor-pointer">
            <h4 className="font-semibold text-sm">Fall 2027 Strategy</h4>
            <p className="text-xs text-muted-foreground mt-1">Generated 2 hours ago</p>
          </div>
          <div className="p-3 hover:bg-secondary rounded-md cursor-pointer transition-colors">
            <h4 className="font-semibold text-sm">Competitor SWOT Q3</h4>
            <p className="text-xs text-muted-foreground mt-1">Generated 2 days ago</p>
          </div>
        </div>

        {/* Report Viewer */}
        <div className="lg:col-span-3 bg-card border border-border rounded-lg p-8 shadow-sm prose prose-slate max-w-none overflow-y-auto h-[600px]">
          <ReactMarkdown>{markdownContent}</ReactMarkdown>
        </div>
      </div>
    </div>
  )
}

export default Reports
