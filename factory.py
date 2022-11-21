import abc
from value_object import UserName
from entity import User

class IUserFactory(abc.ABCMeta):
    @abc.abstractmethod
    def create(self, user_name: UserName) -> User:
        raise NotImplementedError

class UserFactory(IUserFactory):
    def create(self, user_name: UserName) -> User:
