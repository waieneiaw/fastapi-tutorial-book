from fastapi import FastAPI, Depends, status, HTTPException
from typing import Optional, List
from sqlalchemy.orm import Session
from . import models
from .schemas import Blog, ShowBlog, User, ShowUser
from .types import JsonType, HTTPResponse
from .models import Base
from .database import engine, sessionLocal
from .hashing import Hash

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


@app.get(
    "/blog", status_code=status.HTTP_200_OK, response_model=List[ShowBlog]
)
def all_fetch(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}", status_code=status.HTTP_200_OK, response_model=ShowBlog)
def show(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available",
        )

    return blog


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)) -> HTTPResponse:
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not found",
        )

    blog.delete(synchronize_session=False)
    db.commit()

    return {"data": "Deletion completed"}


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(
    id: int, request: Blog, db: Session = Depends(get_db)
) -> HTTPResponse:
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not found",
        )

    blog.update(request.dict())
    db.commit()

    return {"data": "Update completed"}


@app.post("/user")
def create_user(request: User, db: Session = Depends(get_db)):
    hashed_password = Hash.bcrypt(request.password)
    new_user = models.User(
        name=request.name, email=request.email, password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/user/{id}", response_model=ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} is not available",
        )

    return user
