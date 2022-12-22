import abc
from pydantic import BaseModel
from repository import UserRepository, IUserRepository

class UserData(BaseModel):
    id: int
    user_name: str

class UserUpdateOutputData(BaseModel):
    """出力データ"""
    user_data: UserData

class UserGetInputData(BaseModel):
    """入力データ"""
    id: int


#
# [Use Case Output Port]
#
class IUserGetOutputPort(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def output(self, output_data: UserUpdateOutputData):
        raise NotImplementedError

#
# [Presenter]
#
class UserGetPresenter(IUserGetOutputPort):
    def output(self, output_data: UserUpdateOutputData):
        print(output_data)

#
# [Use Case Input Port]
#
class IUserGetInputPort(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def handle(self, input_data: UserGetInputData):
        raise NotImplementedError

#
# [Use Case Interactor]
#
class UserGetInteractor(IUserGetInputPort):
    """アプリケーションサービスのgetメソッドをそのままクラスにしたもの
    アプリケーションサービスと異なる点は、結果の出力先がpresenterオブジェクトであること
    """
    def __init__(self, repository: IUserRepository, presenter: IUserGetOutputPort):
        self.repository = repository
        self.presenter = presenter

    def handle(self, input_data: UserGetInputData):
        user = self.repository.find(input_data.id)
        if user is None:
            return
        user_data = UserData(id=user.id, user_name=str(user.user_name))
        output_data = UserUpdateOutputData(user_data=user_data)
        self.presenter.output(output_data)

#
# [Controller]
#
def controller(interactor: IUserGetInputPort):
    input_data = UserGetInputData(id=1)
    interactor.handle(input_data)

if __name__ == "__main__":
    repository = UserRepository("store.json")
    presenter = UserGetPresenter()
    interactor = UserGetInteractor(repository, presenter)
    controller(interactor)