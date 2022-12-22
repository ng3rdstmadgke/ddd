from pydantic import BaseModel, ValidationError, validator

# pydantic: https://pydantic-docs.helpmanual.io/usage/models/
class UserName(BaseModel):
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
    user_name1 = UserName(first_name="keita", last_name="midorikawa")
    user_name2 = UserName(first_name="keita", last_name="midorikawa")
    # user_name3 = UserName(first_name="", last_name="")    # バリデーションエラー
    # user_name1.first_name = "hoge"    # エラー
    print(user_name1)    # keita midorikawa
    print(user_name1 == user_name2)    # True