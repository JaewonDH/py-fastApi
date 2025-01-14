from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.router.routers import api_router
from app.core.logger import setup_logging
from app.core.exception.custom_exception import set_error_handlers
from app.core.middleware.request_logger_middleware import RequestLoggingMiddleware
from app.db.database import init_db
import logging

setup_logging()  # 로그 설정

logger = logging.getLogger("main")  # 현재 모듈 이름으로 로거 생성


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작할 때
    logger.info("startup_event")
    init_db()
    yield
    # 종료할 때
    logger.info("shutdown_event")


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 허용할 도메인 목록
    allow_credentials=True,
    allow_methods=["*"],  # 허용할 HTTP 메소드
    allow_headers=["*"],  # 허용할 HTTP 헤더
)

set_error_handlers(app)  # Custom Exception 등록

app.include_router(api_router, prefix="/api")


# app.add_middleware(
#     RequestLoggingMiddleware
# )  # 라우터 호출전에 호출 되는 Middleware로 라우터 호출 전에 사전 처리 가능
