from fastapi import Depends
from app.db.database import get_db
from sqlalchemy.orm import Session, selectinload, load_only, joinedload
from app.schema.comment_schema import CreateComment, CommentResponse, UserResponse
from app.model.comment_entity import Comment
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
from collections import defaultdict

logger = logging.getLogger("CommentService")

T = TypeVar("T")


class CommentService(BaseService):
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session
        super().__init__(session)

    def create(self, create_comment: CreateComment):
        try:
            comment = Comment(
                title=create_comment.title,
                content=create_comment.content,
                user_id=create_comment.user_id,
                post_id=create_comment.post_id,
                parent_id=create_comment.parent_id,
            )
            self.session.add(comment)
            self.session.commit()
            self.session.flush()
            return comment
        except InvalidInputException as e:
            raise e
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to create user: {e}")
            raise ServiceException(error_code=ErrorCode.UNEXPECTED_ERROR, detail=str(e))

    def get_comment_tree(self, parent_id=None):
        # 1. 모든 댓글과 사용자 정보를 한 번에 JOIN해서 가져옵니다.
        comments_query = (
            self.session.query(
                Comment.id,
                Comment.content,
                Comment.created_dt,
                Comment.updated_dt,
                Comment.parent_id,
                User.id.label("user_id"),
                User.name.label("user_name"),
            )
            .join(User)
            .filter(Comment.parent_id == parent_id)
            .all()
        )

        # 2. 댓글을 부모-자식 관계로 딕셔너리에 저장
        comments_dict = defaultdict(list)
        for comment in comments_query:
            comments_dict[comment.parent_id].append(comment)

        # 3. 댓글을 트리 구조로 재구성하는 함수
        def build_comment_tree(parent_id):
            comment_responses = []
            for comment in comments_dict[parent_id]:
                comment_response = CommentResponse(
                    id=str(comment.id),
                    content=comment.content,
                    user=UserResponse(id=str(comment.user_id), name=comment.user_name),
                    created_dt=comment.created_dt,
                    updated_dt=comment.updated_dt,
                    comments=build_comment_tree(comment.id),  # 자식 댓글 재귀 호출
                )
                comment_responses.append(comment_response)
            return comment_responses

        # 최상위 댓글부터 시작
        return build_comment_tree(parent_id) or []  # 빈 리스트 반환

    def get_comments(self):
        response = self.get_comment_tree()  # get_comment_tree 호출해서 댓글 가져오기
        return self.get_comment_tree()  # get_comment_tree 호출해서 댓글 가져오기

    def get_comment(self, id: str):
        comment = self.session.query(Comment).filter(Comment.id == id).first()
        return comment
