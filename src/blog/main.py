from fastapi import FastAPI, Depends, status, HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from . import models
from .schemas import Blog
from .types import JsonType, HTTPResponse
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


@app.get("/blog/{id}/comments")
def comments(id: int, limit: Optional[str] = None) -> HTTPResponse:
    return {"data": [id, limit, "comments"]}


@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create_blog(blog: Blog, db: Session = Depends(get_db)) -> HTTPResponse:
    new_blog = models.Blog(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"data": new_blog}


@app.get("/blog", status_code=status.HTTP_200_OK)
def all_fetch(db: Session = Depends(get_db)) -> HTTPResponse:
    blogs = db.query(models.Blog).all()
    return {"data": blogs}


@app.get("/blog/{id}", status_code=status.HTTP_200_OK)
def show(id: int, db: Session = Depends(get_db)) -> HTTPResponse:
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available",
        )

    return {"data": blog}
