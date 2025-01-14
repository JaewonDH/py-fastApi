from fastapi import HTTPException
from app.core.exception.error import ErrorCode, ErrorDetailMessage
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger("custom_exception")


class ServiceException(HTTPException):
    def __init__(
        self,
        detail: ErrorDetailMessage | str,
        status_code: int = 500,
        error_code: ErrorCode = ErrorCode.UNEXPECTED_ERROR,
    ):
        # logger.info(f"ServiceException status_code={status_code}")
        detail = detail.value if type(detail) == ErrorDetailMessage else detail
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code.value


class NotFoundException(ServiceException):
    def __init__(self, detail: ErrorDetailMessage):
        super().__init__(
            detail=detail, status_code=404, error_code=ErrorCode.RESOURCE_NOT_FOUND
        )


class InvalidInputException(ServiceException):
    def __init__(
        self,
        detail: ErrorDetailMessage = ErrorDetailMessage.invalid_input_data,
        status_code: int = 400,
        error_code: ErrorCode = ErrorCode.INVALID_INPUT,
    ):
        super().__init__(detail=detail, status_code=status_code, error_code=error_code)


def response_data(exc: ServiceException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.error_code, "message": exc.detail},
    )


def set_error_handlers(app: FastAPI):
    @app.exception_handler(ServiceException)
    async def service_exception_handler(request: Request, exc: ServiceException):
        return response_data(exc)
