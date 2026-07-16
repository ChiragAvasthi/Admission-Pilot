import React, { useState, useEffect } from 'react'
import { PlayCircle, CheckCircle2, Clock, AlertCircle } from 'lucide-react'
import { useAppStore } from '@/store/useAppStore'
import { startExecution } from '@/services/api'

const Execution = () => {
  const { currentProject } = useAppStore()
  const [executionId, setExecutionId] = useState<string | null>(null)
  const [logs, setLogs] = useState<string[]>([])
  const [status, setStatus] = useState<string>('idle')
  const [ws, setWs] = useState<WebSocket | null>(null)

  const handleStart = async () => {
    if (!currentProject) {
      alert("Please select a project first")
      return
    }
    
    try {
      const res = await startExecution(currentProject)
      setExecutionId(res.id)
      setStatus('queued')
      setLogs([`[${new Date().toLocaleTimeString()}] MasterAgent: Execution queued.`])
      
      const newWs = new WebSocket(`ws://localhost:8000/api/v1/ws/execution/${res.id}`)
      
      newWs.onmessage = (event) => {
        const data = JSON.parse(event.data)
        setLogs(prev => [...prev, `[${new Date().toLocaleTimeString()}] ${data.message}`])
        setStatus(data.status)
      }
      
      setWs(newWs)
    } catch (error) {
      setLogs(prev => [...prev, `[${new Date().toLocaleTimeString()}] Error: Could not start execution.`])
    }
  }

  useEffect(() => {
    return () => {
      if (ws) ws.close()
    }
  }, [ws])

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold tracking-tight">Agent Execution</h2>
        <button 
          onClick={handleStart}
          disabled={status === 'running' || !currentProject}
          className="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90 flex items-center disabled:opacity-50"
        >
          <PlayCircle className="mr-2 h-4 w-4" /> Start New Workflow
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Timeline */}
        <div className="lg:col-span-2 bg-card border border-border rounded-lg p-6">
          <h3 className="font-semibold text-lg mb-6">Execution Status: <span className="uppercase text-primary">{status}</span></h3>
          <div className="space-y-6 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-border before:to-transparent">
            {/* Step 1 */}
            <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
              <div className="flex items-center justify-center w-10 h-10 rounded-full border-2 border-primary bg-primary/10 text-primary shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2">
                <Clock className="h-5 w-5 animate-pulse" />
              </div>
              <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] bg-card border border-primary/50 p-4 rounded-lg shadow-sm">
                <div className="flex items-center justify-between mb-1">
                  <h4 className="font-bold text-foreground">LangGraph Orchestration</h4>
                  <span className="text-xs text-primary font-medium bg-primary/10 px-2 py-1 rounded">Active</span>
                </div>
                <p className="text-sm text-muted-foreground">Streaming real-time events via WebSocket...</p>
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
            {logs.map((log, idx) => (
              <p key={idx} className={log.includes('Error') || log.includes('failed') ? 'text-red-400' : (log.includes('finished') || log.includes('started') ? 'text-green-400' : '')}>{log}</p>
            ))}
            {status === 'running' && <p className="animate-pulse">_</p>}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Execution
