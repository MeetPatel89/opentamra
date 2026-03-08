from fastapi import APIRouter

from backend.api.routes.health import router as health_router
from backend.api.routes.jobs import router as jobs_router
from backend.api.routes.reports import router as reports_router
from backend.api.routes.uploads import router as uploads_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(jobs_router)
api_router.include_router(reports_router)
api_router.include_router(uploads_router)

# Health is at root level, not under /api/v1
root_router = APIRouter()
root_router.include_router(health_router)
