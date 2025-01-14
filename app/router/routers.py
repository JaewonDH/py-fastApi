from fastapi import APIRouter
from app.router import (
    test_router,
    user_router,
    group_router,
    post_router,
    comment_router,
)

api_router = APIRouter()
api_router.include_router(user_router.router, prefix="/user", tags=["User"])
api_router.include_router(group_router.router, prefix="/gorup", tags=["Group"])
api_router.include_router(post_router.router, prefix="/post", tags=["Post"])
api_router.include_router(comment_router.router, prefix="/comment", tags=["Comment"])
api_router.include_router(test_router.router, prefix="/test", tags=["Test"])
