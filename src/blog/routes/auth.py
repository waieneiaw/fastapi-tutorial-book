from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..hashing import Hash

router = APIRouter(tags=["auth"])


@router.post("/login")
def login(request: schemas.Login, db: Session = Depends(get_db)):
    user = (
        db.query(models.User)
        .filter(models.User.email == request.email)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials",
        )

    if not Hash.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials"
        )

    return user
