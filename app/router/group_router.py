from fastapi import APIRouter, Depends, Query
from app.service.group_service import GroupService
from app.schema.group_schema import (
    CreateGroup,
    GroupsResponse,
    UpdateGroup,
    CreateGroupMemeber,
)
import logging

router = APIRouter()
logger = logging.getLogger("group_router")


@router.post("", summary="그룹 추가")
def create_group(group: CreateGroup, service: GroupService = Depends(GroupService)):
    return service.create_group(group)


@router.get("s", summary="그룹 조회", response_model=GroupsResponse)
def get_users(
    page: int = Query(1, gt=0, description="페이지 번호 (1부터 시작)"),
    page_size: int = Query(10, gt=0, description="페이지 번호 (1부터 시작)"),
    name: str | None = Query(None, description="그룹 이름 (부분 검색 가능)"),
    service: GroupService = Depends(GroupService),
):
    return service.get_groups(page, page_size, name)


@router.put("", summary="그룹 정보 수정")
def update_group(
    update_group: UpdateGroup, service: GroupService = Depends(GroupService)
):
    return service.update_group(update_group)


@router.post("/member/status", summary="그룹 등록 상태 추가")
def create_group_member_status(service: GroupService = Depends(GroupService)):
    return service.create_group_member_status()


@router.post("/member", summary="그룹 회원 추가")
def create_group_member(
    create_group_member: CreateGroupMemeber,
    service: GroupService = Depends(GroupService),
):
    return service.create_group_member(create_group_member)


# @router.delete("/{id}", summary="사용자 삭제")
# def update_user(id: UUID, service: UserService = Depends(UserService)):
#     return service.delete_user(id)


# @router.delete("s/", summary="모든 사용자 삭제")
# def update_user(service: UserService = Depends(UserService)):
#     return service.delete_all_user()
