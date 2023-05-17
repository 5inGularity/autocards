from typing import List
from db.models import Article, ArticleStatus, Card as CardModel
from db.db import SessionLocal
from schemas import Card
from sqlalchemy.orm import Session
import requests
import tempfile
from unstructured.partition.json import partition_json
from langchain.document_loaders import UnstructuredAPIFileLoader
from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.output_parsers import PydanticOutputParser
from langchain.text_splitter import TokenTextSplitter
from pydantic import BaseModel, Field
from typing import List
import json
import logging


PROMPT = """
In the following text delimited with triple backticks, identify at most five most important facts, and create flash cards for them. 
Where a flash card has front text and a back text.
For example, if the key idea is "LLM means Large Language Model" then the flash card could be "front" : "LLM" and "back": "Large Language Model". 
{format_instructions}
Do not return anything else but the JSON object conforming to the above schema.

```{text}```
"""


class Cards(BaseModel):
    cards: List[Card] = Field(description="list of flash cards")


def save_cards(cards: List[Card], article: Article, db: Session):
    for card in cards:
        card.article_id = article.id
        card.id = None
    db.add_all([CardModel(**card.dict()) for card in cards])
    db.commit()


def get_cards(documents):
    llm = OpenAI(temperature=0, model_name="text-davinci-003", max_tokens=2000)

    output_parser = PydanticOutputParser(pydantic_object=Cards)

    llm_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate(
            template=PROMPT,
            input_variables=["text"],
            partial_variables={
                "format_instructions": output_parser.get_format_instructions
            },
            output_parser=output_parser,
        ),
    )

    try:
        cards = Cards(cards=[])
        for doc in documents:
            resp = llm_chain.run(doc)
            cards.cards = cards.cards + output_parser.parse(resp).cards
        return cards.cards
    except json.JSONDecodeError as e:
        raise Exception(f"Could not decode openAI response: {resp}", e)


def load_content(content_path: str):
    loader = UnstructuredAPIFileLoader(
        content_path,
        url="http://unstructured:4000/general/v0/general",
        content_type="text/html",
    )
    documents = loader.load()
    return TokenTextSplitter(chunk_size=1000, chunk_overlap=0).split_documents(
        documents
    )


def download_content(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(response.content)
            return (f.name, str(response.content))
    else:
        raise Exception(f"Could not download from url {url}. Error: {response.content}")


def process_article(article_id: int):
    with SessionLocal() as db:
        article = db.query(Article).get(article_id)
        if article is None:
            logging.error(f"Article with id {article_id} is not present anymore.")
            return
        if article.url:
            article.status = ArticleStatus.DOWNLOADING
            db.add(article)
            db.commit()
            db.refresh(article)
            try:
                (content_path, content) = download_content(article.url)
                article.status = ArticleStatus.PROCESSING
                article.content = content
                db.add(article)
                db.commit()

                docs = load_content(content_path)
                cards = get_cards(docs)
                save_cards(cards, article, db)
                article.status = ArticleStatus.READY
            except Exception as e:
                logging.exception(
                    f"Error processing article {article.title}: %s", e, exc_info=True
                )
                article.status = ArticleStatus.ERROR
                article.error = "Processing error"
            db.add(article)
            db.commit()
