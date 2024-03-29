from typing import Optional
from datetime import datetime, timedelta
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from .schemas import TokenData
from .functions import user

SECRET_KEY = "8e36d1a7d73ceacfc0d6a76e0f6081c397d1dec71f516ac5824df4f5acf6609a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_token(token: str, credentials_exception: Exception, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        email: str | None = payload.get("sub")
        if not email:
            raise credentials_exception

        id: str | None = payload.get("id")
        if not id:
            raise credentials_exception

        _ = TokenData(email=email)

    except JWTError:
        raise credentials_exception

    result = user.show(db, id)
    return result
