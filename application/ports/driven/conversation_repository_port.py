from abc import ABC, abstractmethod
from typing import List

from domain.ai import Message


class ConversationRepositoryPort(ABC):
    """Puerto para almacenar y recuperar conversaciones"""

    @abstractmethod
    def save(self, session_id: str, message: Message) -> None:
        """Guarda un mensaje en la conversación"""
        pass

    @abstractmethod
    def get(self, session_id: str) -> List[Message]:
        """Obtiene todos los mensajes de una conversación"""
        pass