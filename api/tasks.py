from typing import List
from db.models import Article, ArticleStatus
from sqlalchemy.orm import Session
import requests
import tempfile
from unstructured.partition.json import partition_json
from langchain.document_loaders import UnstructuredAPIFileLoader
from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
import json
import logging


PROMPT = """
In the following text delimited with triple backticks, identify the most important ideas, sort them in descending order of importance
, take the top 5 ideas and create flash cards for them. Where a flash card has front text and a back text.
For example, if the key idea is "LLM means Large Language Model" then the flash card could be "front" : "LLM" and "back": "Large Language Model". 
{format_instructions}
Do not return anything else but the JSON object conforming the above schema.

```{text}```
"""


class Card(BaseModel):
    front: str = Field(description="text that should be on the front of the card")
    back: str = Field(description="text that should be at the back of the card")


class Cards(BaseModel):
    cards: List[Card] = Field(description="list of flash cards")


def load_content(content_path: str):
    loader = UnstructuredAPIFileLoader(
        content_path,
        url="http://unstructured:4000/general/v0/general",
        content_type="text/html",
    )
    documents = loader.load()

    llm = OpenAI(temperature=0, model_name="text-davinci-003")

    output_parser = PydanticOutputParser(pydantic_object=Cards)

    chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate(
            template=PROMPT,
            input_variables=["text"],
            partial_variables={
                "format_instructions": output_parser.get_format_instructions
            },
        ),
    )
    resp = chain.run(documents)
    try:
        cards = output_parser.parse(resp)
        print(cards.json(indent=2))
    except json.JSONDecodeError as e:
        raise Exception(f"Could not decode openAI response: {resp}", e)


def download_content(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(response.content)
            return (f.name, str(response.content))
    else:
        raise Exception(f"Could not download from url {url}. Error: {response.content}")


def process_article(article: Article, db: Session):
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

            load_content(content_path)
            article.status = ArticleStatus.READY
        except Exception as e:
            logging.exception(
                f"Error processing article {article.title}: %s", e, exc_info=True
            )
            article.status = ArticleStatus.ERROR
            article.error = "Processing error"
        db.add(article)
        db.commit()
