from value_object_2 import FullName
from pydantic import BaseModel

class User(BaseModel):
    id: int = 0
    full_name: FullName

    def __eq__(self, other):
        if other is None or not isinstance(other, User):
            return False
        return self.id == other.id

if __name__ == "__main__":
    user1 = User(id=1, full_name=FullName(first_name="keita", last_name="midorikawa"))
    user2 = User(id=2, full_name=FullName(first_name="keita", last_name="midorikawa"))
    user3 = User(id=1, full_name=FullName(first_name="makoto", last_name="midorikawa"))

    # IDによってい識別される
    print(user1 == user2)  # False
    print(user1 == user3)  # True

    # ミュータブル
    user1.full_name = FullName(first_name="hoge", last_name="fuga")
    print(user1)  # True
