from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Enum
from sqlalchemy.sql import func
from app.db.database import Base
from app.core.util import gen_uuid_v4
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum


# 그룹
class Group(Base):
    __tablename__ = "group"

    id = Column(String(64), nullable=False, primary_key=True, default=gen_uuid_v4)
    name = Column(String(64), nullable=False, unique=True)
    description = Column(String(100), nullable=False)
    created_dt = Column(
        DateTime(timezone=True), server_default=func.now(), default=func.now()
    )
    updated_dt = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=func.now(),
        onupdate=func.now(),
    )

    # group_members = relationship("GroupMember", back_populates="group")
    # group_admins = relationship("GroupAdmin", back_populates="group")


# 그룹 관리자  복합 키
class GroupAdmin(Base):
    __tablename__ = "group_admin"
    __table_args__ = (
        PrimaryKeyConstraint("user_id", "group_id", name="group_admin_pk"),
    )

    user_id = Column(String(64), ForeignKey("user.id"), nullable=False)
    group_id = Column(String(64), ForeignKey("group.id"), nullable=False)
    assigned_at = Column(
        DateTime(timezone=True), server_default=func.now(), default=func.now()
    )
    updated_dt = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=func.now(),
        onupdate=func.now(),
    )


class GroupMemberStatus(PyEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    SUSPENDED = "suspended"


# 그룹에 속한 사용자
class GroupMember(Base):
    __tablename__ = "group_member"
    __table_args__ = (
        PrimaryKeyConstraint("user_id", "group_id", name="group_member_pk"),
    )
    user_id = Column(String(64), ForeignKey("user.id"), nullable=False)
    group_id = Column(String(64), ForeignKey("group.id"), nullable=False)
    group_member_status = Column(Enum(GroupMemberStatus), nullable=False)
    join_dt = Column(
        DateTime(timezone=True), server_default=func.now(), default=func.now()
    )
    updated_dt = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=func.now(),
        onupdate=func.now(),
    )
