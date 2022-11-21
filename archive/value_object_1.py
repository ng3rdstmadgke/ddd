# dataclasses: https://docs.python.org/ja/3/library/dataclasses.html
from dataclasses import dataclass

# dataclasses: https://docs.python.org/ja/3/library/dataclasses.html
# frozen=True: オブジェクトを不変にする
# eq=True: __eq__ を自動実装する (デフォルトTrue)
@dataclass(frozen=True)
class UserName:
  first_name: str
  last_name: str
  
  def __str__(self):
    return f"{self.first_name} {self.last_name}"

if __name__ == "__main__":
  full_name1 = UserName(first_name="keita", last_name="midorikawa")
  full_name2 = UserName(first_name="keita", last_name="midorikawa")
  # full_name1.first_name = "hoge"  # エラー
  print(full_name1)
  print(full_name1 == full_name2)