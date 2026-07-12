import pytest
from app.agents.state.context import Context, ContextManager
from app.agents.types import TaskStatus
from app.agents.workflow.task import TaskManager
from app.agents.registry.registry import AgentRegistry
from app.agents.events.dispatcher import EventDispatcher
from app.agents.events.models import TaskCreated

def test_context_manager_immutability():
    initial_context = Context(goal="Test goal")
    manager = ContextManager(initial_context)
    
    # Update context
    new_context = manager.update_context({"budget": 1000.0})
    
    assert new_context.budget == 1000.0
    assert new_context.goal == "Test goal"
    assert new_context is not initial_context # Ensure it returned a new instance

def test_task_manager():
    tm = TaskManager()
    task = tm.create_task("Test Task", "Description")
    
    assert task.status == TaskStatus.PENDING
    
    tm.update_status(task.id, TaskStatus.IN_PROGRESS)
    assert tm.get_task(task.id).status == TaskStatus.IN_PROGRESS
    
    tm.update_status(task.id, TaskStatus.COMPLETED)
    assert tm.get_task(task.id).status == TaskStatus.COMPLETED

def test_event_dispatcher():
    dispatcher = EventDispatcher()
    received_events = []
    
    def listener(event):
        received_events.append(event)
        
    dispatcher.subscribe(TaskCreated, listener)
    
    event = TaskCreated(task_id="123", task_name="Test Event")
    dispatcher.dispatch(event)
    
    assert len(received_events) == 1
    assert received_events[0].task_id == "123"
