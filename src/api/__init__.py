from fastapi import APIRouter

from src.api import v1, v2


router = APIRouter()

router.include_router(v1.router, prefix="/v1")
router.include_router(v2.router, prefix="/v2")
