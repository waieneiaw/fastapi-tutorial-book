from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas


def get_all(db: Session) -> List[models.Blog]:
    blogs = db.query(models.Blog).all()
    return blogs


def create(
    db: Session, request: schemas.Blog, current_user: models.User
) -> models.Blog:
    new_blog = models.Blog(
        title=request.title, body=request.body, user_id=current_user.id
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def delete(db: Session, id: int) -> str:
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not found",
        )

    blog.delete(synchronize_session=False)
    db.commit()

    return "done"


def update(db: Session, id: int, request: schemas.Blog) -> str:
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not found",
        )

    blog.update(request.dict())
    db.commit()

    return "updated"
