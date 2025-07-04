from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config: # SQLAlchemy 모델(ORM 객체)(예: User) → Pydantic 모델(dict 타입)(예: UserOut)로 자동 변환 가능하게 만들어줌
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"