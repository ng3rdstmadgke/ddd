import abc
from typing import Optional
from value_object import UserName
from entity import User
from repository import UserRepository, IUserRepository
from domein_service import UserService

class IUserRegisterApplicationService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def register(self, id: int, first_name: str, last_name: str):
        raise NotImplementedError

class IUserGetApplicationService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self, id: int) -> Optional[User]:
        raise NotImplementedError

class IUserUpdateApplicationService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def update(self, id: int, first_name: Optional[str] = None, last_name: Optional[str] = None): 
        raise NotImplementedError

class IUserDeleteApplicationService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def delete(self, id: int):
        raise NotImplementedError

class UserRegisterApplicationService(IUserRegisterApplicationService):
    def __init__(self, repository: IUserRepository, service: UserService):
        self.service = service
        self.repository = repository

    def register(self, id: int, first_name: str, last_name: str):
        user_name = UserName(first_name=first_name, last_name=last_name)
        user = User(id=id, user_name=user_name)
        if self.service.exists(user):
            raise Exception(f"{user.user_name} はすでに存在しています")
        self.repository.save(user)

class UserGetApplicationService(IUserGetApplicationService):
    def __init__(self, repository: IUserRepository, service: UserService):
        self.service = service
        self.repository = repository

    def get(self, id: int) -> Optional[User]:
        return self.repository.find(id)

class UserUpdateApplicationService(IUserUpdateApplicationService):
    def __init__(self, repository: IUserRepository, service: UserService):
        self.service = service
        self.repository = repository

    def update(self, id: int, first_name: Optional[str] = None, last_name: Optional[str] = None): 
        user = self.repository.find(id)
        if user is None:
            raise Exception(f"ユーザーが見つかりません (id={id})")
        if first_name is not None and last_name is not None:
            user.user_name = UserName(first_name=first_name, last_name=last_name)
            if (self.service.exists(user)):
                raise Exception(f"{user.user_name} はすでに存在しています")
        self.repository.save(user)

class UserDeleteApplicationService(IUserDeleteApplicationService):
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    def delete(self, id: int):
        user = self.repository.find(id)
        if user is None:
            raise Exception(f"ユーザーが見つかりません (id={id})")
        self.repository.delete(user)



if __name__ == "__main__":
    store_path = "store.json"

    # リポジトリ
    repository = UserRepository(store_path)

    # ドメインサービス
    service = UserService(repository)

    # 初期化
    repository.clear()

    # アプリケーション
    register_app = UserRegisterApplicationService(repository, service)

    # 追加
    register_app.register(1, "kta", "mido")
    register_app.register(2, "hoge", "fuga")
    register_app.register(3, "foo", "bar")

    # 取得
    get_app = UserGetApplicationService(repository, service)
    print(get_app.get(1))  # id=1 user_name=UserName(first_name='kta', last_name='mido')

    # 更新
    update_app = UserUpdateApplicationService(repository, service)
    update_app.update(1, "keita", "midorikawa")

    # 削除
    delete_app = UserDeleteApplicationService(repository)
    delete_app.delete(1)