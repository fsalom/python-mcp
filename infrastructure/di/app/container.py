import os

from dependency_injector import containers, providers

from driven.openai.adapter import OpenAIRepository
from driven.tools.adapter import RemoteToolsServiceAdapter
from driven.conversation.adapter import MemoryConversationRepository
from application.services.ai_service import AIService
from infrastructure.mcp.mcp_instance import mcp_server


class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["driving.api_rest.v1.ai.adapter"]
    )

    mcp_instance = providers.Object(mcp_server)

    llm_service = providers.Factory(OpenAIRepository,
                                    api_key=os.getenv("OPENAI_API_KEY"))
    tools_service = providers.Factory(RemoteToolsServiceAdapter,
                                      base_url=os.getenv("TOOLS_BASE_URL", "http://localhost:5000"))
    conversation_repository = providers.Factory(MemoryConversationRepository)

    ai_service = providers.Factory(
        AIService,
        llm_service=llm_service,
        tools_service=tools_service,
        conversation_repository=conversation_repository,
        mcp=mcp_instance
    )
