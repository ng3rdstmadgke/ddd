from typing import Optional
from entity import User
from value_object import UserName
from repository import IUserRepository, UserStoreSchema, UserService

class InMemoryRepository(IUserRepository):
    """テスト用のインメモリなリポジトリを実装"""

    def __init__(self):
        self.data = UserStoreSchema(users=[])

    def save(self, user: User) -> Optional[User]:
        users = list(filter(lambda e: e.id == user.id, self.data.users))
        if len(users) > 0:
            # update
            delete_user = users[0]
            self.data.users.remove(delete_user)
        self.data.users.append(user)

    def find_by_name(self, user_name: UserName) -> Optional[User]:
        for user in self.data.users:
            if user.user_name == user_name:
                return user
        return None

    def delete(self, user: User):
        pass

    def find(self, id: int) -> Optional[User]:
        return None



class UserServiceTest:
    """ドメインサービスのテストコード"""

    def test_exists_false(self):
        """UserServiceのexistsメソッドをテスト"""
        user = User(id=1, user_name=UserName(first_name="kta", last_name="mido"))
        repository = InMemoryRepository()
        service = UserService(repository)
        assert service.exists(user) == False

    def test_exists_true(self):
        """UserServiceのexistsメソッドをテスト"""
        user = User(id=1, user_name=UserName(first_name="kta", last_name="mido"))
        repository = InMemoryRepository()
        repository.save(user)
        service = UserService(repository)
        assert service.exists(user) == True


if __name__ == "__main__":
    test = UserServiceTest()

    test.test_exists_false()
    test.test_exists_true()
