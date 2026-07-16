from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.db.database import get_db
from app.models.domain import Report
from app.schemas.domain import ReportResponse

router = APIRouter()

@router.get("/", response_model=List[ReportResponse])
async def list_reports(
    project_id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Report).filter(Report.project_id == project_id))
    return result.scalars().all()

@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: str,
    db: AsyncSession = Depends(get_db)
):
    report = await db.get(Report, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report
