from dependency_injector.wiring import inject, Provide
from containers import Container
from fastapi import BackgroundTasks, APIRouter, Depends
from pydantic import BaseModel, EmailStr, Field
from user.application.user_service import UserService
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
from common.auth import CurrentUser, get_current_user, get_admin_user
from typing import Annotated

router = APIRouter(prefix="/users")

class CreateUserBody(BaseModel): # 파이단틱의 BaseModel 을 상속받아 파이단틱 모델 선언
    name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(max_length=64)
    password: str = Field(min_length=8, max_length=32)
    memo: str | None = Field(default=None)

class UpdateUserBody(BaseModel):
    name: str | None = Field(min_length=2, max_length=32, default=None)
    password: str | None = Field(min_length=8, max_length=32, default=None)

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime
    updated_at: datetime

class GetUserResponse(BaseModel):
    total_count: int
    page: int
    users: list[UserResponse]
    
@router.post("/login")
@inject
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service : UserService = Depends(Provide[Container.user_service])
):
    access_token = user_service.login(
        email=form_data.username,
        password=form_data.password,
    )

    return {"access_token" : access_token, "token_type": "bearer"}

@router.post("", status_code=201)
@inject
def create_user(
    user: CreateUserBody,
    background_tasks: BackgroundTasks,
    user_service: UserService = Depends(Provide[Container.user_service]),
    # user_service: Annotated[UserService, Depends(UserService)]
):
    create_user = user_service.create_user(
        # background_tasks=background_tasks,
        name=user.name,
        email=user.email,
        password=user.password,
        memo=user.memo
    )
    return create_user

@router.put("", response_model=UserResponse)
@inject
def update_user(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    body: UpdateUserBody,
    user_service: UserService = Depends(Provide[Container.user_service])
):
    update_user = user_service.update_user(
        user_id=current_user.id,
        name=body.name,
        password=body.password,
    )
    return update_user

@router.get("")
@inject
def get_users(
    page: int = 1, 
    items_per_page: int = 1,
    current_user: CurrentUser = Depends(get_admin_user), # page, items_per_page 의 기본값이 있기 때문에 이렇게 파라미터를 받아야한다. 만약 맨 앞에 사용한다면 Annotated 사용 가능
    user_service : UserService = Depends(Provide[Container.user_service]), 
) -> GetUserResponse :
    total_count, users = user_service.get_users(page, items_per_page)


    return {
        "total_count" : total_count,
        "page" : page,
        "users" : users
    }

@router.delete("", status_code=204)
@inject
def delete_user(
    current_user: Annotated[CurrentUser, Depends(get_current_user)], # 기본값이 없기 때문에 이렇게 사용해서 기본값이 없는 인자로 간주 가능
    user_service : UserService = Depends(Provide[Container.user_service])
):
    # TODO: 다른 유저를 삭제할 수 없도록 토큰에서 유저 아이디를 구한다.
    user_service.delete_user(current_user.id)