import os
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

from app.api.v1.api import api_router
from app.api.v1.websockets.execution_ws import ws_manager
from fastapi import WebSocket, WebSocketDisconnect

# Configure Logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/application.log")
    ]
)
logger = logging.getLogger("admission_pilot")

# Rate Limiter
limiter = Limiter(key_func=get_remote_address)

# File Size Limiter Middleware
class MaxFileSizeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.endswith("/uploads/"):
            content_length = request.headers.get("content-length")
            max_size_mb = int(os.getenv("MAX_UPLOAD_SIZE_MB", 50))
            if content_length and int(content_length) > max_size_mb * 1024 * 1024:
                return JSONResponse(status_code=413, content={"detail": f"File too large. Max size is {max_size_mb}MB."})
        return await call_next(request)

app = FastAPI(
    title="AdmissionPilot API",
    description="End-to-end API for Agentic AI Platform",
    version="1.0.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(MaxFileSizeMiddleware)

# CORS config
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.websocket("/api/v1/ws/execution/{execution_id}")
async def websocket_endpoint(websocket: WebSocket, execution_id: str):
    await ws_manager.connect(execution_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(execution_id, websocket)

@app.on_event("startup")
async def startup():
    logger.info("AdmissionPilot API started successfully.")
