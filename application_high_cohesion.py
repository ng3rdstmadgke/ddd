import abc
from typing import Optional, List
from value_object_2 import FullName
from entity import User
from repository import UserRepository, UserService, IUserRepository
from pydantic import BaseModel
from dataclasses import dataclass

class IUserRegisterApplicationService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def register(self, first_name: str, last_name: str):
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

    def register(self, first_name: str, last_name: str):
        full_name = FullName(first_name=first_name, last_name=last_name)
        user = User(full_name=full_name)
        if self.service.exists(user):
            raise Exception(f"{user.full_name} はすでに存在しています")
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
            user.full_name = FullName(first_name=first_name, last_name=last_name)
            if (self.service.exists(user)):
                raise Exception(f"{user.full_name} はすでに存在しています")
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

    # 追加
    UserRegisterApplicationService(repository, service).register("kta", "mido")

    # 取得
    user = UserGetApplicationService(repository, service).get(1)
    print(user)  # id=1 full_name=FullName(first_name='kta', last_name='mido')

    # 更新
    UserUpdateApplicationService(repository, service).update(1, "keita", "midorikawa")

    # 削除
    UserDeleteApplicationService(repository).delete(1)
