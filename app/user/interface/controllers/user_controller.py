from dependency_injector.wiring import inject, Provide
from containers import Continer
from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from user.application.user_service import UserService

router = APIRouter(prefix="/users")

class CreateUserBody(BaseModel): # 파이단틱의 BaseModel 을 상속받아 파이단틱 모델 선언
    name: str
    email: str
    password: str

@router.post("", status_code=201)
@inject
def create_user(
    user: CreateUserBody,
    user_service: UserService = Depends(Provide[Continer.user_service])
    # user_service: Annotated[UserService, Depends(UserService)]
):
    create_user = user_service.create_user(
        name=user.name,
        email=user.email,
        password=user.password
    )
    return create_user