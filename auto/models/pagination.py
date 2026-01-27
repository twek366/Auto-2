from typing import Generic, List, TypeVar

from pydantic import BaseModel

from .common import Metadata

T = TypeVar("T")

class PageResponse(BaseModel, Generic[T]):
    content: List[T]
    metadata: Metadata