from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.db.database import get_db
from app.models.domain import Organization
from app.schemas.domain import OrganizationCreate, OrganizationResponse

router = APIRouter()

@router.post("/", response_model=OrganizationResponse)
async def create_organization(
    org_in: OrganizationCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Organization).filter(Organization.name == org_in.name))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Organization already exists")
    
    org = Organization(**org_in.dict())
    db.add(org)
    await db.commit()
    await db.refresh(org)
    return org

@router.get("/", response_model=List[OrganizationResponse])
async def list_organizations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Organization))
    return result.scalars().all()
