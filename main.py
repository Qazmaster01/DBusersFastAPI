from fastapi import FastAPI, Form, Body, HTTPException
from pydantic import BaseModel, Field, validator
from typing import List
from typing import Annotated
app = FastAPI()

fake_user = []

#Пользватель
class Userskz(BaseModel):
    name: str
    surname: str
    fatherland: str
    gender: str
    phone_number: str
    email: str
    password: str


    #валидация email
    @validator("email")
    @classmethod
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
    #валидация name
    @validator("name")
    @classmethod
    def validate_name(cls, value):
        if len(value) < 2 or len(value) > 10:
            raise TypeError('Имя меньше 2 букв')
        if not value.istitle():
            raise HTTPException(status_code=500, detail='Имя должен начинаться с заглавной буквой')
            # raise TypeError('Имя должен начинаться с заглавной буквой')
        return value

    #валидация phone_number
    @validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value):
        if len(str(value)) <= 11:
            if str(value[:2]) == '87':
                return value
            else:
                raise HTTPException(status_code=500, detail='Неправильный номер')
        else:
            raise HTTPException(status_code=500, detail='Номер меньше 11')

    #валидация surname
    @validator("surname")
    @classmethod
    def validate_surname(cls, value):
        if len(value) < 2 or len(value) > 10:
            raise HTTPException(status_code=500, detail='Фамилия меньше 2 букв')
        if not value.istitle():
            raise HTTPException(status_code=500, detail='Фамилия должно начинаться с заглавной буквой')
        return value

    #валидация fatherland
    @validator("fatherland")
    @classmethod
    def validate_fatherland(cls, value):
        if len(value) < 2 or len(value) > 10:
            raise HTTPException(status_code=500, detail='Отечество меньше 2 букв')
        if not value.istitle():
            raise HTTPException(status_code=500, detail='Отечество должно начинаться с заглавной буквой')
        return value

    #валидация gender
    @validator("gender")
    @classmethod
    def validate_gender(cls, value):
        if value == "Мужчина" or value == "Женщина":
            return value
        else:
            raise HTTPException(status_code=500, detail='Неверный гендер. Укажите гендер так (Мужчина - если вы мужчина) или (Женщина - если вы женщина)')

    #валидаация password
    @validator("password")
    @classmethod
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
                raise HTTPException(status_code=500, detail='В пароле верхний регистр меньше 3')
            if total_e < 6:
                raise HTTPException(status_code=500, detail='В пароле нижний регистр меньше 6')
            if total_n < 3:
                raise HTTPException(status_code=500, detail='В пароле цифры меньше 3')
            if total_s < 1:
                raise HTTPException(status_code=500, detail='В пароле спецсимволы меньше 1')
            if total_N >= 2 or total_e > 6 or total_n > 3 or total_s > 1:
                return value
        else:
            raise HTTPException(status_code=500, detail='В пароле длина пароля меньше 12')


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
user = []
@app.post("/login/")
async def login(users: List[Userskz] = Body(...)):
    fake_user.extend(users)
    return {'data': fake_user}