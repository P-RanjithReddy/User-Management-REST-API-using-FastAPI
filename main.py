from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import Base, engine, get_db
import models
import schemas
import crud

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Management REST API",
    description="Simple CRUD API with FastAPI, Pydantic, SQLAlchemy and SQLite.",
    version="1.0.0",
)

@app.get("/")
def home():
    return {"message": "User Management API is running", "docs": "/docs"}

@app.post("/users", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=409, detail="Email already exists")
    return crud.create_user(db, user)

@app.get("/users", response_model=list[schemas.UserResponse])
def get_users(
    city: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    return crud.get_users(db, city=city, is_active=is_active)

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user_data: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_data.email and user_data.email != user.email:
        existing = crud.get_user_by_email(db, user_data.email)
        if existing:
            raise HTTPException(status_code=409, detail="Email already exists")
    return crud.update_user(db, user, user_data)

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, user)
    return {"message": f"User {user_id} deleted successfully"}
