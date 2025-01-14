from fastapi import APIRouter, Depends, Query
from app.service.post_service import PostService
from app.schema.post_schema import CreatePost, PostsResponse, PostResponseContent
import logging

router = APIRouter()
logger = logging.getLogger("post_router")


@router.post("", summary="Post 등록")
def create(create_post: CreatePost, service: PostService = Depends(PostService)):
    return service.create_post(create_post)


@router.get("", summary="Post 조회", response_model=PostsResponse)
def get_posts(
    page: int = Query(1, gt=0, description="페이지 번호 (1부터 시작)"),
    page_size: int = Query(10, gt=0, description="페이지 번호 (1부터 시작)"),
    search: str | None = Query(None, description="title 검색 가능)"),
    service: PostService = Depends(PostService),
):
    return service.get_posts(page, page_size, search)


@router.get("/{id}", summary="Post 상세", response_model=PostResponseContent)
def get_post(
    id: str,
    service: PostService = Depends(PostService),
):
    return service.get_post(id)
