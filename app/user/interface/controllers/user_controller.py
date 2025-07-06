from fastapi import APIRouter
from pydantic import BaseModel
from app.user.application.user_service import UserService

router = APIRouter(prefix="/users")

class CreateUserBody(BaseModel): # 파이단틱의 BaseModel 을 상속받아 파이단틱 모델 선언
    name: str
    email: str
    password: str

@router.post("", status_code=201)
def create_user(user: CreateUserBody):
    user_serivce = UserService()
    create_user = user_serivce.create_user(
        name=user.name,
        email=user.email,
        password=user.password
    )
    return create_user