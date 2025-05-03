import json
from typing import List

import requests

from application.ports.driving.llm_service_port import LLMServicePort
from domain.ai import Message, ResponseAI


class OpenAIRepository(LLMServicePort):
    """Adaptador para el servicio de OpenAI"""
    def __init__(self, api_key: str, modelo: str = "gpt-4"):
        self.api_key = api_key
        self.modelo = modelo
        self.base_url = "https://api.openai.com/v1/chat/completions"

    def query(self, messages: List[Message], tools_definitions: List[dict] = None) -> ResponseAI:
        """Implementación del método del puerto usando OpenAI API"""

        # Transformar mensajes al formato de OpenAI
        openai_messages = []
        for msg in messages:
            openai_messages.append({
                "role": msg.role,
                "content": msg.content
            })

        # Preparar payload para la API
        payload = {
            "model": self.modelo,
            "messages": openai_messages,
        }

        # Añadir definiciones de herramientas si existen
        if tools_definitions:
            # Convertir definiciones de herramientas al formato OpenAI
            openai_tools = []
            for tool in tools_definitions:
                openai_tool = {
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool["description"],
                        "parameters": {
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                    }
                }

                # Convertir parámetros
                for param_name, param_info in tool["parameters"].items():
                    openai_tool["function"]["parameters"]["properties"][param_name] = {
                        "type": param_info["type"].lower(),
                        "description": param_info.get("description", "")
                    }

                    if param_info.get("required", False):
                        openai_tool["function"]["parameters"]["required"].append(param_name)

                openai_tools.append(openai_tool)

            payload["tools"] = openai_tools
            payload["tool_choice"] = "auto"

        # Realizar llamada a la API
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            result = response.json()

            # Extraer contenido y metadatos
            assistant_message = result["choices"][0]["message"]
            content = assistant_message.get("content", "")

            # Procesar tool calls si existen
            metadatos = {}
            if "tool_calls" in assistant_message:
                metadatos["tool_calls"] = []
                for tool_call in assistant_message["tool_calls"]:
                    if tool_call["type"] == "function":
                        function_call = tool_call["function"]
                        try:
                            arguments = json.loads(function_call["arguments"])
                        except json.JSONDecodeError:
                            arguments = {"error": "Invalid JSON in arguments"}

                        metadatos["tool_calls"].append({
                            "name": function_call["name"],
                            "arguments": arguments
                        })

            return ResponseAI(
                content=content or "No se pudo generar una respuesta.",
                metadata=metadatos
            )

        except Exception as e:
            return ResponseAI(
                content=f"Error al comunicarse con OpenAI: {str(e)}",
                metadata={"error": str(e)}
            )