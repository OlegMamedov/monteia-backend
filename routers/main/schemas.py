from pydantic import BaseModel, validator
from datetime import date

class ChatRequest(BaseModel):
    message: str

class RegisterSchema(BaseModel):
    number: str
    f_name: str
    l_name: str
    birthday_date: date

class LoginSchema(BaseModel):
    number: str

class AuthSchema(BaseModel):
    number: str
    code: str

class GadanieSchema(BaseModel):
    pass
