
# 🐳 Docker 컨테이너에서 Alembic 사용 가이드

## 📦 1. Docker 컨테이너 진입 및 Alembic 설치

```bash
# 컨테이너 목록 확인
docker ps

# 컨테이너에 접속 (예: my_app_container)
docker exec -it my_app_container /bin/bash

# Alembic 설치
pip install alembic
```

> **Tip:** 프로젝트 루트에 `requirements.txt`에 `alembic`을 추가하면 Dockerfile에서 자동 설치 가능

---

## 🏗️ 2. Alembic 초기화

```bash
alembic init alembic
```

**생성 파일 구조:**

- `alembic.ini` : Alembic 설정 파일
- `alembic/env.py` : 마이그레이션 환경 스크립트
- `alembic/versions/` : 마이그레이션 스크립트 저장 경로

---

## ⚙️ 3. 데이터베이스 연결 설정

`alembic.ini` 파일에서 다음 부분을 수정합니다:

```ini
sqlalchemy.url = postgresql+psycopg2://user:password@host:port/dbname
```

또는 환경 변수를 사용하고 싶다면 `env.py`에 다음과 같이 수정:

```python
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from myapp.models import Base  # SQLAlchemy Base 모델

config = context.config
fileConfig(config.config_file_name)

# 환경 변수에서 URL 읽기
config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL'))
target_metadata = Base.metadata
```

---

## 🧠 4. 모델 메타데이터 연결

`env.py` 파일에서 다음을 추가하거나 수정합니다:

```python
import database
target_metadata = database.Base.metadata

또는

from myapp.models import Base
target_metadata = Base.metadata
```

---

## 🧬 5. 마이그레이션 스크립트 생성

```bash
alembic revision --autogenerate -m "add User table"
```

---

## 🚀 6. 마이그레이션 적용 (테이블 생성)

```bash
alembic upgrade head
```

---

## ⏪ 7. 마이그레이션 롤백

```bash
# 한 단계 전으로 롤백
alembic downgrade -1

# 특정 리비전으로 롤백
alembic downgrade <revision_id>
```

---

## 📋 8. 마이그레이션 상태 확인

```bash
# 현재 리비전 확인
alembic current

# 전체 히스토리 보기
alembic history
```

---

## 🧼 9. 관리 팁

- 마이그레이션 파일은 Git 등의 버전 관리에 포함하세요.
- SQLAlchemy 모델 변경 시 `--autogenerate`로 새 리비전 생성하세요.
- Docker 컨테이너 재시작 시 `alembic upgrade head`를 entrypoint 또는 초기화 스크립트에 포함할 수 있습니다.
