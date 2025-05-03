from abc import ABC, abstractmethod
from typing import List

from domain.ai import Message, ResponseAI


class LLMServicePort(ABC):
    """Puerto para interactuar con servicios de LLM externos"""

    @abstractmethod
    def query(self, messages: List[Message], tools_definitions: List[dict] = None) -> ResponseAI:
        """Genera una respuesta usando el LLM externo"""
        pass
