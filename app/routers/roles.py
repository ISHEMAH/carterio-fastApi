from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.auth import AuthJWT

router = APIRouter()

@router.post("/", response_model=schemas.RoleBase)
def create_role(role: schemas.RoleCreate, db: Session = Depends(database.SessionLocal)):
    db_role = models.Role(name=role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

@router.get("/", response_model=list[schemas.RoleBase])
def list_roles(db: Session = Depends(database.SessionLocal)):
    roles = db.query(models.Role).all()
    return roles
