from typing import Optional

from pydantic import BaseModel, Field
from db.models import ArticleStatus


class Article(BaseModel):
    id: Optional[int]
    title: str
    url: Optional[str]
    status: Optional[ArticleStatus]
    error: Optional[str]

    class Config:
        orm_mode = True


class Card(BaseModel):
    id: Optional[int]
    front: str = Field(description="text that should be on the front of the card")
    back: str = Field(description="text that should be at the back of the card")
    article_id: Optional[int]

    class Config:
        orm_mode = True


class ArticleContent(BaseModel):
    id: Optional[int]
    article_id: int
    content: str

    class Config:
        orm_mode = True
