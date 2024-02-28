from fastapi import FastAPI, HTTPException
from models import User
from pydantic import BaseModel, EmailStr, validator
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME


app = FastAPI()

# SQLAlchemy
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



# Pydantic models
class UserCreate(BaseModel):
    name: str
    surname: str
    fatherland: str
    gender: str
    phone_number: str
    email: EmailStr
    password: str

    @validator("email")
    def validate_email(cls, value):
        if value.count('@') == 1 and value.count('.') == 1:
            if value.find('.') > value.find('@'):
                a = value.index('@')
                if not (value[a + 1:a + 5] == 'mail' or value[a + 1:a + 6] == 'gmail'):
                    raise HTTPException(status_code=500, detail='Должно быть mail или gmail')
                if value[a + 1:a + 5] == 'mail':
                    if not value[-3:] == '.ru':
                        raise HTTPException(status_code=500, detail='Проверьте правильность электронной почты')
                if value[a + 1:a + 6] == 'gmail':
                    if not value[-4:] == '.com':
                        raise HTTPException(status_code=500, detail='Проверьте правильность электронной почты')
                return value
            else:
                raise HTTPException(status_code=500, detail='@ должен быть перед .')
        else:
            raise HTTPException(status_code=500, detail='@ или . должен быть ровно 1 раз')

    @validator("name")
    def validate_name(cls, value):
        if len(value) < 2 or len(value) > 10:
            raise HTTPException(status_code=500, detail='Имя должно быть от 2 до 10 символов')
        if not value.istitle():
            raise HTTPException(status_code=500, detail='Имя должно начинаться с заглавной буквы')
        return value

    @validator("phone_number")
    def validate_phone_number(cls, value):
        if len(str(value)) <= 11:
            if str(value[:2]) == '87':
                return value
            else:
                raise HTTPException(status_code=500, detail='Неправильный номер')
        else:
            raise HTTPException(status_code=500, detail='Номер должен быть не более 11 символов')

    @validator("surname")
    def validate_surname(cls, value):
        if len(value) < 2 or len(value) > 10:
            raise HTTPException(status_code=500, detail='Фамилия должна быть от 2 до 10 символов')
        if not value.istitle():
            raise HTTPException(status_code=500, detail='Фамилия должна начинаться с заглавной буквы')
        return value

    @validator("fatherland")
    def validate_fatherland(cls, value):
        if len(value) < 2 or len(value) > 10:
            raise HTTPException(status_code=500, detail='Отчество должно быть от 2 до 10 символов')
        if not value.istitle():
            raise HTTPException(status_code=500, detail='Отчество должно начинаться с заглавной буквы')
        return value

    @validator("gender")
    def validate_gender(cls, value):
        if value == "Мужчина" or value == "Женщина":
            return value
        else:
            raise HTTPException(status_code=500, detail='Неверный гендер. Укажите "Мужчина" или "Женщина"')

    @validator("password")
    def validate_password(cls, value):
        s = '!@#$%^&*'
        total_e = 0
        total_N = 0
        total_n = 0
        total_s = 0
        if len(value) > 12:
            for i in value:
                if i.isupper():
                    total_N += 1
                if i.islower():
                    total_e += 1
                if i.isdigit():
                    total_n += 1
                if i in s:
                    total_s += 1
            if total_N < 3:
                raise HTTPException(status_code=500,
                                    detail='В пароле должно быть не менее 3 символов в верхнем регистре')
            if total_e < 6:
                raise HTTPException(status_code=500,
                                    detail='В пароле должно быть не менее 6 символов в нижнем регистре')
            if total_n < 3:
                raise HTTPException(status_code=500, detail='В пароле должно быть не менее 3 цифр')
            if total_s < 1:
                raise HTTPException(status_code=500, detail='В пароле должен быть хотя бы 1 спецсимвол')
            return value
        else:
            raise HTTPException(status_code=500, detail='Пароль должен содержать не менее 12 символов')


class UserResponse(BaseModel):
    id: int
    name: str
    surname: str
    fatherland: str
    gender: str
    phone_number: str
    email: EmailStr

# Routes
@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate):
    db = SessionLocal()
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user



# @app.post('/users')
# def users_kz(users: List[Userskz]):
#     fake_user.extend(users)
#     return {'status': 200, 'data': fake_user}


# @app.post("/login/")
# async def login(
#     name: str = Form(...),
#     surname: str = Form(...),
#     fatherland: str = Form(...),
#     gender: str = Form(...),
#     phone_number: str = Form(...),
#     email: str = Form(...),
#     password: str = Form(...),
# ):
#     user.append({
#         "name": name,
#         "surname": surname,
#         "fatherland": fatherland,
#         "gender": gender,
#         "phone_number": phone_number,
#         "email": email,
#         "password": password
#     })
#     return {"name": name, "surname": surname, "fatherland": fatherland, "gender": gender, "phone_number": phone_number, "email": email, "password": password}