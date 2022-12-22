from value_object import UserName
from entity import User
from repository import IUserRepository, UserRepository

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
        found = self.user_repository.find_by_name(user.user_name)
        return found is not None

if __name__ == "__main__":
    # リポジトリ
    store_path = "store.json"
    repository = UserRepository(store_path)

    # ドメインサービス
    service = UserService(repository)

    # 初期化
    repository.clear()

    # 同名のユーザーが存在しなければuserを追加
    user = User(id=0, user_name=UserName(first_name="kta", last_name="mido"))
    if not service.exists(user):
        user = repository.save(user)

    # userの存在確認
    print(service.exists(user))  # True

    # userの削除
    repository.delete(user)

    # userの存在確認
    print(service.exists(user))  # False
