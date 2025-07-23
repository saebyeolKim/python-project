from fastapi import FastAPI
from user.interface.controllers.user_controller import router as user_routers
from note.interface.controllers.note_controller import router as note_routers
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from containers import Container
from starlette.status import HTTP_400_BAD_REQUEST
from fastapi import FastAPI, Depends

app = FastAPI(title="FastAPI 게시판", version="1.0.0")
app.container = Container() # 애플리케이션을 구동할 때 앞에서 containers.py 컨테이너 클래스 등록

# 라우터 등록
app.include_router(user_routers)
app.include_router(note_routers)

@app.exception_handler(RequestValidationError) # RequestValidationError 에러 발생 시 422 가 아닌 400 으로 오류코드 내보냄
async def valiation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    # exc.errors() 안에 있는 'input' 값을 bytes → str로 변환
    safe_errors = []
    for err in exc.errors():
        err_copy = err.copy()
        if isinstance(err_copy.get("input"), bytes):
            try:
                err_copy["input"] = err_copy["input"].decode("utf-8")
            except UnicodeDecodeError:
                err_copy["input"] = "<binary data>"
        safe_errors.append(err_copy)

    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"detail": safe_errors}
    )