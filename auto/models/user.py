from typing import List, Literal, Optional

from pydantic import BaseModel, EmailStr, Field

RoleEnum = Literal["ADMINISTRATOR"]


class UserEditDto(BaseModel):
    username: Optional[str] = Field(None, pattern=r"^[a-zA-Z0-9_]+$")
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=128)
    firstName: Optional[str] = Field(None, min_length=1, max_length=32)
    lastName: Optional[str] = Field(None, min_length=1, max_length=32)
    defaultCity: Optional[int] = None
    language: Optional[int] = None
    role: Optional[str] = None
    active: Optional[bool] = None

class UserReadDto(BaseModel):
    id: int
    username: str
    email: str
    lastName: str
    firstName: str
    role: RoleEnum
    avatar: Optional[str] = None
    defaultLanguage: Optional[int] = None
    defaultCity: Optional[int] = None
    active: bool

class UserRegisterDto(BaseModel):
    username: str = Field(..., pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    firstName: str = Field(..., min_length=1, max_length=32)
    lastName: str = Field(..., min_length=1, max_length=32)
    defaultCity: int
    language: Optional[int] = None
    role: str