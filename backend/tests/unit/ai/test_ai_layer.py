import pytest
from app.parsers.structured import StructuredExecutionPlan, TaskPlan, ReasoningResult
from app.agents.types import Priority

def test_structured_execution_plan_validation():
    # Valid data
    valid_data = {
        "goal": "Test goal",
        "tasks": [
            {
                "name": "Task 1",
                "description": "Do something",
                "priority": "HIGH",
                "dependencies": []
            }
        ],
        "required_agents": ["RESEARCH"],
        "expected_output": "A report"
    }
    
    plan = StructuredExecutionPlan(**valid_data)
    assert plan.goal == "Test goal"
    assert len(plan.tasks) == 1
    assert plan.tasks[0].priority == Priority.HIGH

    # Invalid data should raise ValidationError
    invalid_data = {
        "goal": "Test goal",
        "tasks": "not a list",
        "required_agents": [],
        "expected_output": ""
    }
    with pytest.raises(Exception):
        StructuredExecutionPlan(**invalid_data)

def test_reasoning_result_validation():
    data = {
        "goal_understanding": "Understanding",
        "missing_information": ["Info 1"],
        "required_capabilities": ["RESEARCH"],
        "execution_strategy": "Step 1, Step 2",
        "confidence_score": 0.95
    }
    
    result = ReasoningResult(**data)
    assert result.confidence_score == 0.95
    assert len(result.missing_information) == 1
