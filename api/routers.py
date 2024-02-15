from fastapi import APIRouter

from api.v1 import user_endpoint

router = APIRouter()

# include/register all the end_points
router.include_router(router=user_endpoint.router, tags=["User"], prefix="/users")
