from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.database import get_db
from app.models import User
from app.schemas import TokenData

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if not payload.get('user_id'):
            raise HTTPException(status_code=400, detail='Token expired')

        token_data = TokenData(user_id=payload.get('user_id'))
    except JWTError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    token_data = verify_access_token(token)
    user = db.query(User).filter(User.id == token_data.user_id).first()
    if not user:
        raise HTTPException(status_code=409, detail='User nor found')
    return user