import logging
from typing import Dict, List, Optional, Type
from app.agents.base.agent import BaseAgent
from app.agents.events.dispatcher import EventDispatcher
from app.agents.events.models import AgentRegistered

logger = logging.getLogger(__name__)

class AgentRegistry:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AgentRegistry, cls).__new__(cls)
            cls._instance._agents = {}
            cls._instance._event_dispatcher = None
        return cls._instance

    def set_event_dispatcher(self, dispatcher: EventDispatcher):
        self._event_dispatcher = dispatcher

    def register_agent(self, agent: BaseAgent) -> None:
        if agent.id in self._agents:
            logger.warning(f"Agent {agent.id} is already registered. Overwriting.")
        self._agents[agent.id] = agent
        logger.info(f"Registered agent {agent.name} ({agent.id})")
        
        if self._event_dispatcher:
            self._event_dispatcher.dispatch(AgentRegistered(
                agent_id=agent.id,
                agent_name=agent.name,
                capabilities=agent.capabilities
            ))

    def unregister_agent(self, agent_id: str) -> None:
        if agent_id in self._agents:
            del self._agents[agent_id]
            logger.info(f"Unregistered agent {agent_id}")

    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        return self._agents.get(agent_id)

    def get_available_agents(self) -> List[BaseAgent]:
        return [agent for agent in self._agents.values() if agent.health_check()]

    def filter_by_capability(self, capability: str) -> List[BaseAgent]:
        return [agent for agent in self.get_available_agents() if capability in agent.capabilities]

    def find_best_matching_agent(self, required_capabilities: List[str]) -> Optional[BaseAgent]:
        """
        Finds an agent that has the highest overlap with required capabilities.
        In a real implementation, this might involve an LLM routing call or complex heuristics.
        """
        best_agent = None
        max_overlap = 0
        for agent in self.get_available_agents():
            overlap = len(set(required_capabilities).intersection(set(agent.capabilities)))
            if overlap > max_overlap:
                max_overlap = overlap
                best_agent = agent
        return best_agent
