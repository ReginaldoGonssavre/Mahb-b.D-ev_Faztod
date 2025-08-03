from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    hashed_password: str
    is_active: bool

    class Config:
        from_attributes = True

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
