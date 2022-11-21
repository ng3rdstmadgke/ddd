import abc
from value_object import UserName
from entity import User

class IUserFactory(abc.ABCMeta):
    @abc.abstractmethod
    def create(user_name: UserName) -> User:
        pass