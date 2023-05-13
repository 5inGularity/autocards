from enum import Enum

from sqlalchemy import Column, Integer, String, Enum as EnumType
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ArticleStatus(Enum):
    WAITING = "waiting"
    DOWNLOADING = "downloading"
    PROCESSING = "processing"
    ERROR = "error"
    READY = "ready"


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String)
    status = Column(
        EnumType(ArticleStatus), nullable=False, default=ArticleStatus.WAITING
    )
    content = Column(String)
    error = Column(String)
