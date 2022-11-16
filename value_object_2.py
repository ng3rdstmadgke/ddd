from pydantic import BaseModel, ValidationError, validator

# pydantic: https://pydantic-docs.helpmanual.io/usage/models/
class FullName(BaseModel):
  first_name: str
  last_name: str

  # pydantic - Validators: https://pydantic-docs.helpmanual.io/usage/validators/
  @validator("first_name", "last_name")
  def name_validator(cls, v):
      if len(v) <= 0 or len(v) > 32:
        raise ValueError("error...")
      return v

  def __str__(self):
    return f"{self.first_name} {self.last_name}"

  class Config:
      # イミュータブルなオブジェクトにする
      # pydantic - ModelConfig - Options: https://pydantic-docs.helpmanual.io/usage/model_config/#options
      allow_mutation = False

if __name__ == "__main__":
  full_name1 = FullName(first_name="keita", last_name="midorikawa")
  full_name2 = FullName(first_name="keita", last_name="midorikawa")
  # full_name3 = FullName(first_name="", last_name="")  # バリデーションエラー
  # full_name1.first_name = "hoge"  # エラー
  print(full_name1)  # keita midorikawa
  print(full_name1 == full_name2)  # True