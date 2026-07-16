import os
import shutil
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.database import get_db
from app.models.domain import Upload
from app.schemas.domain import UploadResponse

router = APIRouter()

UPLOAD_DIR = "company_workspaces"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=UploadResponse)
async def upload_file(
    project_id: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    project_dir = os.path.join(UPLOAD_DIR, project_id)
    os.makedirs(project_dir, exist_ok=True)
    
    file_path = os.path.join(project_dir, file.filename)
    
    # Save the file to disk
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Store metadata in database
    upload_record = Upload(
        project_id=project_id,
        filename=file.filename,
        file_path=file_path,
        content_type=file.content_type,
        status="pending"
    )
    db.add(upload_record)
    await db.commit()
    await db.refresh(upload_record)
    
    return upload_record

@router.get("/", response_model=List[UploadResponse])
async def list_uploads(
    project_id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Upload).filter(Upload.project_id == project_id))
    return result.scalars().all()
