import React from 'react'
import { PlayCircle, CheckCircle2, Clock, AlertCircle } from 'lucide-react'

const Execution = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold tracking-tight">Agent Execution</h2>
        <button className="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90 flex items-center">
          <PlayCircle className="mr-2 h-4 w-4" /> Start New Workflow
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Timeline */}
        <div className="lg:col-span-2 bg-card border border-border rounded-lg p-6">
          <h3 className="font-semibold text-lg mb-6">Execution Timeline</h3>
          <div className="space-y-6 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-border before:to-transparent">
            {/* Step 1 */}
            <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
              <div className="flex items-center justify-center w-10 h-10 rounded-full border-2 border-green-500 bg-green-50 text-green-500 shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2">
                <CheckCircle2 className="h-5 w-5" />
              </div>
              <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] bg-card border border-border p-4 rounded-lg shadow-sm">
                <div className="flex items-center justify-between mb-1">
                  <h4 className="font-bold text-foreground">Document Analysis</h4>
                  <span className="text-xs text-green-600 font-medium bg-green-100 px-2 py-1 rounded">Completed</span>
                </div>
                <p className="text-sm text-muted-foreground">Confidence: 94% | 2.4s</p>
              </div>
            </div>
            
            {/* Step 2 */}
            <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
              <div className="flex items-center justify-center w-10 h-10 rounded-full border-2 border-primary bg-primary/10 text-primary shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2">
                <Clock className="h-5 w-5 animate-pulse" />
              </div>
              <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] bg-card border border-primary/50 p-4 rounded-lg shadow-sm">
                <div className="flex items-center justify-between mb-1">
                  <h4 className="font-bold text-foreground">Marketing Strategy</h4>
                  <span className="text-xs text-primary font-medium bg-primary/10 px-2 py-1 rounded animate-pulse">Running</span>
                </div>
                <p className="text-sm text-muted-foreground">Synthesizing past campaigns...</p>
              </div>
            </div>

            {/* Step 3 */}
            <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
              <div className="flex items-center justify-center w-10 h-10 rounded-full border-2 border-border bg-background text-muted-foreground shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2">
                <AlertCircle className="h-5 w-5" />
              </div>
              <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] bg-card border border-border p-4 rounded-lg shadow-sm opacity-60">
                <div className="flex items-center justify-between mb-1">
                  <h4 className="font-bold text-foreground">Quality Assurance</h4>
                  <span className="text-xs text-muted-foreground font-medium bg-secondary px-2 py-1 rounded">Pending</span>
                </div>
                <p className="text-sm text-muted-foreground">Waiting for upstream agents</p>
              </div>
            </div>
          </div>
        </div>

        {/* Live Logs */}
        <div className="bg-card border border-border rounded-lg flex flex-col overflow-hidden">
          <div className="p-4 border-b border-border bg-secondary/50">
            <h3 className="font-semibold text-sm">Live Execution Logs</h3>
          </div>
          <div className="flex-1 p-4 bg-slate-950 text-slate-300 font-mono text-xs overflow-y-auto space-y-2 h-[400px]">
            <p className="text-green-400">[13:00:01] MasterAgent: Delegating to DocumentIntelligenceAgent</p>
            <p>[13:00:02] DocumentIntelligenceAgent: Fetching file 'brochure.pdf'</p>
            <p>[13:00:04] DocumentIntelligenceAgent: Completed successfully.</p>
            <p className="text-green-400">[13:00:04] MasterAgent: Routing to MarketingStrategyAgent</p>
            <p>[13:00:05] MarketingStrategyAgent: Querying ChromaDB for past campaigns...</p>
            <p className="animate-pulse">_</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Execution
