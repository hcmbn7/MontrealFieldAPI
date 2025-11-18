from pydantic import BaseModel, EmailStr, ConfigDict, Field


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=72)
    favorites: list[int] = Field(default_factory=list)


class UserOut(UserBase):
    id: int
    favorites: list[int] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)


class UserFavoritesUpdate(BaseModel):
    favorites: list[int] = Field(default_factory=list)


class UserUpdate(BaseModel):
    full_name: str | None = None
