from fastapi import Depends
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.schema.user_schema import (
    CreateUser,
    PaginatedUserResponse,
    UpdateUser,
    DeleteUserSuccessResponse,
)
from app.model.user_entity import User
from app.core.exception.custom_exception import (
    InvalidInputException,
    ServiceException,
    ErrorCode,
    ErrorDetailMessage,
    NotFoundException,
)
import logging

logger = logging.getLogger("user_service")


class UserService:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def __validate_user(self, user: User):
        if not user:
            raise NotFoundException(
                detail=ErrorDetailMessage.invalid_user,
            )

    def __find_by_id(self, id: str) -> User:
        user = self.session.query(User).filter(User.id == id).first()
        self.__validate_user(user)
        return user

    def __check_duplicate_email(self, email: str) -> User:
        user = self.session.query(User).filter(User.email == email).first()
        if user:
            raise InvalidInputException(
                error_code=ErrorCode.INVALID_INPUT,
                detail=ErrorDetailMessage.duplicate_email,
            )

    def create_user(self, create_user: CreateUser):
        try:
            self.__check_duplicate_email(create_user.email)
            user = User(
                email=create_user.email,
                name=create_user.name,
                address=create_user.address,
                password=create_user.password,
            )
            self.session.add(user)
            self.session.commit()
            logger.info(f"!!!!!!!!!!! 2user: {user.id}")
            self.session.refresh(user)
            logger.info(f"!!!!!!!!!!!! 3user: {user.id}")
            return user
        except InvalidInputException as e:
            raise e
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to create user: {e}")
            raise ServiceException(error_code=ErrorCode.UNEXPECTED_ERROR, detail=str(e))

    def update_user(self, update_user: UpdateUser):
        user = user = self.__find_by_id(update_user.id)
        try:
            user.name = update_user.name
            user.email = update_user.email
            user.address = update_user.address
            self.session.commit()
            return user
        except NotFoundException as e:
            raise e
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to create user: {e}")
            raise ServiceException(error_code=ErrorCode.UNEXPECTED_ERROR, detail=str(e))

    def delete_user(self, id: str):
        try:
            user = self.__find_by_id(id)
            self.session.delete(user)
            self.session.commit()
            return DeleteUserSuccessResponse()
        except NotFoundException as e:
            raise e
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to create user: {e}")
            raise ServiceException(error_code=ErrorCode.UNEXPECTED_ERROR, detail=str(e))

    def detail_user(self, id):
        user = self.__find_by_id(id)
        return user

    def get_users(self, page: int = 1, page_size: int = 10, name: str | None = None):
        users_query = self.session.query(
            User.id,
            User.name,
            User.email,
            User.address,
            User.created_dt,
            User.updated_dt,
        )

        if name:
            users_query = users_query.filter(User.name.ilike(f"%{name}%"))

        total_count = users_query.count()
        users = users_query.offset((page - 1) * page_size).limit(page_size).all()

        return PaginatedUserResponse(
            total_count=total_count, page=page, page_size=page_size, users=users
        )

    def delete_all_user(self):
        try:
            self.session.query(User).delete()
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def use_test(self):
        result = self.session.query(User).all()
        for user in result:
            logger.info(f"count{len(user.posts)}")
        return result
