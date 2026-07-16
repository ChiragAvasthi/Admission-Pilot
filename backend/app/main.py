from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.db.database import engine

app = FastAPI(
    title="AdmissionPilot API",
    description="End-to-end API for Agentic AI Platform",
    version="1.0.0",
)

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

from fastapi import WebSocket, WebSocketDisconnect
from app.api.v1.websockets.execution_ws import ws_manager

@app.websocket("/api/v1/ws/execution/{execution_id}")
async def websocket_endpoint(websocket: WebSocket, execution_id: str):
    await ws_manager.connect(execution_id, websocket)
    try:
        while True:
            # Just keep the connection open to send updates
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(execution_id, websocket)

@app.on_event("startup")
async def startup():
    print("Application starting...")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
