from fastapi import APIRouter

from src.api import v2, v3


router = APIRouter()

router.include_router(v2.router, prefix="/v2")
router.include_router(v3.router, prefix="/v3")
