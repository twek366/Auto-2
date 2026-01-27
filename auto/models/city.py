from typing import Optional

from pydantic import BaseModel


class CityEditDto(BaseModel):
    name: Optional[str] = None

class CityCreateDto(BaseModel):
    name: str