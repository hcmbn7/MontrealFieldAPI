from pydantic import BaseModel, EmailStr, Field, ConfigDict


class AdminBase(BaseModel):
    email: EmailStr
    full_name: str


class AdminOut(AdminBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AdminLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)
