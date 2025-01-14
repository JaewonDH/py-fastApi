from fastapi import Depends
from app.db.database import get_db

from sqlalchemy import label
from sqlalchemy.orm import Session, selectinload, load_only, joinedload
from app.model.post_entity import Post
from app.model.user_entity import User
from app.core.exception.custom_exception import (
    ServiceException,
    ErrorCode,
    ErrorDetailMessage,
    NotFoundException,
    InvalidInputException,
)
import logging
from typing import Type, TypeVar, Any
from app.service.base_service import BaseService
from app.schema.post_schema import CreatePost, PostsResponse

logger = logging.getLogger("GroupService")

T = TypeVar("T")


class PostService(BaseService):
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session
        super().__init__(session)

    def create_post(self, create_post: CreatePost):
        try:
            post = Post(
                title=create_post.title,
                content=create_post.content,
                user_id=create_post.user_id,
            )
            self.session.add(post)
            self.session.commit()
            return post
        except InvalidInputException as e:
            raise e
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to create user: {e}")
            raise ServiceException(error_code=ErrorCode.UNEXPECTED_ERROR, detail=str(e))

    def get_posts(self, page: int = 1, page_size: int = 10, search: str | None = None):
        # joinedload: 하나의 JOIN 쿼리로 가져오므로 적은 데이터에서는 효율적. 그러나 데이터가 많을 경우 JOIN의 성능 저하 가능.
        # selectinload: 데이터가 많거나, N쪽 관계가 복잡할 때 적합. IN 쿼리로 데이터를 가져오므로 효율적.
        query = self.session.query(Post).options(
            selectinload(Post.user).load_only(
                User.id, User.name
            ),  # Specify columns from the related User entity
            load_only(
                Post.id, Post.title, Post.created_dt, Post.updated_dt
            ),  # Specify columns from the Post entity
        )

        if search:
            query = query.filter(Post.title.ilike(f"%{search}%"))

        total_count = query.count()
        posts = query.offset((page - 1) * page_size).limit(page_size).all()

        for post in posts:
            logger.info(post)

        return PostsResponse(
            total_count=total_count, page=page, page_size=page_size, posts=posts
        )

    def get_post(self, id: str):
        post = self.session.query(Post).filter(Post.id == id).first()
        return post
