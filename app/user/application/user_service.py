from ulid import ULID
from datetime import datetime
from app.user.domain.user import User
from app.user.domain.repository.user_repo import IUserRepository
from app.user.infra.repository.user_repo import UserRepository
from fastapi import HTTPException
from app.utils.crypto import Crypto

class UserService:
    def __init__(self):
        self.user_repo: IUserRepository = UserRepository()
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