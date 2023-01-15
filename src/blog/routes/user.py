from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas import User, ShowUser
from ..database import get_db
from ..functions import user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/")
def create_user(request: User, db: Session = Depends(get_db)):
    return user.create(db, request)


@router.get("/{id}", response_model=ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.show(db, id)
