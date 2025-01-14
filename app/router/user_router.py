from fastapi import APIRouter, Depends, Query
from app.service.user_service import UserService
from app.schema.user_schema import (
    CreateUser,
    PaginatedUserResponse,
    UpdateUser,
    UserResponse,
)

import logging

router = APIRouter()
logger = logging.getLogger("user_router")


# @router.post("/", summary="사용자 추가", description="사용자생성")
@router.post("/", summary="사용자 추가")
def create_user(create_user: CreateUser, service: UserService = Depends(UserService)):
    return service.create_user(create_user)


@router.get("s/", summary="사용자 조회", response_model=PaginatedUserResponse)
def get_users(
    page: int = Query(1, gt=0, description="페이지 번호 (1부터 시작)"),
    page_size: int = Query(10, gt=0, description="페이지 번호 (1부터 시작)"),
    name: str | None = Query(None, description="사용자 이름 (부분 검색 가능)"),
    service: UserService = Depends(UserService),
):
    return service.get_users(page, page_size, name)


# @router.get("/{id}", summary="사용자 상세 조회", response_model=UserResponse)
# def get_user(id: str, service: UserService = Depends(UserService)):
#     return service.detail_user(id)


@router.put("/", summary="사용자 정보 수정", response_model=UserResponse)
def update_user(update_user: UpdateUser, service: UserService = Depends(UserService)):
    return service.update_user(update_user)


@router.delete("/{id}", summary="사용자 삭제")
def update_user(id: str, service: UserService = Depends(UserService)):
    return service.delete_user(id)


@router.delete("s/", summary="모든 사용자 삭제")
def update_user(service: UserService = Depends(UserService)):
    return service.delete_all_user()


@router.get("/test", summary="test")
def get_users(
    page: int = Query(1, gt=0, description="페이지 번호 (1부터 시작)"),
    page_size: int = Query(10, gt=0, description="페이지 번호 (1부터 시작)"),
    name: str | None = Query(None, description="사용자 이름 (부분 검색 가능)"),
    service: UserService = Depends(UserService),
):
    return service.use_test()
