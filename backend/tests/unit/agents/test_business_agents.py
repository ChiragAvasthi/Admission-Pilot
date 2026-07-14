import pytest
from unittest.mock import MagicMock
from app.agents.document.agent import DocumentIntelligenceAgent
from app.agents.website.agent import WebsiteAnalysisAgent
from app.agents.qa.agent import QualityAssuranceAgent
from app.parsers.agents import DocumentAnalysisResult, WebsiteAuditResult, QAResult
from app.agents.state.context import ContextManager
from app.agents.types import AgentStatus

@pytest.fixture
def mock_model_manager():
    manager = MagicMock()
    llm_mock = MagicMock()
    manager.get_active_model.return_value = llm_mock
    return manager

@pytest.fixture
def mock_knowledge_store():
    return MagicMock()

@pytest.fixture
def context_manager():
    return ContextManager(goal="Test goal")

def test_document_intelligence_agent(mock_model_manager, mock_knowledge_store, context_manager):
    # Setup mock LLM response
    mock_result = DocumentAnalysisResult(
        college_profile="Test Profile",
        courses_offered=["CS 101"],
        facilities=["Library"],
        placements="90%",
        vision="Vision",
        mission="Mission",
        past_campaigns=[],
        confidence_score=0.9
    )
    mock_model_manager.get_active_model().structured_invoke.return_value = mock_result
    
    agent = DocumentIntelligenceAgent(mock_model_manager, mock_knowledge_store)
    agent.initialize()
    
    task_input = {"document_content": "Test content"}
    result = agent.execute(task_input, context_manager)
    
    assert agent.status == AgentStatus.IDLE
    assert result.confidence_score == 0.9
    assert result.college_profile == "Test Profile"
    mock_knowledge_store.ingest_document.assert_called_once()

def test_qa_agent_requests_revision(mock_model_manager, context_manager):
    # Setup mock LLM response with low confidence to trigger revision
    mock_result = QAResult(
        is_consistent=False,
        missing_information=["budget"],
        conflicting_recommendations=[],
        business_feasibility="Low",
        confidence_score=0.6,
        needs_revision=False,
        feedback="Missing budget info."
    )
    mock_model_manager.get_active_model().structured_invoke.return_value = mock_result
    
    agent = QualityAssuranceAgent(mock_model_manager)
    agent.initialize()
    
    task_input = {"target_output": "Some bad output"}
    result = agent.execute(task_input, context_manager)
    
    # Assert QA Agent forces revision due to low confidence score
    assert result.needs_revision is True
    assert agent.status == AgentStatus.IDLE
