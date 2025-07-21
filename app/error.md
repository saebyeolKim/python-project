# ERROR LOG

### [ERROR1] OAuth2PasswordRequestForm 의 데이터 형식 application/x-www-form-urlencoded 값을 못 읽는 현상 발생
- [오류 내용]
    - {"detail":[{"type":"model_attributes_type","loc":["body"],"msg":"`Input should be a valid dictionary or object to extract fields from","input`":"grant_type=password&username=apple@example.com&password=q123456789"}]}

- [해결 과정 1]
    - 저 코드만 남기고 다른 코드를 지운 뒤 실행 시 정상 작동
      
- [해결 과정 2]
    - dependency-injector의 @inject 데코레이터는 FastAPI의 request 파라미터 처리(특히 Depends, Form, Body) 순서를 바꿔버릴 수 있습니다.특히 pydantic 모델 (BaseModel)을 사용하는 POST 엔드포인트가 같은 라우터에 있으면 FastAPI가 request의 Content-Type을 보고 전역적으로 "JSON으로 왔겠지"라고 오판해버리는 경우가 생깁니다. 즉, /users/login에 form-data로 요청을 보내도, 다른 함수(/users POST 등)가 JSON을 기대하고 있으면 그걸 기준으로 전체 라우터에서 파싱 기준이 밀려버리는 현상이 발생합니다.

- [해결]
    - 로그인 기능을 최상단으로 올려서 해결, 지피티가 말하길 @inject 는 라우터에 등록하는 것이 아닌, 서비스와 서비스 사이의 의존성 주입을 위해 사용하는 것이라고 한다. 현재 이 프로젝트를 끝내고 다른 책들도 참고해서 어떻게 의존성 주입을 하는지 참고해 볼 것!

### [ERROR2] current_user: CurrnetUser = Depends(get_admin_user) 와 current_user: Annotated[CurrnetUser, Depends(get_current_user)] 의 차이점
- [오류내용]
  - get_users 에서는 Annotated 를 사용못하지만, delete_user 에서는 사용가능, 비슷한 기능임에도 차이점이 발생
    
- [해결]
  
✅ 이 코드는 Python 인터프리터가 문법적으로 OK

```Python
def get_users(
    page: int = 1,
    items_per_page: int = 1,
    current_user: CurrnetUser = Depends(get_admin_user),
):
```

- page와 items_per_page는 기본값이 있음 → 기본값 있는 인자

- current_user도 Depends(...) → 기본값이 있는 인자로 간주됨

- 따라서 순서 상 문제 없음 → Pylance/파이썬 모두 OK

❌ 이 코드는 Python 문법 오류 (또는 Pylance 오류) 발생 가능

```Python
def get_users(
    page: int = 1,
    items_per_page: int = 1,
    current_user: Annotated[CurrnetUser, Depends(get_admin_user)],
):
```

- Annotated[...]는 타입 힌트이므로 기본값이 없음

- 그런데 그 앞에 = 1 같은 기본값 있는 인자가 먼저 나옴

- → 파이썬 문법 위반: Non-default argument follows default argument ❌

✅ 반면 이건 OK

```Python
def delete_user(
    current_user: Annotated[CurrnetUser, Depends(get_current_user)],
):
```

- 여기엔 =1 같은 기본값 있는 인자가 없음

- 즉 Annotated[...]가 "기본값 없는 인자"더라도 순서 상 문제가 없음 → OK ✅

🔍 왜 이런 일이 벌어지나?

파이썬 문법 상 함수 정의에서 기본값이 있는 인자 다음에는 기본값 없는 인자가 올 수 없습니다.

FastAPI의 Depends(...)는 사실상 디폴트 값처럼 작동하지만, Annotated[...]는 단순히 타입 힌트일 뿐이기 때문에 기본값처럼 간주되지 않습니다.

그래서 파이썬은 이렇게 생각합니다:

```Python
# OK
def f(a=1, b=2): pass

# ❌ 오류: Non-default argument follows default argument
def f(a=1, b): pass
```

b가 Annotated[...]처럼 생겼으면 → 기본값 없는 인자처럼 간주됨 → 에러 발생
