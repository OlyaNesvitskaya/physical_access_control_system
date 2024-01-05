from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    email: EmailStr
    password: str
    is_superuser: bool | None = False


class UpdateUserSchema(BaseModel):
    email: EmailStr | None = None
    password: str | None = None


class UserPostSchema(BaseModel):
    id: int
    email: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str

