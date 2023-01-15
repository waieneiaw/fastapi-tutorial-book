from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import TypedDict
from sqlalchemy.orm import Session
from .. import models, token
from ..database import get_db
from ..hashing import Hash

router = APIRouter(tags=["auth"])


AccessTokenResponse = TypedDict(
    "AccessTokenResponse", {"access_token": str, "token_type": str}
)


@router.post("/login")
def login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> AccessTokenResponse:
    user = (
        db.query(models.User)
        .filter(models.User.email == request.username)
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

    access_token = token.create_access_token(
        data={"sub": user.email, "id": user.id}
    )

    return {"access_token": access_token, "token_type": "bearer"}
