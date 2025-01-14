from fastapi import APIRouter
from app.core.exception.custom_exception import ServiceException, InvalidInputException
from app.core.exception.error import ErrorCode, ErrorDetailMessage

router = APIRouter()


@router.get("/{id}")
def exception_test(id: str):
    if id == "1":
        raise InvalidInputException(detail=ErrorDetailMessage.invalid_input_data)
    elif id == "2":
        raise ServiceException(detail=ErrorDetailMessage.server_error)
    elif id == "3":
        raise ServiceException(
            detail=ErrorDetailMessage.invalid_input_data,
            status_code=400,
            error_code=ErrorCode.INVALID_INPUT,
        )

    return "default"


# @router.post("/complex-operation")
# def complex_operation(request: ComplexRequest, db: Session = Depends(get_db)):
#     try:
#         service1 = Service1(db)
#         service2 = Service2(db)

#         result1 = service1.do_something(request)
#         result2 = service2.do_something_else(request)

#         db.commit()  # 한 트랜잭션으로 커밋
#         return {"result1": result1, "result2": result2}
#     except Exception as e:
#         db.rollback()  # 트랜잭션 전체 롤백
#         raise HTTPException(status_code=500, detail="Operation failed")
