from fastapi import FastAPI
from typing import Optional
from .schemas import Blog
from .types import JsonType, OkResponseType
from .models import Base
from .database import engine

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def index():
    return {"data": {"name": "Test"}}


@app.get("/about")
def about():
    return {"data": {"name": "about"}}


@app.get("/blog/category")
def category() -> JsonType:
    return {"data": ["all category"]}


@app.get("/blog")
def item(limit: int = 10, published: bool = True) -> OkResponseType:
    if published:
        return {"data": f"{limit}件"}
    else:
        return {"data": "非公開"}


@app.get("/blog/{id}")
def show(id: int) -> OkResponseType:
    return {"data": id}


@app.get("/blog/{id}/comments")
def comments(id: int, limit: Optional[str] = None) -> OkResponseType:
    return {"data": [id, limit, "comments"]}


@app.post("/blog")
def create_blog(blog: Blog) -> OkResponseType:
    return {"data": blog}
