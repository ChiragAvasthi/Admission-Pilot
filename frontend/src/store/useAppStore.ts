import { create } from 'zustand'

interface AppState {
  currentOrganization: string | null
  currentProject: string | null
  theme: 'light' | 'dark'
  setOrganization: (orgId: string) => void
  setProject: (projectId: string) => void
  setTheme: (theme: 'light' | 'dark') => void
}

export const useAppStore = create<AppState>((set) => ({
  currentOrganization: null,
  currentProject: null,
  theme: 'light',
  setOrganization: (orgId) => set({ currentOrganization: orgId }),
  setProject: (projectId) => set({ currentProject: projectId }),
  setTheme: (theme) => set({ theme }),
}))
