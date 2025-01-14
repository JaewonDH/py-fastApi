from sqlalchemy import Column, String, DateTime, ForeignKey, TEXT
from sqlalchemy.sql import func
from app.db.database import Base
from app.core.util import gen_uuid_v4


class Comment(Base):
    __tablename__ = "comment"

    id = Column(String(64), nullable=False, primary_key=True, default=gen_uuid_v4)
    parent_id = Column(String(64), ForeignKey("comment.id"), nullable=True)
    post_id = Column(String(64), ForeignKey("post.id"), nullable=False)
    user_id = Column(String(64), ForeignKey("user.id"), nullable=False)
    title = Column(String(64), nullable=False, unique=True)
    content = Column(TEXT, nullable=False)
    created_dt = Column(
        DateTime(timezone=True), server_default=func.now(), default=func.now()
    )
    updated_dt = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=func.now(),
        onupdate=func.now(),
    )

    
