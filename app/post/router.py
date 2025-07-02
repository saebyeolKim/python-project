from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.post import service, schemas
from app.db import SessionLocal
from fastapi import Depends
from app.auth.dependencies import get_current_user
from app.models import User

post_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@post_router.get("/posts", response_model=list[schemas.Post])
def read_posts(db: Session = Depends(get_db)):
    return service.get_posts(db)

@post_router.get("/posts/{post_id}", response_model=schemas.Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = service.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@post_router.post("/posts", response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate, 
    db: Session = Depends(get_db),
    currnet_user: User = Depends(get_current_user)
):
    return service.create_post(db, post)

@post_router.delete("/posts/{post_id}", response_model=schemas.Post)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = service.delete_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post