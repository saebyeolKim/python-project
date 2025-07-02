from fastapi import FastAPI
from app.core.init_db import init_db
from app.post.router import post_router
from app.auth.router import router as auth_router

app = FastAPI(title="FastAPI 게시판", version="1.0.0")

# DB 테이블 초기화
init_db()

# 라우터 등록
app.include_router(post_router)
app.include_router(auth_router)