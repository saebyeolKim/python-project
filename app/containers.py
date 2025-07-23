# dependency-injector 를 활용해
# 애플리케이션이 구동될 때 IoC 컨테이너(현재 파일)에 미리 의존성을 제공하는 객체를 등록해두고
# 필요한 모듈에서 주입하도록 할 수 있다.

from dependency_injector import containers, providers
from user.application.user_service import UserService
from note.application.note_service import NoteService
from user.infra.repository.user_repo import UserRepository
from note.infra.repository.note_repo import NoteRepository

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "user",
            "note"
        ], # 의존성을 사용할 모듈 선언, packages 에 패키지의 경로를 기술하면 해당 패키지 하위에 있는 모듈이 모두 포함.
    )

    user_repo = providers.Factory(UserRepository) # 의존성을 제공할 모듈을 팩토리에 등록
    user_service = providers.Factory(UserService, user_repo=user_repo)
    note_repo = providers.Factory(NoteRepository)
    note_service = providers.Factory(NoteService, note_repo=note_repo)