from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db
from app.models import User
from app.schemas import Token
from app.services.oauth2 import create_access_token
from app.services.utils import verify

router = APIRouter(tags=['Auth'])


@router.post('/login', status_code=200, response_model=Token)
def login(user: OAuth2PasswordRequestForm = Depends(), db: Depends = Depends(get_db)):
    query = db.query(User).filter(User.email == user.username).first()

    if not query:
        raise HTTPException(status_code=409, detail="User not found")

    if not verify(user.password, query.password):
        raise HTTPException(status_code=409, detail="Invalid User password")

    access_token = create_access_token(data={'user_id': query.id})

    return {"access_token": access_token, "token_type": "Bearer"}