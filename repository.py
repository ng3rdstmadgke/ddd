import abc
import os
from typing import Optional, List
from entity import User
from value_object_2 import FullName
from pydantic import BaseModel

class UserStoreSchema(BaseModel):
    """データストアの構造定義"""
    id: int = 1
    users: List[User]

    def increment(self) -> int:
        id = self.id
        self.id += 1
        return id

class IUserRepository(metaclass=abc.ABCMeta):
    """リポジトリのインターフェース"""
    @abc.abstractmethod
    def save(self, user: User) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_name(self, user_name: FullName) -> Optional[User]:
        raise NotImplementedError

    @abc.abstractmethod
    def find(self, id: int) -> Optional[User]:
        raise NotImplementedError

class UserRepository(IUserRepository):
    """リポジトリ
    データの入出力処理を担当
    """
    def __init__(self, store_path: str):
        self._store_path = store_path

    def _save(self, schema: UserStoreSchema):
        with open(self._store_path, "w") as writer:
            writer.write(schema.json(ensure_ascii=False, indent=2))

    def _load(self) -> UserStoreSchema:
        if os.path.exists(self._store_path):
            return UserStoreSchema.parse_file(self._store_path)
        return UserStoreSchema(users=[])

    def clear(self):
        self._save(UserStoreSchema(users=[]))

    def save(self, user: User) -> User:
        store = self._load()
        users = list(filter(lambda e: e.id == user.id, store.users))
        if len(users) > 0:
            # update
            delete_user = users[0]
            store.users.remove(delete_user)
        else:
            # add
            user.id = store.increment()
        store.users.append(user)
        self._save(store)
        return user

    def delete(self, user: User):
        store = self._load()
        users = list(filter(lambda e: e.id == user.id, store.users))
        if len(users) > 0:
            delete_user = users[0]
            store.users.remove(delete_user)
            self._save(store)

    def find_by_name(self, user_name: FullName) -> Optional[User]:
        for user in self._load().users:
            if user.full_name == user_name:
                return user
        return None

    def find(self, id: int) -> Optional[User]:
        for user in self._load().users:
            if user.id == id:
                return user
        return None



class UserService:
    """ドメインサービス
    データの入出力はリポジトリを利用することで実現する。
    後でテストができるように、リポジトリのインターフェースに依存させる
    """
    def __init__(self, user_repository: IUserRepository):
        # インターフェース依存
        self.user_repository = user_repository
    
    # 「ユーザーの重複確認」はドメインのルールに近いので、existsはドメインサービスに実装する
    def exists(self, user: User) -> bool:
        # データの入出力処理をリポジトリに閉じ込めることで、見通しが良くなる
        found = self.user_repository.find_by_name(user.full_name)
        return found is not None

if __name__ == "__main__":
    store_path = "store.json"

    # リポジトリ
    repository = UserRepository(store_path)

    # ドメインサービス
    service = UserService(repository)

    # 初期化
    repository.clear()


    # ユーザー追加処理
    user = User(full_name=FullName(first_name="kta", last_name="mido"))

    # 同名のユーザーが存在しなければuserを追加
    if not service.exists(user):
        user = repository.save(user)

    # userの存在確認
    print(service.exists(user))  # True

    # userの削除
    repository.delete(user)

    # userの存在確認
    print(service.exists(user))  # False
