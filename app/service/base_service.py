from typing import Type, TypeVar, Any
from sqlalchemy.orm import Session
from app.core.exception.custom_exception import (
    InvalidInputException,
    ErrorCode,
    ErrorDetailMessage,
    NotFoundException,
)
import logging
from typing import Type, TypeVar, Any

T = TypeVar("T")

logger = logging.getLogger("BaseServic")


class BaseService:
    def __init__(self, session: Session):
        self.session = session

    def _find_by(self, entity: Type[T], field: str, value: Any):
        return (
            self.session.query(entity).filter(getattr(entity, field) == value).first()
        )

    def _check_duplicate(
        self, entity: Type[T], field: str, value: Any, detail: ErrorDetailMessage | str
    ):
        result = self._find_by(entity, field, value)
        if result:
            raise InvalidInputException(
                error_code=ErrorCode.INVALID_INPUT,
                detail=detail,
            )

    def _check_validate(
        self, entity: Type[T], field: str, value: Any, detail: ErrorDetailMessage | str
    ):
        result = self._find_by(entity, field, value)
        if not result:
            raise NotFoundException(
                detail=detail,
            )
        return result

    def _find_by_id(self, entity: Type[T], id: str):
        return self.session.query(entity).filter(entity.id == id).first()

    def _find_by_name(self, entity: Type[T], name: str):
        return self.session.query(entity).filter(entity.name == name).first()

    # def _check_duplicate_name(self, entity: Type[T], name: str):
    #     user = self.session.query(Group).filter(entity.name == name).first()
    #     if user:
    #         raise InvalidInputException(
    #             error_code=ErrorCode.INVALID_INPUT,
    #             detail=ErrorDetailMessage.duplicate_group_name,
    #         )

    # def _check_duplicate_name(self, name: str) -> User:
    #     user = self.session.query(Group).filter(Group.name == name).first()
    #     if user:
    #         raise InvalidInputException(
    #             error_code=ErrorCode.INVALID_INPUT,
    #             detail=ErrorDetailMessage.duplicate_group_name,
    #         )
