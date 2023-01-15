from fastapi import APIRouter, Depends, status, HTTPException
from typing import Optional, List
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..types import JsonType, HTTPResponse
from ..database import get_db
from ..functions import blog


router = APIRouter(
    prefix="/blog",
    tags=["blogs"],
)


@router.get("/category")
def category() -> JsonType:
    return {"data": ["all category"]}


@router.get("/{id}/comments")
def comments(id: int, limit: Optional[str] = None) -> HTTPResponse:
    return {"data": [id, limit, "comments"]}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_blog(
    request: schemas.Blog, db: Session = Depends(get_db)
) -> HTTPResponse:
    result = blog.create(db, request)
    return {"data": result}


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.ShowBlog],
)
def all_fetch(
    db: Session = Depends(get_db),
    _: schemas.User = Depends(oauth2.get_current_user),
):
    blogs = blog.get_all(db)
    return blogs


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowBlog,
)
def show(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available",
        )

    return blog


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)) -> HTTPResponse:
    return {"data": blog.delete(db, id)}


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(
    id: int, request: schemas.Blog, db: Session = Depends(get_db)
) -> HTTPResponse:
    return {"data": blog.update(db, id, request)}
