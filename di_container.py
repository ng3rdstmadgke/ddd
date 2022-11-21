from dependency_injector import containers, providers
from repository import UserRepository, UserService
from application import UserApplicationService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Factoryは呼び出しごとに新しいインスタンスを作る
    user_repository = providers.Factory(
        UserRepository,
        store_path=config.store_path
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository
    )

    user_application = providers.Factory(
        UserApplicationService,
        repository=user_repository,
        service=user_service
    )


if __name__ == "__main__":
    config = {
        "store_path": "store.json"
    }

    container = Container()
    container.config.from_dict(config)
    container.init_resources()

    # リポジトリ
    repository = container.user_repository()

    # アプリケーション
    app = container.user_application()

    # 初期化
    repository.clear()

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