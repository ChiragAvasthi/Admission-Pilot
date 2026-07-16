from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.database import get_db, async_session_maker
from app.models.domain import Execution, Project
from app.schemas.domain import ExecutionCreate, ExecutionResponse
from app.agents.execution.manager import ExecutionManager
from app.api.v1.websockets.execution_ws import ws_manager
import asyncio
import uuid

router = APIRouter()

async def run_execution_workflow(execution_id: str, project_id: str):
    # This runs in the background
    async with async_session_maker() as db:
        execution = await db.get(Execution, execution_id)
        if not execution:
            return
            
        execution.status = "running"
        await db.commit()
        await ws_manager.broadcast_execution_update(execution_id, {"status": "running", "message": "Workflow started. Initializing Document Processing..."})
        
        try:
            # Here we would initialize the LangGraph execution manager from Phase 4
            # For integration, we simulate the MasterAgent orchestration
            # 1. Document parsing async
            # 2. Planning
            # 3. Agent execution
            
            await asyncio.sleep(2)
            await ws_manager.broadcast_execution_update(execution_id, {"status": "running", "message": "Document Intelligence Agent completed chunking and vectorization."})
            
            await asyncio.sleep(2)
            await ws_manager.broadcast_execution_update(execution_id, {"status": "running", "message": "Marketing Strategy Agent synthesizing past campaigns..."})
            
            await asyncio.sleep(2)
            await ws_manager.broadcast_execution_update(execution_id, {"status": "running", "message": "Report Generation Agent compiling final summary."})
            
            # Simulated completion
            execution.status = "completed"
            await db.commit()
            await ws_manager.broadcast_execution_update(execution_id, {"status": "completed", "message": "Workflow finished successfully."})
            
        except Exception as e:
            execution.status = "failed"
            execution.logs = [*execution.logs, {"error": str(e)}]
            await db.commit()
            await ws_manager.broadcast_execution_update(execution_id, {"status": "failed", "message": f"Execution failed: {str(e)}"})

@router.post("/", response_model=ExecutionResponse)
async def start_execution(
    exec_in: ExecutionCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    project = await db.get(Project, exec_in.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    execution = Execution(project_id=exec_in.project_id, status="queued")
    db.add(execution)
    await db.commit()
    await db.refresh(execution)
    
    # Start the async LangGraph workflow in the background
    background_tasks.add_task(run_execution_workflow, execution.id, project.id)
    
    return execution

@router.get("/{execution_id}", response_model=ExecutionResponse)
async def get_execution(
    execution_id: str,
    db: AsyncSession = Depends(get_db)
):
    execution = await db.get(Execution, execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    return execution
