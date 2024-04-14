from fastapi import APIRouter, Depends, HTTPException

from FastapiInstagramClone.app.models import User
from FastapiInstagramClone.app.schemas import Token
from fastapi.security import OAuth2PasswordRequestForm
from FastapiInstagramClone.app.database import get_db
from FastapiInstagramClone.app.services.oauth2 import create_access_token
from FastapiInstagramClone.app.services.utils import verify
router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/login', status_code=200, response_model=Token)
def login(user: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    query = db.query(User).filter(User.email == user.username)

    if not query:
        raise HTTPException(status_code=409, detail="Invalid User email")

    if not verify(user.password, query.password):
        raise HTTPException(status_code=409, detail="Invalid User password")

    access_token = create_access_token(data={'user_id': query.id})

    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }
