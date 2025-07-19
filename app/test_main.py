from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
import uvicorn

# 컨테이너, 라우터, 예외 핸들러 등 모든 것을 제외한 순수 FastAPI 앱
app = FastAPI()

@app.post("/login")
def login_test(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """
    이 엔드포인트가 성공하는지 테스트합니다.
    """
    return {"status": "Minimal test successful!", "username": form_data.username}

# 이 파일을 직접 실행하기 위한 코드
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
