import asyncio
import logging
from typing import Callable, Dict, List, Type
from app.agents.events.models import BaseEvent

logger = logging.getLogger(__name__)

class EventDispatcher:
    def __init__(self):
        self._listeners: Dict[Type[BaseEvent], List[Callable[[BaseEvent], None]]] = {}

    def subscribe(self, event_type: Type[BaseEvent], listener: Callable[[BaseEvent], None]) -> None:
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)
        logger.debug(f"Subscribed {listener.__name__} to {event_type.__name__}")

    def unsubscribe(self, event_type: Type[BaseEvent], listener: Callable[[BaseEvent], None]) -> None:
        if event_type in self._listeners and listener in self._listeners[event_type]:
            self._listeners[event_type].remove(listener)
            logger.debug(f"Unsubscribed {listener.__name__} from {event_type.__name__}")

    def dispatch(self, event: BaseEvent) -> None:
        """
        Dispatches an event synchronously to all registered listeners.
        """
        event_type = type(event)
        if event_type in self._listeners:
            for listener in self._listeners[event_type]:
                try:
                    listener(event)
                except Exception as e:
                    logger.error(f"Error executing listener {listener.__name__} for event {event_type.__name__}: {e}")
        else:
            logger.debug(f"No listeners registered for event {event_type.__name__}")
