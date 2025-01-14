from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.db.database import Base
from app.core.util import gen_uuid_v4
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"

    id = Column(String(64), nullable=False, primary_key=True, default=gen_uuid_v4)
    email = Column(String(64), nullable=False)
    name = Column(String(64), nullable=False)
    address = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)
    created_dt = Column(
        DateTime(timezone=True), server_default=func.now(), default=func.now()
    )
    updated_dt = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=func.now(),
        onupdate=func.now(),
    )

    # backref 사용전략  1:N 관계에서 1에 해당하는 쪽에 backref 사용해서 relationship 정의하면 N에 해당하는 곳에서는
    # relationship 정의하지 않아도 Post에서 Entity를 호출이 가능 아니면 back_populates 양쪽 Entity에 모두 사용해서 사용 가능

    # 1: N 관계 User 한행이 Post의 여러행에 등록이 가능
    posts = relationship("Post", backref="user")
    # 1: N 관계 User 한행이 Comment의 여러행에 등록이 가능
    comments = relationship("Comment", backref="user")
    # 1: N 관계 User 한행이 GroupMember의 여러행에 등록이 가능
    group_members = relationship("GroupMember", backref="user")
