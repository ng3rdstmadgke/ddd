# dataclasses: https://docs.python.org/ja/3/library/dataclasses.html
from dataclasses import dataclass

@dataclass(frozen=True)
class FullName:
  first_name: str
  last_name: str
  
  def __str__(self):
    return f"{self.first_name} {self.last_name}"

if __name__ == "__main__":
  full_name1 = FullName(first_name="keita", last_name="midorikawa")
  full_name2 = FullName(first_name="keita", last_name="midorikawa")
  # full_name1.first_name = "hoge"  # エラー
  print(full_name1)
  print(full_name1 == full_name2)