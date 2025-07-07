from fastapi import FastAPI
from user.interface.controllers.user_controller import router as user_routers
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

app = FastAPI(title="FastAPI 게시판", version="1.0.0")

# 라우터 등록
app.include_router(user_routers)

@app.exception_handler(RequestValidationError) # RequestValidationError 에러 발생 시 422 가 아닌 400 으로 오류코드 내보냄
async def valiation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content=exc.error
    )