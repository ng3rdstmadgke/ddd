from typing import Type, Dict, Any
from repository import UserRepository, IUserRepository
from entity import User
from value_object import UserName

class ServiceLocator:
    services: Dict[Any, Any] = {}

    @classmethod
    def register(cls, interface: Type, type: Type):
        cls.services[interface] = type

    @classmethod
    def resolve(cls, interface: Type) -> Type:
        return cls.services[interface]

if __name__ == "__main__":

    # インターフェースに紐づく形で利用するリポジトリの具象クラスを登録しておく
    ServiceLocator.register(IUserRepository, UserRepository)

    # リポジトリを利用するときにServiceLocator経由でリポジトリの具象クラスを取得
    Repository = ServiceLocator.resolve(IUserRepository)

    # リポジトリインスタンス
    repository = Repository("store.json")

    user = User(full_name=UserName(first_name="foo", last_name="bar"))

    repository.save(user)
    repository.delete(user)