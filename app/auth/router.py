from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.auth import schemas, service
from app.models import User
from app.db import SessionLocal

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup", response_model=schemas.Token)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = service.hash_password(user.password)
    new_user = User(username=user.username, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = service.create_access_token(data={"sub": new_user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if not existing or not service.verify_password(user.password, existing.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    token = service.create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
    