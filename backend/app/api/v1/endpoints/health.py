from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.database import get_db
import httpx
import os

router = APIRouter()

@router.get("/")
async def health_check():
    """General API health check."""
    return {"status": "ok", "service": "admission-pilot-backend"}

@router.get("/live")
async def liveness_probe():
    """Liveness probe for Docker/Kubernetes to check if the app is responsive."""
    return {"status": "alive"}

@router.get("/ready")
async def readiness_probe(db: AsyncSession = Depends(get_db)):
    """
    Readiness probe to check if critical dependencies (DB, Ollama) are available.
    """
    dependencies = {
        "database": "unknown",
        "ollama": "unknown"
    }
    is_ready = True
    
    # Check Database
    try:
        await db.execute(select(1))
        dependencies["database"] = "ok"
    except Exception as e:
        dependencies["database"] = f"error: {str(e)}"
        is_ready = False

    # Check Ollama
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            res = await client.get(f"{ollama_url}/api/tags")
            if res.status_code == 200:
                dependencies["ollama"] = "ok"
            else:
                dependencies["ollama"] = f"error: {res.status_code}"
                is_ready = False
    except Exception as e:
        dependencies["ollama"] = f"error: {str(e)}"
        is_ready = False

    if not is_ready:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "not ready", "dependencies": dependencies}
        )

    return {"status": "ready", "dependencies": dependencies}
