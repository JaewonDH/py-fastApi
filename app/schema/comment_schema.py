from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime


class BaseGroup(BaseModel):
    title: str
    content: str


class CreateComment(BaseGroup):
    post_id: str
    user_id: str
    parent_id: str | None = None


# class UpdateGroup(BaseGroup):
#     id: str


class UserResponse(BaseModel):
    id: str
    name: str
    model_config = ConfigDict(from_attributes=True)


class CommentResponse(BaseModel):
    id: str
    content: str
    user: UserResponse
    created_dt: datetime
    updated_dt: datetime
    comments: List["CommentResponse"] | None = None
    model_config = ConfigDict(from_attributes=True)


# class DeleteGroupSuccessResponse(BaseModel):
#     code: int = 200
#     message: str = "삭제완료"


# class CreateGroupMemeber(BaseModel):
#     group_id: str
#     user_id: str
