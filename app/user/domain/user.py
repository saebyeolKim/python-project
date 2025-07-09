from dataclasses import dataclass
from datetime import datetime

@dataclass
class Profile:
    name: str
    email: str

@dataclass # 도메인 객체를 다루기 쉽게 하기 위해 선언
class User:
    id: str
    profile: Profile
    password: str
    memo: str | None # null 허용
    created_at: datetime
    updated_at: datetime