from fastapi import APIRouter

from app.api.v1.endpoints import organizations, projects, uploads, execution, reports, health

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["Health Checks"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["Organizations"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
api_router.include_router(uploads.router, prefix="/uploads", tags=["Uploads"])
api_router.include_router(execution.router, prefix="/execution", tags=["Execution"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
