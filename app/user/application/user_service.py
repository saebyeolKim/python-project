from ulid import ULID
from datetime import datetime
from user.domain.user import User
from user.domain.repository.user_repo import IUserRepository
from fastapi import HTTPException, Depends, status
from utils.crypto import Crypto
from common.auth import create_access_token

class UserService:
    def __init__(
        self,
        user_repo: IUserRepository, # 이렇게 하면 UserService 는 UserRepository 에 직접적인 의존을 안한다. 애플리케이션 계층이 인프라 계층과 의존 관계를 안만드는게 중요
    ):
        self.user_repo = user_repo
        self.ulid = ULID()
        self.crypto = Crypto()

    def create_user(
            self, 
            name: str, 
            email: str, 
            password: str,
            memo: str | None = None # 문자열이나 None을 받을 수 있고, 기본값은 None
    ):
        _user = None

        try: 
            _user = self.user_repo.find_by_email(email)
        except HTTPException as e:
            if e.status_code != 422:
                raise e
            
        if _user: # 이미 가입한 유저일 경우 422 에러 발생
            raise HTTPException(status_code=422)

        now = datetime.now()
        user: User = User(
            id=self.ulid.generate(),
            name=name,
            email=email,
            password=self.crypto.encrypt(password),
            memo=memo,
            created_at=now,
            updated_at=now,
        )
        self.user_repo.save(user)

    def update_user(
            self,
            user_id: str,
            name: str | None = None,
            password: str | None = None,
    ):
        user = self.user_repo.find_by_id(user_id)

        if name:
            user.name = name

        if password:
            user.password = self.crypto.encrypt(password)
        
        user.updated_at = datetime.now()

        self.user_repo.update(user)

        return user
    
    def get_users(self, page: int, items_per_page: int) -> tuple[int, list[User]]:
        users = self.user_repo.get_users(page, items_per_page)
        return users
    
    def delete(self, id: str):
        self.user_repo.delete(id)

    def login(self, email: str, password: str):
        user = self.user_repo.find_by_email(email)

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        if not self.crypto.verify(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) # 비밀번호가 일치하지 않다면 오류 발생
    
        access_token = create_access_token(
            payload={"user_id": user.id}
        )

        return access_token