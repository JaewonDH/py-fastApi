from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import List
from datetime import datetime


class BaseGroup(BaseModel):
    name: str
    description: str


class CreateGroup(BaseGroup):
    user_id: str
    pass


class UpdateGroup(BaseGroup):
    id: str


class GroupResponse(UpdateGroup):
    id: str
    manager_id: str
    manager_name: str
    created_dt: datetime
    updated_dt: datetime
    model_config = ConfigDict(from_attributes=True)


class GroupsResponse(BaseModel):
    total_count: int
    page: int
    page_size: int
    groups: List[GroupResponse]

    model_config = ConfigDict(from_attributes=True)


class DeleteGroupSuccessResponse(BaseModel):
    code: int = 200
    message: str = "삭제완료"


class CreateGroupMemeber(BaseModel):
    group_id: str
    user_id: str
