from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.dependencies import get_app_settings, get_job_store
from backend.api.router import api_router, root_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_app_settings()
    # Ensure directories exist
    settings.paths_output_dir.mkdir(parents=True, exist_ok=True)
    settings.paths_upload_dir.mkdir(parents=True, exist_ok=True)
    # Initialize database
    store = get_job_store()
    await store.init()
    yield


def create_app() -> FastAPI:
    settings = get_app_settings()
    app = FastAPI(
        title=settings.app_name,
        debug=settings.app_debug,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.server_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(root_router)
    app.include_router(api_router)

    return app


app = create_app()
