# AdmissionPilot - Phase 5: Frontend Application Implementation Plan

This document outlines the architecture and implementation strategy for building the modern enterprise dashboard (Phase 5). This phase will establish the complete React frontend stack, integrating with the backend APIs built in Phases 1-4.

## Proposed Changes

### 1. Project Initialization & Dependencies
- **Action**: Run `npm install` for all required dependencies and their types.
- **Action**: Initialize Tailwind CSS and configure `tailwind.config.ts`.
- **Action**: Set up global styles (`frontend/src/styles/globals.css`) with a sleek Light Theme.
- **Action**: Configure `vitest` for testing components and services.

### 2. Directory Structure Setup
Establish the strictly typed enterprise architecture under `frontend/src/`:
- `app/` (Global providers, core routing config)
- `components/` (Reusable UI elements: Buttons, Cards, Dialogs, Progress Bars)
- `features/` (Domain-specific components: Auth, Organizations, Projects, Execution, Uploads)
- `pages/` (Top-level route components)
- `layouts/` (Sidebar, TopNav, AppLayout)
- `hooks/` (Custom React hooks)
- `services/` (Axios API instances and endpoints)
- `store/` (Zustand stores)
- `types/` (TypeScript interfaces representing backend schemas)
- `routes/` (Route definitions)
- `context/`, `styles/`, `utils/`, `assets/`, `constants/`, `providers/`, `config/`

### 3. Core Infrastructure
- **Routing**: Set up `react-router-dom` with a central layout wrapping all dashboard pages.
- **API Client**: Configure an Axios instance with base URL (from `.env`), interceptors for error handling, and timeout configurations.
- **State Management**: Create a Zustand store (`useAppStore`). Configure a `QueryClient` provider for React Query.

### 4. Page Implementations
- **Dashboard**: High-level metrics using `recharts`, recent activity timelines, and quick action cards.
- **Organizations & Projects**: CRUD interfaces using `react-hook-form` and `zod` validation.
- **Uploads**: Drag-and-drop interface supporting various file types with a simulated progress bar using `react-dropzone`.
- **Agent Execution**: A dynamic timeline view tracking the LangGraph workflow, showing current task, agent confidence, and live logs.
- **Reports & Knowledge Base**: Rendering markdown outputs via `react-markdown`, with search and filtering capabilities.
- **Settings**: Application settings to configure Theme, API endpoint, Language, and Models.
- **Chat Panel**: A dedicated interface for communicating ONLY with the Master Agent, supporting streaming text, markdown, and typing indicators.
