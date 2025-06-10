from abc import ABC, abstractmethod
from typing import List

from domain.ai import ToolCall, ToolResponse


class ToolsServicePort(ABC):
    """Puerto para interactuar con el servicio de herramientas"""

    @abstractmethod
    def execute_tool(self, tool_call: ToolCall) -> ToolResponse:
        """Ejecuta una herramienta en el servicio remoto"""
        pass

    @abstractmethod
    def get_definitions_tools(self) -> List[dict]:
        """Obtiene la definición de todas las herramientas disponibles"""
        pass