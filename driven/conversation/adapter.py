from typing import List

from application.ports.driven.conversation_repository_port import ConversationRepositoryPort
from domain.ai import Message


class MemoryConversationRepository(ConversationRepositoryPort):
    """Implementación en memoria del repositorio de conversaciones"""

    def __init__(self):
        self.conversations = {}  # session_id -> List[Message]

    def save(self, session_id: str, message: Message) -> None:
        """Guarda un mensaje en la conversación"""
        if session_id not in self.conversations:
            self.conversations[session_id] = []

        self.conversations[session_id].append(message)

    def get(self, session_id: str) -> List[Message]:
        """Obtiene todos los mensajes de una conversación"""
        return self.conversations.get(session_id, [])
