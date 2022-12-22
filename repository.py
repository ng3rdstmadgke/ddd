import abc
import os
from typing import Optional, List
from entity import User
from value_object import UserName
from pydantic import BaseModel

class UserStoreSchema(BaseModel):
    """データストアの構造定義"""
    id: int = 1
    users: List[User]

class IUserRepository(metaclass=abc.ABCMeta):
    """リポジトリのインターフェース"""
    @abc.abstractmethod
    def save(self, user: User) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_name(self, user_name: UserName) -> Optional[User]:
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

    def find_by_name(self, user_name: UserName) -> Optional[User]:
        for user in self._load().users:
            if user.user_name == user_name:
                return user
        return None

    def find(self, id: int) -> Optional[User]:
        for user in self._load().users:
            if user.id == id:
                return user
        return None


if __name__ == "__main__":
    store_path = "store.json"

    # リポジトリ
    repository = UserRepository(store_path)

    # 初期化
    repository.clear()

    # ユーザー追加処理
    username = UserName(first_name="kta", last_name="mido")
    user = User(id=0, user_name=username)
    user = repository.save(user)

    print(repository.find_by_name(username))

    # userの削除
    repository.delete(user)
