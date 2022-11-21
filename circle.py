from typing import List
from dataclasses import dataclass
from pydantic import BaseModel

class User(BaseModel):
    id: int
    user_name: str

    def greet(self):
        return f"hello. {self.user_name}"


class Circle(BaseModel):
    id: int = 0
    members: List[User] = []

    def is_full(self) -> bool:
        return len(self.members) >= 30

    def join(self, user: User):
        # 2. 引数で渡されたオブジェクトのメソッドへのアクセス
        print(user.greet())
        # 1. Circle自身のメソッドへのアクセス
        if self.is_full():
            raise Exception()
        # 4. Circleのインスタンス変数のメソッドへのアクセス
        self.members.append(user)


if __name__ == "__main__":
    circle = Circle()
    user1 = User(id=1, user_name="foo")
    # 3. 直接インスタンス化されたオブジェクトのメソッドへのアクセス
    circle.join(user1)

    # circle.member.append(user1) のように内部のオブジェクトを直接操作するのはNG
