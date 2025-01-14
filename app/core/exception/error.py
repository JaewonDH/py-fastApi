from enum import Enum


class ErrorDetailMessage(Enum):
    invalid_input_data = "입력이 잘 못 되었습니다. 입력한 정보를 다시 확인해주세요"
    duplicate_email = "이메일 주소가 중복 됩니다"
    invalid_email = "조회 할 수 없는 이메일 입니다."
    invalid_user = "조회 할 수 없는 사용자 입니다."
    invalid_group = "조회 할 수 없는 그룹 입니다."
    server_error = "Server Error"
    duplicate_group_name = "그룹 이름이 중복됩니다."


class ErrorCode(Enum):
    # 400 Bad Request
    NOT_DEFINED = 1000
    INVALID_INPUT = 1102

    # 401 Unauthorized
    NO_TOKEN = 2001
    # 토큰이 만료된 경우 -> http status code는 489로 처리
    TOKEN_EXPIRED = 2002
    INVALID_TOKEN = 2003

    # 403 Fobidden
    TBD = 3000
    FOBIDDEN = 3001

    # 404 Not Found
    RESOURCE_NOT_FOUND = 4001

    # 500 Internal Server Error
    UNEXPECTED_ERROR = 9000
    CONNECTION_ERROR = 9001
    FAIL_CALL_GATEWAY = 9002
    MODEL_TIMEOUT = 9101
