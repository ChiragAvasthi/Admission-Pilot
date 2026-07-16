from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class OrganizationBase(BaseModel):
    name: str
    description: Optional[str] = None

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationResponse(OrganizationBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    organization_id: str
    name: str
    description: Optional[str] = None
    website_url: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UploadResponse(BaseModel):
    id: str
    project_id: str
    filename: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ExecutionCreate(BaseModel):
    project_id: str

class ExecutionResponse(BaseModel):
    id: str
    project_id: str
    status: str
    progress: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ReportResponse(BaseModel):
    id: str
    execution_id: str
    project_id: str
    title: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
