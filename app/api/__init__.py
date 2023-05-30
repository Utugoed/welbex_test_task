from fastapi import APIRouter

from app.api.cargos import cargos_router
from app.api.health import health_router
from app.api.vehicles import vehicles_router


api_router = APIRouter()

api_router.include_router(cargos_router, prefix="/cargos")
api_router.include_router(health_router, prefix="/health-check")
api_router.include_router(vehicles_router, prefix="/vehicles")
