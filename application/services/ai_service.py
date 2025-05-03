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
        messages = [{"role": "user", "content": query}]

        tools = [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters
                }
            }
            for tool in (await self.mcp.get_tools()).values()
        ]

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message
        tool_calls = message.tool_calls if hasattr(message, "tool_calls") else None

        if tool_calls:
            tool_call = tool_calls[0]
            tool_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            tool_call_id = tool_call.id  # ✅ este viene de OpenAI, no de MCP

            # Ejecutar la función del tool desde MCP
            tools_map = await self.mcp.get_tools()
            tool = tools_map[tool_name]
            if tool.is_async:
                result = await tool.fn(**args)
            else:
                result = tool.fn(**args)

            # Segunda llamada a GPT con la respuesta del tool
            followup = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": query},
                    {"role": "assistant", "tool_calls": [tool_call.model_dump()]},
                    {
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "content": str(result)
                    }
                ]
            )

            return ResponseAI(
                content=followup.choices[0].message.content,
                sources=[]
            )

        return ResponseAI(
            content=message.content,
            sources=[]
        )