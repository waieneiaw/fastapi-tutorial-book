from fastapi import APIRouter, Depends, status, HTTPException
from typing import Optional, List
from sqlalchemy.orm import Session
from .. import models
from ..schemas import Blog, ShowBlog
from ..types import JsonType, HTTPResponse
from ..database import get_db


router = APIRouter()


@router.get("/blog/category", tags=["blogs"])
def category() -> JsonType:
    return {"data": ["all category"]}


@router.get("/blog/{id}/comments", tags=["blogs"])
def comments(id: int, limit: Optional[str] = None) -> HTTPResponse:
    return {"data": [id, limit, "comments"]}


@router.post("/blog", status_code=status.HTTP_201_CREATED, tags=["blogs"])
def create_blog(blog: Blog, db: Session = Depends(get_db)) -> HTTPResponse:
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"data": new_blog}


@router.get(
    "/blog",
    status_code=status.HTTP_200_OK,
    response_model=List[ShowBlog],
    tags=["blogs"],
)
def all_fetch(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.get(
    "/blog/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowBlog,
    tags=["blogs"],
)
def show(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available",
        )

    return blog


@router.delete(
    "/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"]
)
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


@router.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["blogs"])
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
