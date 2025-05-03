from fastapi import FastAPI

from driving.api_rest.health.adapter import health_router
from driving.api_rest.v1.ai.adapter import ai_router


def add_routers(app: FastAPI):
    app.include_router(health_router, prefix='/api')
    # v1
    app.include_router(ai_router, prefix='/api/v1')
