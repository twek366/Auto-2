from datetime import datetime

from pydantic import BaseModel



class City(BaseModel):
    id: int
    name: str

class CityReadDto(City):
    pass

class Metadata(BaseModel):
    page: int
    size: int
    totalElements: int

class ErrorResponse(BaseModel):
    date: datetime
    message: dict