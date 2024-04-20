from fastapi import APIRouter, Depends, HTTPException

from app.models import User
from app.services.utils import hash
from app.database import get_db
from app.schemas import UserCreate, UserOutput
from app.services.oauth2 import get_current_user
from starlette import status

# from fastapi import Form

router = APIRouter(prefix='/user', tags=['User'])


@router.post('/register', status_code=201, response_model=UserOutput)
def user_create(user: UserCreate, db: Depends = Depends(get_db)):
    query = db.query(User).filter(User.email == user.email)

    if query.first() is not None:
        raise HTTPException(status_code=409, detail=f"This {user.email} is already registered.")

    user.password = hash(user.password)
    user = User(**user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/user_get", response_model=UserOutput)
def user_get(db: Depends = Depends(get_db), user: UserOutput = Depends(get_current_user)):
    query = db.query(User).filter(User.email == user.email)

    if query.first() is None:
        raise HTTPException(status_code=403, detail="User not Found")

    return query.first()


@router.delete("/delete")
def user_get(db: Depends = Depends(get_db), user: UserOutput = Depends(get_current_user)):
    query = db.query(User).filter(User.email == user.email).first()

    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not Found")

    db.query(User).filter(User.email == user.email).delete()
    db.commit()
    return {"message": "successful"}