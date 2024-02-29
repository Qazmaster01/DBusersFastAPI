from fastapi import FastAPI, HTTPException
from src.crud import pydant
from src.crud.hashing import Hasher
from models import User
from pydantic import BaseModel, EmailStr, validator
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
from src.crud.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME


app = FastAPI()

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Routes
@app.post("/users/", response_model=pydant.UserResponse)
async def create_user(user: pydant.UserCreate):
    db = SessionLocal()
    # db_user = User(**user.dict())
    db_user = User(
        name = user.name,
        surname = user.surname,
        fatherland = user.fatherland,
        gender = user.gender,
        phone_number = user.phone_number,
        email = user.email,
        password = Hasher.get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=pydant.UserResponse)
async def read_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найдено")
    return user

@app.put("/users/{user_id}", response_model=pydant.UserResponse)
async def update_user(user_id: int, name: str, surname: str, fatherland: str, gender: str, phone_number: str, email: str, password: str):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найдено")
    user.name = name
    user.surname = surname
    user.fatherland = fatherland
    user.gender = gender
    user.phone_number = phone_number
    user.email = email
    user.password = Hasher.get_password_hash(password)
    db.commit()
    db.refresh(user)
    return user



@app.delete("/users/remove", response_model=pydant.UserResponse)
async def remove_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найдено")
    db.delete(user)
    db.commit()
    return user
