# Admission Pilot - Frontend

This is the React + Vite + TypeScript frontend for Admission Pilot.

## Setup

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Environment Variables**
   Create a `.env` file based on your environment.
   ```bash
   VITE_API_URL=http://localhost:8000
   ```

## Running Locally

```bash
npm run dev
```
The application will be available at `http://localhost:5173` (or `3000` via Docker).

## Docker

To build and run standalone:
```bash
docker build -t admission-pilot-frontend .
docker run -p 3000:3000 admission-pilot-frontend
```

## Structure
- `src/components/`: Reusable UI components.
- `src/pages/`: Full page views for routing.
- `src/hooks/`: Custom React hooks.
- `src/services/`: API calls and business logic.
- `src/layouts/`: Page layout wrappers.
- `src/assets/`: Static assets (images, global CSS).
