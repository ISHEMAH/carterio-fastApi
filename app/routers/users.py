from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.auth import AuthJWT
from app.utils import get_password_hash, verify_password
from fastapi.security import HTTPBearer

router = APIRouter()

security = HTTPBearer()

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(database.SessionLocal)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_password, role_id=user.role_id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(username: str, password: str, Authorize: AuthJWT = Depends(), db: Session = Depends(database.SessionLocal)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = Authorize.create_access_token(subject=str(user.id))
    return {"access_token": access_token}

@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(Authorize: AuthJWT = Depends(), db: Session = Depends(database.SessionLocal)):
    Authorize.jwt_required()
    user_id = int(Authorize.get_jwt_subject())
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
