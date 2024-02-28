from fastapi import APIRouter

router = APIRouter()

from .data import router as data_router

router.include_router(data_router, prefix="/data", tags=["data"])