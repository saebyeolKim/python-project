1. 로그인 기능을 만들다 OAuth2PasswordRequestForm 이 데이터 형식은 application/x-www-form-urlencoded 인데
자꾸 값을 못 읽는 현상 발생

[오류 내용]
{"detail":[{"type":"model_attributes_type","loc":["body"],"msg":"Input should be a valid dictionary or object to extract fields from","input":"grant_type=password&username=apple@example.com&password=q123456789"}]}

[해결 과정 1]
저 코드만 남기고 다른 코드를 지운 뒤 실행 시 정상 작동

[해결 과정 2]
dependency-injector의 @inject 데코레이터는 FastAPI의 request 파라미터 처리(특히 Depends, Form, Body) 순서를 바꿔버릴 수 있습니다.
특히 pydantic 모델 (BaseModel)을 사용하는 POST 엔드포인트가 같은 라우터에 있으면
FastAPI가 request의 Content-Type을 보고 전역적으로 "JSON으로 왔겠지"라고 오판해버리는 경우가 생깁니다.
즉, /users/login에 form-data로 요청을 보내도,
다른 함수(/users POST 등)가 JSON을 기대하고 있으면 그걸 기준으로 전체 라우터에서 파싱 기준이 밀려버리는 현상이 발생합니다.

[해결]
로그인 기능을 최상단으로 올려서 해결, 지피티가 말하길 @inject 는 라우터에 등록하는 것이 아닌, 서비스와 서비스 사이의 의존성 주입을 위해 사용하는 것이라고 한다.
현재 이 프로젝트를 끝내고 다른 책들도 참고해서 어떻게 의존성 주입을 하는지 참고해 볼 것!

