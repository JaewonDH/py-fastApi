from fastapi import Depends
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.schema.group_schema import (
    CreateGroup,
    GroupsResponse,
    UpdateGroup,
    CreateGroupMemeber,
)
from app.model.group_entity import Group
from app.model.user_entity import User
from app.model.group_entity import GroupAdmin, Group, GroupMemberStatus, GroupMember
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

logger = logging.getLogger("GroupService")

T = TypeVar("T")


class GroupService(BaseService):
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session
        super().__init__(session)

    def create_group(self, create_group: CreateGroup):
        try:
            self._check_duplicate(
                Group,
                "name",
                create_group.name,
                ErrorDetailMessage.duplicate_group_name,
            )

            group = Group(name=create_group.name, description=create_group.description)

            self.session.add(group)
            self.session.flush()

            group_admin = GroupAdmin(user_id=create_group.user_id, group_id=group.id)
            self.session.add(group_admin)
            self.session.commit()
            return
        except InvalidInputException as e:
            raise e
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to create group: {e}")
            raise ServiceException(error_code=ErrorCode.UNEXPECTED_ERROR, detail=str(e))

    def update_group(self, update_group: UpdateGroup):
        group: Group = self._check_validate(
            Group,
            "id",
            update_group.id,
            ErrorDetailMessage.invalid_group,
        )

        self._check_duplicate(
            Group,
            "name",
            update_group.name,
            ErrorDetailMessage.duplicate_group_name,
        )

        try:
            group.name = update_group.name
            group.description = update_group.description
            self.session.flush()
            self.session.commit()
            return group
        except InvalidInputException as e:
            raise e
        except NotFoundException as e:
            raise e
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to create user: {e}")
            raise ServiceException(error_code=ErrorCode.UNEXPECTED_ERROR, detail=str(e))

    def get_groups(self, page: int = 1, page_size: int = 10, name: str | None = None):
        query = (
            self.session.query(
                GroupAdmin.group_id.label("id"),
                Group.name,
                Group.description,
                User.id.label("manager_id"),
                User.name.label("manager_name"),
                Group.created_dt,
                Group.updated_dt,
            )
            .join(User, User.id == GroupAdmin.user_id)
            .join(Group, Group.id == GroupAdmin.group_id)
        )

        if name:
            query = query.filter(User.name.ilike(f"%{name}%"))

        total_count = query.count()

        groups = query.offset((page - 1) * page_size).limit(page_size).all()

        return GroupsResponse(
            total_count=total_count, page=page, page_size=page_size, groups=groups
        )

    def create_group_member_status(self):
        count = (
            self.session.query(GroupMemberStatus)
            .filter(
                GroupMemberStatus.status_name.in_(
                    ["가입요청", "가입 반려", "가입 승인"]
                )
            )
            .count()
        )

        if count > 0:
            raise Exception
        try:
            status = [
                GroupMemberStatus(
                    status_name="가입 요청",
                    description="유저가 해당 그룹의 가입 요청한 상태",
                ),
                GroupMemberStatus(
                    status_name="가입 반려",
                    description="그룹의 관리자가 가입을 요청한 반려한 상태",
                ),
                GroupMemberStatus(
                    status_name="가입 승인",
                    description="그룹의 관리자가 가입을 승인한 상태",
                ),
            ]
            self.session.add_all(status)
            self.session.commit()
            return {"code": 200, "message": "상태추가 완료"}
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to create group: {e}")
            raise ServiceException(error_code=ErrorCode.UNEXPECTED_ERROR, detail=str(e))

    def create_group_member(self, create_group_member: CreateGroupMemeber):
        try:
            # self._check_duplicate(
            #     Group,
            #     "name",
            #     create_group.name,
            #     ErrorDetailMessage.duplicate_group_name,
            # )

            logger.error(f"create_group_member 1")

            status = (
                self.session.query(GroupMemberStatus)
                .filter(GroupMemberStatus.status_name.like("%요청%"))
                .first()
            )

            logger.error(f"create_group_member 2={status}")

            group_member = GroupMember(
                group_id=create_group_member.group_id,
                user_id=create_group_member.user_id,
                group_member_status_id=status.id,
            )

            self.session.add(group_member)
            self.session.flush()
            self.session.commit()
            return
        except InvalidInputException as e:
            raise e
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to create group: {e}")
            raise ServiceException(error_code=ErrorCode.UNEXPECTED_ERROR, detail=str(e))
