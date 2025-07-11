from dependency_injector.wiring import inject, Provide
from containers import Container
from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from user.application.user_service import UserService

router = APIRouter(prefix="/users")

class CreateUserBody(BaseModel): # 파이단틱의 BaseModel 을 상속받아 파이단틱 모델 선언
    name: str
    email: str
    password: str
    memo: str

@router.post("", status_code=201)
@inject
def create_user(
    user: CreateUserBody,
    user_service: UserService = Depends(Provide[Container.user_service])
    # user_service: Annotated[UserService, Depends(UserService)]
):
    create_user = user_service.create_user(
        name=user.name,
        email=user.email,
        password=user.password,
        memo=user.memo
    )
    return create_user

class UpdateUserBody(BaseModel):
    name: str | None = None
    password: str | None = None

@router.post("/{user_id}")
@inject
def update_user(
    user_id: str,
    user: UpdateUserBody,
    user_service: UserService = Depends(Provide[Container.user_service])
):
    update_user = user_service.update_user(
        user_id=user_id,
        name=user.name,
        password=user.password,
    )
    return user

@router.get("")
@inject
def get_users(
    page: int = 1, 
    items_per_page: int = 1,
    user_service = Depends(Provide[Container.user_service]), 
):
    
    total_count, users = user_service.get_users(page, items_per_page)


    return {
        "total_count" : total_count,
        "page" : page,
        "users" : users
    }