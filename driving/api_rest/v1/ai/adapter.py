from uuid import uuid4

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from application.ports.driving.ai_service_port import AIServicePort
from driving.api_rest.v1.ai.models import AIResponse, AIRequest
from infrastructure.di.app.container import AppContainer

ai_router = APIRouter()


@ai_router.post("/query")
@inject
async def make_query(
    query: AIRequest,
    service: AIServicePort = Depends(Provide[AppContainer.ai_service])
):
    session_id = query.session_id or str(uuid4())
    result = await service.execute(session_id, query.text, query.context, query.system)

    return AIResponse(
        content=result.content,
        sources=result.sources,
        session_id=session_id
    )
