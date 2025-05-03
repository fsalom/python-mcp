from abc import ABC, abstractmethod

from domain.ai import ResponseAI


class AIServicePort(ABC):
    @abstractmethod
    def execute(self, session_id: str, query: str, context: str = None, system: str = None) -> ResponseAI:
        pass
