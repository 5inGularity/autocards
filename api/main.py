from typing import List
from fastapi import Depends, FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db.db import SessionLocal
from db import models
from schemas import Article, Card
from tasks import process_article
import logging

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
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
    article: Article,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    article = models.Article(**article.dict())
    db.add(article)
    db.commit()
    db.refresh(article)
    background_tasks.add_task(process_article, article.id)
    return Article.from_orm(article)


@app.get("/articles", response_model=List[Article])
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
