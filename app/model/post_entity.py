from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, TEXT
from sqlalchemy.sql import func
from app.db.database import Base
from app.core.util import gen_uuid_v4
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "post"

    id = Column(String(64), nullable=False, primary_key=True, default=gen_uuid_v4)
    title = Column(
        String(64),
        nullable=False,
    )
    content = Column(TEXT, nullable=False)
    user_id = Column(String(64), ForeignKey("user.id"), nullable=False)
    created_dt = Column(
        DateTime(timezone=True), server_default=func.now(), default=func.now()
    )
    updated_dt = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=func.now(),
        onupdate=func.now(),
    )

    # 1: N 관계 Post 한행이 Comment의 여러행에 등록이 가능
    comments = relationship("Comment", backref="post")
