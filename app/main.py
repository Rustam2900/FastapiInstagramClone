from fastapi import FastAPI

from app.router.user import router as user_router
from app.router.auth import router as auth_router
from app.router.post import router as post_router
from app.router.post import app as post_app
from app.router.like import router as like_router
from app.router.comment import router as comment_router

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(post_router)
app.include_router(like_router)
app.include_router(comment_router)
app.include_router(post_app)