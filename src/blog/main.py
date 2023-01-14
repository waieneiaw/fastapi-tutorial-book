from fastapi import FastAPI, Depends
from typing import Optional
from sqlalchemy.orm import Session
from . import models
from .schemas import Blog
from .types import JsonType, OkResponseType
from .models import Base
from .database import engine, sessionLocal

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = sessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def index():
    return {"data": {"name": "Test"}}


@app.get("/about")
def about():
    return {"data": {"name": "about"}}


@app.get("/blog/category")
def category() -> JsonType:
    return {"data": ["all category"]}


@app.get("/blog/{id}")
def show(id: int) -> OkResponseType:
    return {"data": id}


@app.get("/blog/{id}/comments")
def comments(id: int, limit: Optional[str] = None) -> OkResponseType:
    return {"data": [id, limit, "comments"]}


@app.post("/blog")
def create_blog(blog: Blog, db: Session = Depends(get_db)) -> OkResponseType:
    new_blog = models.Blog(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"data": new_blog}


@app.get("/blog")
def all_fetch(db: Session = Depends(get_db)) -> OkResponseType:
    blogs = db.query(models.Blog).all()
    return {"data": blogs}
