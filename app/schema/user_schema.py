from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime

# 회원(Member): 회원 ID, 비밀번호, 이름, 이메일, 주소 등 회원 정보를 저장합니다.

# orm_mode->  ConfigDict(from_attributes=True)  v2.0에서는  ConfigDict(from_attributes=True)  사용해야 함.


class BaseUser(BaseModel):
    email: str
    name: str
    address: str


class CreateUser(BaseUser):
    password: str


class UpdateUser(BaseUser):
    id: str


class UserResponse(BaseUser):
    id: str
    created_dt: datetime
    updated_dt: datetime

    model_config = ConfigDict(from_attributes=True)


class PaginatedUserResponse(BaseModel):
    total_count: int  # 전체 사용자 수
    page: int  # 현재 페이지 번호
    page_size: int  # 페이지 당 사용자 수
    users: List[UserResponse]  # 사용자 목록

    model_config = ConfigDict(from_attributes=True)


class DeleteUserSuccessResponse(BaseModel):
    code: int = 200
    message: str = "삭제완료"
