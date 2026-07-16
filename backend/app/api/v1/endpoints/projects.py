from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.db.database import get_db
from app.models.domain import Project
from app.schemas.domain import ProjectCreate, ProjectResponse

router = APIRouter()

@router.post("/", response_model=ProjectResponse)
async def create_project(
    project_in: ProjectCreate,
    db: AsyncSession = Depends(get_db)
):
    project = Project(**project_in.dict())
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project

@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    organization_id: str = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(Project)
    if organization_id:
        query = query.filter(Project.organization_id == organization_id)
    result = await db.execute(query)
    return result.scalars().all()
