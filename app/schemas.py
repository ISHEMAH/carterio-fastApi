from pydantic import BaseModel

class RoleBase(BaseModel):
    name: str
    id: int

    class Config:
        orm_mode = True

class RoleCreate(RoleBase):
    pass

class UserBase(BaseModel):
    username: str
    role_id: int

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    role: RoleBase

    class Config:
        orm_mode = True
