from fastapi import APIRouter, Depends, HTTPException
from app.schemas import CommentSchema
from starlette import status
from app.services.oauth2 import get_current_user
from app.database import get_db
from app.models import Comment, Post
from sqlalchemy import and_
from fastapi import Form

router = APIRouter(prefix="/comment", tags=['comment'])


@router.post("/", status_code=status.HTTP_201_CREATED)
def comment_to_post(post: CommentSchema, db=Depends(get_db), user=Depends(get_current_user)):
    post_ = db.query(Post).filter(Post.id == post.post_id).first()

    if post_ is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    comment = Comment(**post.dict(), owner_id=user.id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return {"message": "create comment"}


@router.get("/comments_get")
def comment_list(post_id, db=Depends(get_db), user=Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    comments = db.query(Comment).filter(and_(Comment.post_id == post_id, Comment.owner_id == user.id)).all()
    return comments


@router.put("/update")
def comment_update(comment_id, content=Form(), db=Depends(get_db), user=Depends(get_current_user)):
    comment = db.query(Comment).filter(and_(Comment.id == comment_id, Comment.owner_id == user.id)).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    db.query(Comment).filter(Comment.id == comment_id).update({"content": content})
    db.commit()
    return {"message": "successful"}


@router.delete("/delete")
def comment_delete(comment_id, db=Depends(get_db), user=Depends(get_current_user)):
    comment = db.query(Comment).filter(and_(Comment.id == comment_id, Comment.owner_id == user.id)).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    db.query(Comment).filter(Comment.id == comment_id).delete()
    db.commit()
    return {"message": "successful"}
