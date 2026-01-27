from typing import List, Optional

from pydantic import BaseModel

from .common import CityReadDto
from .user import RoleEnum


class UserLoginDto(BaseModel):
    login: str
    password: str

class UserAuthDto(BaseModel):
    id: int
    username: str
    email: str
    firstName: str
    lastName: str
    defaultLanguage: Optional[int] = None
    defaultCity: Optional[int] = None
    token: str

class CurrentUserDto(BaseModel):
    id: int
    username: str
    email: str
    firstName: str
    lastName: str
    defaultCity: Optional[CityReadDto] = None
    language: Optional[int] = None
    avatar: Optional[str] = None
    role: RoleEnum
    token: str