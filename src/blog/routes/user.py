from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import models
from ..schemas import User, ShowUser
from ..database import get_db
from ..hashing import Hash

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/")
def create_user(request: User, db: Session = Depends(get_db)):
    hashed_password = Hash.bcrypt(request.password)
    new_user = models.User(
        name=request.name, email=request.email, password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} is not available",
        )

    return user