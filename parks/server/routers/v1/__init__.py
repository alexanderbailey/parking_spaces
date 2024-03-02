from fastapi import APIRouter

router = APIRouter()

from .data import router as data_router

router.include_router(data_router, prefix="/data", tags=["data"])

from .carpark import router as carpark_router

router.include_router(carpark_router, prefix="/carpark", tags=["carpark"])

from .spaces import router as spaces_router

router.include_router(spaces_router, prefix="/spaces", tags=["spaces"])