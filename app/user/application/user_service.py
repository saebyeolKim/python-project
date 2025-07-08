from dependency_injector.wiring import inject, Provide
from containers import Continer
from ulid import ULID
from datetime import datetime
from user.domain.user import User
from user.domain.repository.user_repo import IUserRepository
from fastapi import HTTPException, Depends
from utils.crypto import Crypto

class UserService:
    @inject
    def __init__(
        self,
        user_repo: IUserRepository, # 이렇게 하면 UserService 는 UserRepository 에 직접적인 의존을 안한다. 애플리케이션 계층이 인프라 계층과 의존 관계를 안만드는게 중요
    ):
        self.user_repo = user_repo
        self.ulid = ULID()
        self.crypto = Crypto()

    def create_user(self, name: str, email: str, password: str):
        _user = None

        try: 
            _user = self.usre_repo.find_by_email(email)
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
            created_at=now,
            updated_at=now,
        )
        self.usre_repo.save(user)