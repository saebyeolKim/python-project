# 🚀 FastAPI 게시판 프로젝트

간단한 게시판 REST API를 FastAPI로 개발한 프로젝트입니다. JWT 기반 회원 인증, 게시글 CRUD, Docker 기반 환경 구성 등을 포함합니다.

---

## 📁 프로젝트 구조

```
app/
├── auth/                     # 🔐 인증 관련 로직
│   ├── dependencies.py       # JWT 토큰 검증 및 유저 의존성 처리
│   ├── router.py             # /auth 라우터 등록
│   ├── schemas.py            # 사용자 요청/응답 스키마 정의
│   └── service.py            # 비밀번호 해시/검증, 토큰 생성 함수
│
├── core/
│   └── init_db.py            # DB 테이블 초기화 함수 (Base.metadata.create_all)
│
├── post/                     # 📃 게시글 관련 로직
│   ├── router.py             # /posts 라우터 등록
│   ├── schemas.py            # 게시글 요청/응답 스키마 정의
│   └── service.py            # 게시글 CRUD 비즈니스 로직
│
├── models.py                 # 📊 SQLAlchemy 모델 정의 (User, Post)
├── db.py                     # 🎉 DB 연결 설정 및 SessionLocal
└── main.py                   # 🚀 FastAPI 앱 진입점
```

---

## ⚡️ 기능 요약

* 회원가입
* 로그인 (JWT 토큰 반환)
* 게시글 작성/조회/수정/삭제
* 로그인 사용자 인증 처리
* Docker, Docker Compose 구성
* .env 환경 변수 관리

---

## ⚙️ 실행 방법

### 1. `.env` 파일 생성

`.env` 파일은 다음과 같이 구성합니다.

```env
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=your_database_name
POSTGRES_HOST=db
POSTGRES_PORT=5432
SECRET_KEY=your_jwt_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> ⚠️ `.env` 파일은 `.gitignore` 파일에 들어가여 Git에 포함되지 않게 해주세요.

### 2. Docker Compose 실행

```
docker-compose up --build
```

### 3. API 문서 확인

[http://localhost:8000/docs](http://localhost:8000/docs) 접속 시 Swagger UI 확인 가능

---

## 📘 사용 기술 스택

* **FastAPI**
* **SQLAlchemy**
* **PostgreSQL**
* **Docker / Docker Compose**
* **passlib\[bcrypt]**: 비밀번호 해싱
* **python-jose**: JWT 발급

---

## 📃 주요 라우터

### 인증 (auth)

* `POST /auth/signup`: 회원가입
* `POST /auth/login`: 로그인 (access token 반환)
* `POST /auth/me`: 로그인 사용자 정보 조회

### 게시글 (posts)

* `POST /posts/`: 게시글 작성
* `GET /posts/`: 전체 게시글 목록
* `GET /posts/{post_id}`: 게시글 상세 조회
* `PUT /posts/{post_id}`: 게시글 수정
* `DELETE /posts/{post_id}`: 게시글 삭제

---

## 📢 향후 추가 예정

- [x] `/auth/me` 로그인 사용자 정보 확인 API
- [ ] 댓글(Comment) 기능 구현
- [ ] 게시글 페이징, 검색 기능
- [ ] 파일 업로드 기능 (이미지 등)
- [ ] 예외 처리 통합 / 에러 메시지 개선
- [ ] 테스트 코드 작성 (`pytest`, `TestClient`)
- [ ] OpenAPI 문서 정리 (summary, description 등)
- [ ] `.env.example` 제공 및 README 실행 가이드 보강
- [ ] 관리자 페이지 or 프론트 연동 (ex. Next.js)


## 🧭 진행 순서
1. /auth/me, 댓글 기능
2. 게시글 페이징/검색
3. 테스트 코드 작성 & 예외 처리
4. 파일 업로드
5. 배포 자동화 or CI/CD
6. 관리자 페이지 or Next.js 프론트 연동
7. 배포 자동화 (Gunicorn, Render, Fly.io 등)

---

> 문의 및 피드백은 언제든지 환영합니다!
