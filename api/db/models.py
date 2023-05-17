from enum import Enum

from sqlalchemy import Column, Integer, String, Enum as EnumType, ForeignKey
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

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    url = Column(String)
    status = Column(
        EnumType(ArticleStatus), nullable=False, default=ArticleStatus.WAITING
    )
    error = Column(String)


class ArticleContent(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"))
    content = Column(String, nullable=False)


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    front = Column(String, nullable=False)
    back = Column(String, nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"))
