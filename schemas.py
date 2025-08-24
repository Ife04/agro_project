from pydantic import BaseModel, EmailStr
from enum import Enum

class UserRole(str, Enum):
    buyer = "buyer"
    seller = "seller"

class UserCreate(BaseModel):
    Lastname: str
    Othername: str
    Phonenumber: str
    username: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.buyer   # default = buyer

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    is_seller: bool
