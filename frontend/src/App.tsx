import { BrowserRouter, Routes, Route } from 'react-router-dom'
import AppLayout from '@/layouts/AppLayout'
import Dashboard from '@/pages/Dashboard'
import Organizations from '@/pages/Organizations'
import Projects from '@/pages/Projects'
import Uploads from '@/pages/Uploads'
import Execution from '@/pages/Execution'
import Reports from '@/pages/Reports'
import KnowledgeBase from '@/pages/KnowledgeBase'
import Settings from '@/pages/Settings'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AppLayout />}>
          <Route index element={<Dashboard />} />
          <Route path="organizations" element={<Organizations />} />
          <Route path="projects" element={<Projects />} />
          <Route path="uploads" element={<Uploads />} />
          <Route path="execution" element={<Execution />} />
          <Route path="reports" element={<Reports />} />
          <Route path="knowledge-base" element={<KnowledgeBase />} />
          <Route path="settings" element={<Settings />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
