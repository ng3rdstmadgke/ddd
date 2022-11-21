import abc
from typing import Optional, List
from value_object import UserName
from entity import User
from repository import UserRepository, UserService, IUserRepository
from pydantic import BaseModel
from dataclasses import dataclass

class IUserApplicationService(metaclass=abc.ABCMeta):
    """アプリケーションサービスのインターフェース
    クライアント側でモック実装を作れるようにインターフェースを作る
    """
    @abc.abstractmethod
    def register(self, first_name: str, last_name: str):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int) -> Optional[User]:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, id: int, first_name: Optional[str] = None, last_name: Optional[str] = None): 
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, id: int):
        raise NotImplementedError


class UserApplicationService(IUserApplicationService):
    def __init__(self, repository: IUserRepository, service: UserService):
        self.service = service
        self.repository = repository

    def register(self, first_name: str, last_name: str):
        user_name = UserName(first_name=first_name, last_name=last_name)
        user = User(user_name=user_name)
        if self.service.exists(user):
            raise Exception(f"{user.user_name} はすでに存在しています")
        self.repository.save(user)

    def get(self, id: int) -> Optional[User]:
        """
        本が言うには、ドメインオブジェクト(User)のふるまいの呼び出しはアプリケーションサービスの役目であり、クライアントが自由に操作できてはいけないらしい。
        なので取得したオブジェクトが変更できないようにDTO(Data Transfer Object)という参照専用の型に変換して返すのが本当はいいらしい
        ```
        # データ転送用オブジェクト(DTO)
        class UserData:
            def __init__(self, user: User):
                self.id = user.id
                self.user_name = str(user.user_name)
        ```
        """
        return self.repository.find(id)

    def update(self, id: int, first_name: Optional[str] = None, last_name: Optional[str] = None): 
        """
        UserUpdateCommandのようなコマンドオブジェクトを作成して、引数をオブジェクトとして受け取ってもよい。
        ```
        @dataclass(frozen=True)
        class UserUpdateCommand(BaseModel):
            id: int
            first_name: Optional[str]
            last_name: Optional[str]
        ```
        """
        user = self.repository.find(id)
        if user is None:
            raise Exception(f"ユーザーが見つかりません (id={id})")
        if first_name is not None and last_name is not None:
            user.user_name = UserName(first_name=first_name, last_name=last_name)
            if (self.service.exists(user)):
                raise Exception(f"{user.user_name} はすでに存在しています")
        self.repository.save(user)
    
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
    app = UserApplicationService(repository, service)

    # 追加
    app.register("kta", "mido")
    app.register("foo", "bar")
    app.register("hoge", "piyo")

    # 取得
    print(app.get(1))  # id=1 user_name=UserName(first_name='kta', last_name='mido')

    # 更新
    app.update(1, "keita", "midorikawa")

    # 削除
    app.delete(3)