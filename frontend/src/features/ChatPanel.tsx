import React, { useState } from 'react'
import { Send, Bot, User, Sparkles } from 'lucide-react'

// Mock initial history
const initialMessages = [
  { id: 1, role: 'agent', text: 'Hello! I am the Master Agent. How can I assist you with AdmissionPilot today?' }
]

const ChatPanel = () => {
  const [messages, setMessages] = useState(initialMessages)
  const [input, setInput] = useState('')

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    setMessages([...messages, { id: Date.now(), role: 'user', text: input }])
    setInput('')
    
    // Mock response
    setTimeout(() => {
      setMessages(prev => [...prev, { 
        id: Date.now(), 
        role: 'agent', 
        text: 'I am orchestrating the required agents to fulfill your request. I will notify you when the execution plan is ready.' 
      }])
    }, 1000)
  }

  return (
    <div className="w-96 bg-card border-l border-border h-full flex flex-col hidden xl:flex">
      {/* Header */}
      <div className="p-4 border-b border-border flex items-center space-x-2 bg-secondary/50">
        <Sparkles className="h-5 w-5 text-primary" />
        <h3 className="font-semibold text-sm">Master Agent</h3>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`flex items-start max-w-[85%] space-x-2 ${msg.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${msg.role === 'user' ? 'bg-slate-200' : 'bg-primary/10 text-primary'}`}>
                {msg.role === 'user' ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
              </div>
              <div className={`p-3 rounded-lg text-sm ${msg.role === 'user' ? 'bg-primary text-primary-foreground' : 'bg-secondary text-secondary-foreground'}`}>
                {msg.text}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Input */}
      <div className="p-4 border-t border-border bg-card">
        <form onSubmit={handleSend} className="relative">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask Master Agent..."
            className="w-full pl-3 pr-10 py-2 border border-border rounded-lg text-sm bg-background focus:outline-none focus:ring-1 focus:ring-primary"
          />
          <button 
            type="submit" 
            className="absolute right-2 top-1/2 -translate-y-1/2 p-1 rounded-md text-primary hover:bg-primary/10 transition-colors"
            disabled={!input.trim()}
          >
            <Send className="h-4 w-4" />
          </button>
        </form>
        <div className="flex gap-2 mt-3 overflow-x-auto pb-1 scrollbar-hide">
          {['Analyze competitor', 'Generate report', 'Audit website'].map(suggestion => (
            <button key={suggestion} type="button" className="shrink-0 text-xs px-2 py-1 bg-secondary rounded-md hover:bg-secondary/80 whitespace-nowrap">
              {suggestion}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

export default ChatPanel
