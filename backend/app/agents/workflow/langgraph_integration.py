import logging
from typing import Dict, Any, Literal
from langgraph.graph import StateGraph, END
from app.agents.types import Capability

logger = logging.getLogger(__name__)

class GraphState(Dict[str, Any]):
    """Represents the state passed between LangGraph nodes."""
    pass

class LangGraphWorkflow:
    def __init__(self, master_agent, agent_registry):
        self.master_agent = master_agent
        self.agent_registry = agent_registry
        self.graph = self._build_graph()

    def _build_graph(self):
        """
        Constructs the LangGraph StateGraph connecting orchestration and agents dynamically.
        """
        workflow = StateGraph(GraphState)
        
        # Core Orchestration Nodes
        workflow.add_node("planner", self._node_planner)
        workflow.add_node("orchestrator", self._node_orchestrator)
        workflow.add_node("qa", self._node_qa)
        workflow.add_node("report", self._node_report)
        
        # Business Agent Nodes
        workflow.add_node("document_agent", self._node_agent_runner(Capability.DOCUMENT_ANALYSIS))
        workflow.add_node("website_agent", self._node_agent_runner(Capability.WEBSITE_ANALYSIS))
        workflow.add_node("competitor_agent", self._node_agent_runner(Capability.COMPETITOR_INTELLIGENCE))
        workflow.add_node("marketing_agent", self._node_agent_runner(Capability.MARKETING_STRATEGY))
        workflow.add_node("seo_agent", self._node_agent_runner(Capability.SEO_STRATEGY))

        # Build Edges
        workflow.set_entry_point("planner")
        workflow.add_edge("planner", "orchestrator")
        
        # Conditional Routing from Orchestrator
        workflow.add_conditional_edges(
            "orchestrator",
            self._route_tasks,
            {
                "document_agent": "document_agent",
                "website_agent": "website_agent",
                "competitor_agent": "competitor_agent",
                "marketing_agent": "marketing_agent",
                "seo_agent": "seo_agent",
                "qa": "qa"
            }
        )
        
        # Return to orchestrator after an agent runs
        for agent_node in ["document_agent", "website_agent", "competitor_agent", "marketing_agent", "seo_agent"]:
            workflow.add_edge(agent_node, "orchestrator")
            
        workflow.add_edge("qa", "report")
        workflow.add_edge("report", END)
        
        return workflow.compile()

    def _node_planner(self, state: GraphState) -> GraphState:
        logger.info("LangGraph: Planning node executed")
        # Planner logic here...
        state["next_agent"] = "document_agent" # Mock initial
        return state

    def _node_orchestrator(self, state: GraphState) -> GraphState:
        logger.info("LangGraph: Orchestrator node executed")
        # In reality, the MasterAgent checks the WorkflowEngine/TaskManager 
        # to determine the next task and updates state["next_agent"].
        # Mocking progression:
        if state.get("next_agent") == "document_agent":
            state["next_agent"] = "website_agent"
            state["route"] = "document_agent"
        elif state.get("next_agent") == "website_agent":
            state["next_agent"] = "qa"
            state["route"] = "website_agent"
        else:
            state["route"] = "qa"
        return state
        
    def _route_tasks(self, state: GraphState) -> str:
        route = state.get("route", "qa")
        logger.info(f"LangGraph routing to: {route}")
        return route

    def _node_agent_runner(self, capability: Capability):
        def _runner(state: GraphState) -> GraphState:
            logger.info(f"LangGraph: Executing agent for capability {capability.value}")
            agents = self.agent_registry.get_agents_by_capability(capability)
            if agents:
                logger.info(f"Using agent: {agents[0].name}")
            return state
        return _runner

    def _node_qa(self, state: GraphState) -> GraphState:
        logger.info("LangGraph: QA node executed")
        return state

    def _node_report(self, state: GraphState) -> GraphState:
        logger.info("LangGraph: Report node executed")
        return state
