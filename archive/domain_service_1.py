from entity import User
from value_object import UserName

class UserService:
    def exists(self, user: User) -> bool:
        # ... 重複確認処理 ...
        return False

if __name__ == "__main__":
    user1 = User(id=1, full_name=UserName(first_name="hoge", last_name="fuga"))

    # ドメインサービス: 
    user_service = UserService()
    print(user_service.exists(user=user1))
