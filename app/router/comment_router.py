from fastapi import APIRouter, Depends, Query
from app.service.comment_service import CommentService
from app.schema.comment_schema import CreateComment, CommentResponse
import logging

router = APIRouter()
logger = logging.getLogger("comment_router")


@router.post("", summary="comment 추가")
def create(
    create_comment: CreateComment, service: CommentService = Depends(CommentService)
):
    return service.create(create_comment)


@router.get("", summary="comment 조회", response_model=CommentResponse)
def get_posts(
    page: int = Query(1, gt=0, description="페이지 번호 (1부터 시작)"),
    page_size: int = Query(10, gt=0, description="페이지 번호 (1부터 시작)"),
    search: str | None = Query(None, description="title 검색 가능)"),
    service: CommentService = Depends(CommentService),
):
    return service.get_comments()


# @router.get("/{id}", summary="comment 상세", response_model=PostResponseContent)
# def get_post(
#     id: str,
#     service: PostService = Depends(PostService),
# ):
#     return service.get_post(id)
