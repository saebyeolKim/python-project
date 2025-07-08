from fastapi import FastAPI
from user.interface.controllers.user_controller import router as user_routers
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from containers import Continer

app = FastAPI(title="FastAPI 게시판", version="1.0.0")
app.container = Continer() # 애플리케이션을 구동할 때 앞에서 containers.py 컨테이너 클래스 등록

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