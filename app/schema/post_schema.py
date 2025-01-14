from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime


class BaseGroup(BaseModel):
    title: str
    content: str


class CreatePost(BaseGroup):
    user_id: str


class UpdatePost(CreatePost):
    id: str


class User(BaseModel):
    id: str
    name: str

    model_config = ConfigDict(from_attributes=True)


class PostResponse(BaseModel):
    id: str
    title: str
    created_dt: datetime
    updated_dt: datetime
    user: User

    model_config = ConfigDict(from_attributes=True)


class PostResponseContent(PostResponse):
    content: str

    model_config = ConfigDict(from_attributes=True)


class PostsResponse(BaseModel):
    total_count: int  # 전체 Count
    page: int  # 현재 페이지 번호
    page_size: int  # 페이지 당 사용자 수
    posts: List[PostResponse]  #  목록

    model_config = ConfigDict(from_attributes=True)
