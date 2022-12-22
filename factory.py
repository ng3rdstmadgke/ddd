import abc
from value_object import UserName
from entity import User
from repository import IUserRepository, UserRepository
from domein_service import UserService

class IUserFactory(metaclass=abc.ABCMeta):
    """ファクトリーのインターフェース"""
    @abc.abstractmethod
    def create(self, user_name: UserName) -> User:
        raise NotImplementedError

class UserFactory(IUserFactory):
    """ファクトリー"""

    def __init__(self):
        pass

    def create(self, user_name: UserName) -> User:
        id = 1  # DBに接続してインクリメントされたIDを撮ってくる処理
        return User(id=id, user_name=user_name)


class UserApplicationService:
    def __init__(
        self,
        repository: IUserRepository,
        service: UserService, 
        factory: IUserFactory
    ):
        self.service = service
        self.repository = repository
        self.factory = factory

    def register(self, first_name: str, last_name: str):
        user_name = UserName(first_name=first_name, last_name=last_name)
        user = self.factory.create(user_name)
        if self.service.exists(user):
            raise Exception(f"{user.user_name} はすでに存在しています")
        self.repository.save(user)

if __name__ == "__main__":
    store_path = "store.json"

    # リポジトリ
    repository = UserRepository(store_path)

    # ドメインサービス
    service = UserService(repository)

    # ファクトリー
    factory = UserFactory()

    # 初期化
    repository.clear()

    # アプリケーション
    app = UserApplicationService(repository, service, factory)

    # 追加
    app.register("kta", "mido")
