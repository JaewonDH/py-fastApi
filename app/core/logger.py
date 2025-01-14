import os
import logging
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 환경 변수에서 실행 환경 가져오기
environment = os.getenv("ENVIRONMENT")


def setup_logging():
    # 전역 로깅 설정
    # logging.info(f"2 environment={environment}")
    print(f"1 Environment: {environment}")
    if environment == "DEV":
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logging.basicConfig(
        level=log_level,  # 로그 레벨 설정
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),  # 콘솔 출력
            logging.FileHandler("app.log", mode="a", encoding="utf-8"),  # 파일 출력
        ],
    )
