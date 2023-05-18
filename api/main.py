from typing import List, Union
from fastapi import Depends, FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, load_only
from db.db import SessionLocal
from db import models
from schemas import Article, Card, ArticleContent, CreateArticleInput
from tasks import process_article
import logging

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post("/articles/", response_model=Article)
def create_article(
    input: CreateArticleInput,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    if input.url:
        article = models.Article(url=input.url, title=input.title)
    elif input.text:
        if not input.title:
            raise HTTPException(
                status_code=400, detail="Title is required when specifying text"
            )
        article = models.Article(title=input.title, content=input.text)
    else:
        raise HTTPException(status_code=400, detail="One of URL, Text is required")
    db.add(article)
    db.commit()
    db.refresh(article)
    background_tasks.add_task(process_article, article.id)
    return Article.from_orm(article)


@app.get("/articles", response_model=List[Article], response_model_exclude_unset=True)
def list_articles(db: Session = Depends(get_db)):
    return db.query(models.Article).all()


@app.get("/articles/{article_id}", response_model=Article)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(models.Article).get(article_id)
    if article is None:
        raise HTTPException(status_code=400, detail="Article not found")
    return article


@app.get("/articles/{article_id}/cards", response_model=List[Card])
def get_cards(article_id: int, db: Session = Depends(get_db)):
    return db.query(models.Card).filter_by(article_id=article_id).all()


@app.delete("/articles/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(models.Article).get(article_id)
    if article is None:
        raise HTTPException(status_code=400, detail="Article not found")
    db.delete(article)
    db.commit()


@app.get("/articles/{article_id}/content", response_model=ArticleContent)
def get_article_content(article_id: int, db: Session = Depends(get_db)):
    content = (
        db.query(models.Article)
        .options(load_only(models.Article.id, models.Article.content))
        .get(article_id)
    )
    if content is None or content.content is None:
        raise HTTPException(status_code=400, detail="Content not found")
    return ArticleContent(article_id=content.id, content=content.content)
