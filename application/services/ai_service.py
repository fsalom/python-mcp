import json
from openai import OpenAI
from domain.ai import ResponseAI

from application.ports.driven.conversation_repository_port import ConversationRepositoryPort
from application.ports.driving.ai_service_port import AIServicePort
from application.ports.driving.llm_service_port import LLMServicePort
from application.ports.driving.tools_service_port import ToolsServicePort


class AIService(AIServicePort):
    def __init__(
        self,
        llm_service: LLMServicePort,
        tools_service: ToolsServicePort,
        conversation_repository: ConversationRepositoryPort,
        mcp
    ):
        self.llm_service = llm_service
        self.tools_service = tools_service
        self.conversation_repository = conversation_repository
        self.mcp = mcp
        self.client = OpenAI()  # Usa OPENAI_API_KEY de entorno

    async def execute(self, session_id: str, query: str, context: str = None, system: str = None) -> ResponseAI:
        system_message = system or "Analiza cuidadosamente la consulta del usuario y prioriza el uso de las herramientas disponibles para responder. Usa las herramientas siempre que sea posible antes de dar una respuesta directa."

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": query}
        ]
        '''
        conversation = await self.conversation_repository.get_conversation(session_id)
        if conversation:
            # Añadir contexto histórico si existe
            messages = conversation.messages + messages
        '''
        # Mejora 2: Asegúrate de que las descripciones de las herramientas sean claras y específicas
        tools = []
        tools_map = await self.mcp.get_tools()

        for tool_name, tool in tools_map.items():
            tool_def = {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters
                }
            }
            tools.append(tool_def)

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            tools=tools,
            tool_choice="auto",  # Mantén auto, pero el mensaje de sistema orientará hacia el uso de tools
            temperature=0.2  # Temperatura más baja para ser más determinista
        )

        message = response.choices[0].message
        tool_calls = message.tool_calls if hasattr(message, "tool_calls") else None

        if tool_calls:
            # Procesar todas las llamadas a herramientas (puede haber múltiples)
            tool_responses = []

            for tool_call in tool_calls:
                tool_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                tool_call_id = tool_call.id

                # Ejecutar la función del tool desde MCP
                tool = tools_map[tool_name]
                try:
                    if tool.is_async:
                        result = await tool.fn(**args)
                    else:
                        result = tool.fn(**args)

                    tool_responses.append({
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "content": str(result)
                    })
                except Exception as e:
                    tool_responses.append({
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "content": f"Error al ejecutar la herramienta: {str(e)}"
                    })

            followup_messages = messages + [
                {"role": "assistant", "tool_calls": [tc.model_dump() for tc in tool_calls]},
                *tool_responses
            ]

            followup = self.client.chat.completions.create(
                model="gpt-4",
                messages=followup_messages
            )

            # Actualizar la conversación en el repositorio
            final_response = followup.choices[0].message.content
            '''
            if conversation:
                conversation.add_message({"role": "user", "content": query})
                conversation.add_message({"role": "assistant", "content": final_response})
                await self.conversation_repository.save_conversation(conversation)
            '''
            return ResponseAI(
                content=final_response,
                sources=[]
            )
        else:
            # Actualizar la conversación en el repositorio
            '''
            if conversation:
                conversation.add_message({"role": "user", "content": query})
                conversation.add_message({"role": "assistant", "content": message.content})
                await self.conversation_repository.save_conversation(conversation)
            '''
            return ResponseAI(
                content=message.content,
                sources=[]
            )