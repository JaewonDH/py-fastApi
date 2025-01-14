from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Optional, Any, Dict

SQLALCHEMY_DATABASE_URL: Optional[str] = None
DB_POOL_SIZE: int = 50
DB_POOL_MAX_OVERFLOW: int = 30
DB_POOL_RECYCLE: int = 14400

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL,
#     pool_size=DB_POOL_SIZE,
#     max_overflow=DB_POOL_MAX_OVERFLOW,
#     pool_recycle=DB_POOL_RECYCLE,
# )

# 데이터베이스 연결 설정 (예시: SQLite)
# engine = create_engine("sqlite:///test.db", echo=True)
# DATABASE_URL = "postgresql+psycopg2://admin:1234@localhost:5432/Sample"
DATABASE_URL = "sqlite:///test.db"
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
