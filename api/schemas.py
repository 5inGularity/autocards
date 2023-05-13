from typing import Optional

from pydantic import BaseModel
from db.models import ArticleStatus


class Article(BaseModel):
    id: Optional[int]
    title: str
    url: Optional[str]
    status: Optional[ArticleStatus]
    content: Optional[str]
    error: Optional[str]

    class Config:
        orm_mode = True
